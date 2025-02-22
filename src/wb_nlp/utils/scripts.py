'''
Module containing common functions used across the scripts.
'''
import logging
from functools import lru_cache

import click

# export DASK_DISTRIBUTED__SCHEDULER__ALLOWED_FAILURES=210
# export DASK_DISTRIBUTED__COMM__TIMEOUTS__CONNECT=60
# export DASK_DISTRIBUTED__COMM__RETRY__COUNT=20
from wb_cleaning.cleaning import cleaner
from wb_nlp.interfaces import mongodb


@click.command()
@click.option('-c', '--config', 'cfg_path', required=False,
              type=click.Path(exists=False), help='path to yaml config file')
@click.option('--input-file', 'input_file', required=False,
              type=click.Path(exists=False), help='path to wiki articles generated by gensim.scripts.segment_wiki')
@click.option('--output-file', 'output_file', required=False,
              type=click.Path(exists=False), help='path to output json file of article titles and intros')
@click.option('--quiet', 'log_level', flag_value=logging.WARNING, default=True)
@click.option('-v', '--verbose', 'log_level', flag_value=logging.INFO)
@click.option('-vv', '--very-verbose', 'log_level', flag_value=logging.DEBUG)
def get_command_options(**kwargs):
    '''
    Generic command line arguments extractor.

    Let the individual script handle the extraction, validation, and
    extraction of relevant parameters.

    Returns a dictionary of arguments.
    '''
    return kwargs


@lru_cache(maxsize=64)
def get_cleaner(cleaning_config_id):

    cleaning_configs_collection = mongodb.get_cleaning_configs_collection()
    config = cleaning_configs_collection.find_one({"_id": cleaning_config_id})
    cleaner_object = cleaner.BaseCleaner(config=config)

    return cleaner_object
