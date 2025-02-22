#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This script processes the text data to generate named entities based on SpaCy's NER extractor.
'''
import logging
from pathlib import Path
from collections import Counter
import gzip
import json
import re

import click

from joblib import Parallel, delayed
import joblib
import spacy

import wb_nlp
from wb_nlp.utils.scripts import configure_logger, create_dask_cluster

# logging.basicConfig(stream=sys.stdout,
#                     level=logging.INFO,
#                     datefmt='%Y-%m-%d %H:%M',
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

MAX_LENGTH = 1000000

nlp = spacy.load("en_core_web_sm", disable=["parser"])

valid_entities = set([
    'PERSON',
    'NORP',
    'FAC',
    'ORG',
    'GPE',
    'LOC',
    'PRODUCT',
    'EVENT',
    'WORK_OF_ART',
    'LAW',
    'LANGUAGE',
])


def get_spacy_entities(doc):
    '''Gets a list of entities discovered from the document.
    '''
    return [f"{ent.label_}:{ent.text}" for ent in doc.ents if ent.label_ in valid_entities]


def joblib_extract_spacy_named_entities(
        file_id: int, input_file: Path,
        output_dir: Path, logger=None):
    '''
    Wrapper function used in joblib to parallelize extraction of
    named entities across text documents.
    '''
    if logger is not None:
        logger.info(f"Processing {file_id}: {input_file.name}")

    with open(input_file, "rb") as in_file:
        text = in_file.read().decode("utf-8", errors="ignore")[:MAX_LENGTH]

        entities = get_spacy_entities(doc=nlp(text))
        entities = dict(Counter(entities).most_common())

        result = dict(lib='SpaCy', tokens=[], entities=entities)

    output_file = output_dir / (input_file.name + '.json.gz')

    with gzip.open(output_file, mode='wt', encoding='utf-8') as gz_file:
        json.dump(result, gz_file)

    return True


_logger = logging.getLogger(__file__)


@click.command()
@click.option('--input-dir', 'input_dir', required=True,
              type=click.Path(exists=True), help='path to directory of raw text files')
@click.option('--output-dir', 'output_dir', required=True,
              type=click.Path(exists=False), help='path to directory of output text files')
@click.option('--quiet', 'log_level', flag_value=logging.WARNING, default=True)
@click.option('-v', '--verbose', 'log_level', flag_value=logging.INFO)
@click.option('-vv', '--very-verbose', 'log_level', flag_value=logging.DEBUG)
@click.option('--n-workers', 'n_workers', required=False, default=None)
@click.option('--batch-size', 'batch_size', required=False, default=None)
@click.version_option(wb_nlp.__version__)
def main(input_dir: Path, output_dir: Path, log_level: int, n_workers: int = None, batch_size: int = None):
    '''
    Entry point for part-of-speech based phrase generation script.
    '''
    configure_logger(log_level)

    # YOUR CODE GOES HERE! Keep the main functionality in src/wb_nlp
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    logging.info('Checking directories...')
    if not input_dir.exists():
        raise ValueError("Input directory doesn't exist!")

    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    client = create_dask_cluster(_logger, n_workers=n_workers)
    _logger.info(client)

    _logger.info('Starting joblib tasks...')
    with joblib.parallel_backend('dask'):
        batch_size = 'auto' if batch_size is None else int(batch_size)

        res = Parallel(verbose=10, batch_size=batch_size)(
            delayed(joblib_extract_spacy_named_entities)(
                ix, i, output_dir) for ix, i in enumerate(input_dir.glob('*.txt'), 1))

    entity_by_doc = Counter()
    entity_by_freq = Counter()

    for json_gz in output_dir.glob('*.json.gz'):
        with gzip.open(json_gz) as gz_file:
            json_data = json.load(gz_file)
            ents = json_data.get('entities', {})
            ents_count = Counter()

            for k, v in ents.items():
                ents_count.update({
                    re.sub(r'\s+', ' ', k).replace(
                        ':the ', ':').replace(':The ', ':').strip(): v})

            entity_by_doc.update(set(ents))
            entity_by_freq.update(ents)

    with gzip.open(output_dir / 'entity_by_doc.json.gzip', mode='wt', encoding='utf-8') as gz_file:
        json.dump(dict(entity_by_doc.most_common()), gz_file)

    with gzip.open(output_dir / 'entity_by_freq.json.gzip', mode='wt', encoding='utf-8') as gz_file:
        json.dump(dict(entity_by_freq.most_common()), gz_file)

    # Example analysis
    # climate = Counter(dict(filter(lambda x: 'paris climate' in x[0].lower() or 'paris agreement' in x[0].lower(), entity_by_doc.most_common())))
    # gpe = Counter(dict(filter(lambda x: x[0].startswith('GPE'), entity_by_doc.most_common())))

    _logger.info('Processed all: %s', all(res))

# Parameters:
# - Location of input data
# - Directory of * .txt files
# - MongoDB database


if __name__ == '__main__':
    # export DASK_DISTRIBUTED__SCHEDULER__ALLOWED_FAILURES=210
    # export DASK_DISTRIBUTED__COMM__TIMEOUTS__CONNECT=60
    # export DASK_DISTRIBUTED__COMM__RETRY__COUNT=20

    # Use in local machine
    # python -u ./scripts/extraction/generate_spacy_named_entities.py --input-dir ./data/raw/sample_data/TXT_SAMPLE --output-dir ./data/preprocessed/sample_data/spacy_entities -v --n-workers 6 |& tee ./logs/generate_spacy_named_entities.py.log

    # Use in w1lxbdatad07
    # python -u ./scripts/extraction/generate_spacy_named_entities.py --input-dir /data/wb536061/wb_nlp/data/raw/CORPUS/<corpus_id>/TXT_ORIG --output-dir /data/wb536061/wb_nlp/data/preprocessed/CORPUS/<corpus_id>/spacy_entities -v --n-workers 48 |& tee ./logs/generate_spacy_named_entities.py.log

    main()
