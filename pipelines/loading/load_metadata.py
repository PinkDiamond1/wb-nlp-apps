"""
This script handles the loading of the cleaned metadata into the mongodb.

Data from scraping server is compressed.
server: scraping server
workdir: data/corpus
command: tar -czvf KCP_<list_of_corpus_ids_to_compress_separated_by_underscore>.tar.gz

Send compressed data to gateway:
server: scraping server
workdir: data/corpus
command: rsync -avP KCP_<list_of_corpus_ids_to_compress_separated_by_underscore>.tar.gz gw1:~/

Send data in gateway to app server:
server: gateway server
workdir: ~/
command: rsync -avP KCP_<list_of_corpus_ids_to_compress_separated_by_underscore>.tar.gz app_server:/<path_to_app>/wb_nlp/data/corpus/

Decompress data in app server:
server: app server
workdir: /<path_to_app>/wb_nlp/data/corpus/
command: tar -xzvf KCP_<list_of_corpus_ids_to_compress_separated_by_underscore>.tar.gz

Enter nlp_api container
server: app server
command: docker exec -it wb_nlp_nlp_api_1 /bin/bash

Activate nlp_api conda environment
server: nlp_api container
command: conda activate nlp_api

Load available new data to db and es
server: nlp_api container
command: python pipelines/loading/load_metadata.py

Further steps:

Clean processed data
server: scraping server
workdir: /workspace/
command: python -u ./scripts/cleaning/clean_corpus.py --cleaning-config-id <cleaning_config_id> --input-dir data/corpus --source-dir-name EN_TXT_ORIG --recursive -vv |& tee ./logs/clean_corpus.py.log

Compress cleaned data
server: scraping server
workdir: data/corpus
command: tar -czvf KCP_cleaned_corpus-id-1_corpus-id-2_corpus-id-3.tar.gz cleaned/<cleaning_config_id>/corpus_id_1 cleaned/<cleaning_config_id>/corpus_id_2 cleaned/<cleaning_config_id>/corpus_id_3 ...


Send cleaned data to gateway
server: scraping server
workdir: data/corpus
command: rsync -avP KCP_cleaned_corpus-id-1_corpus-id-2_corpus-id-3.tar.gz gw1:~/

Send cleaned data from gateway to app server
server: gateway server
workdir: ~/
command: rsync -avP KCP_cleaned_corpus-id-1_corpus-id-2_corpus-id-3.tar.gz app_server:/<path_to_app>/wb_nlp/data/corpus/


Transform documents and load to model server


1. Load data to elasticsearch. Do this by running the following snippet:

    # # # Optional - depends if the index is broken
    # # from elasticsearch_dsl import Index
    # # i = Index(name=elasticsearch.DOC_INDEX, using=elasticsearch.get_client())
    # # i.delete()
    # from wb_nlp.interfaces import elasticsearch, mongodb
    # docs_metadata_coll = mongodb.get_collection(
    #     db_name="test_nlp", collection_name="docs_metadata")
    # docs_metadata = list(docs_metadata_coll.find({}))
    # elasticsearch.make_nlp_docs_from_docs_metadata(docs_metadata, ignore_existing=True, en_txt_only=True, remove_doc_whitespaces=True)
    # elasticsearch.make_nlp_docs_from_docs_metadata(docs_metadata, ignore_existing=False, en_txt_only=True, remove_doc_whitespaces=True)

2. Next clean the documents and generate the vectors for the data.

"""
from datetime import datetime
import json
from pathlib import Path
from wb_nlp import dir_manager
from wb_nlp.interfaces import elasticsearch, mongodb


def get_docs_metadata_collection():
    return mongodb.get_collection(
        db_name="test_nlp", collection_name="docs_metadata")


def load_clean_metadata():
    """
    This function loads the cleaned metadata generated from
    pipelines/cleaning/document_pipeline.py to the mongodb database.

    The files are expected to be stored in corpus/<corpus_id>/<l_corpus_id>_clean_metadata.jsonl paths.
    """

    collection = get_docs_metadata_collection()
    ids_in_db = {i["_id"]
                 for i in collection.find({}, projection=["_id"])}

    corpus_path = Path(dir_manager.get_data_dir("corpus"))

    for metadata_file in corpus_path.glob("*/*_clean_metadata.jsonl"):
        corpus_id = metadata_file.parent.name
        print(f"Processing metadata from {corpus_id}...")

        metadata = []
        total_meta = 0

        with open(metadata_file) as open_file:
            for line in open_file:
                total_meta += 1
                line = line.strip()
                meta = json.loads(line)

                if meta["id"] in ids_in_db:
                    continue

                meta["_id"] = meta["id"]

                pid = meta.get("project_id")

                if not pid:
                    wb_pid = meta.get("wb_project_id")
                    if wb_pid:
                        meta["project_id"] = wb_pid

                # ["adm_region", "doc_type", "major_doc_type"]:
                for field in meta.keys():
                    # Convert any empty data to None
                    if not meta[field]:
                        meta[field] = None

                metadata.append(meta)
                ids_in_db.add(meta["id"])

        print(
            f"Inserting {len(metadata)} of {total_meta} data for {corpus_id} to DB...")
        if metadata:
            collection.insert_many(metadata)


def load_data_to_es(ignore_existing=True):
    docs_metadata_coll = get_docs_metadata_collection()

    docs_metadata = list(docs_metadata_coll.find({}))
    elasticsearch.make_nlp_docs_from_docs_metadata(
        docs_metadata, ignore_existing=ignore_existing, en_txt_only=True, remove_doc_whitespaces=True)

    return len(docs_metadata)


def set_update_latest_data(mongodb_doc_count):
    collection = mongodb.get_latest_update_collection()

    search = elasticsearch.NLPDoc.search()
    search.aggs.bucket("corpus_count", "terms", field="corpus").bucket(
        "docs_count", "terms", field="major_doc_type")
    executed_search = search.execute()
    docs_summary_stats = executed_search.aggs.to_dict()

    collection.insert_one(
        dict(
            last_update_date=datetime.now(),
            docs_summary_stats=docs_summary_stats,
            es_doc_count=search.count(),
            mongodb_doc_count=mongodb_doc_count,
        )
    )


def main():
    print("load_clean_metadata")
    load_clean_metadata()

    print("load_data_to_es")
    mongodb_doc_count = load_data_to_es()

    print("set_update_latest_data")
    set_update_latest_data(mongodb_doc_count)

    print("Finished...")


if __name__ == "__main__":
    main()
