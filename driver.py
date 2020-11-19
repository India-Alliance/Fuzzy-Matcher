import sys, os
from validator.validate_data import validate_csv_dataset
from matcher.standardise import standardise_list
import pandas as pd
import argparse
import jsonschema
import json


def validate_data(path_to_file):
    unmatched_entities = validate_csv_dataset(path_to_file,
                                              log_file='log.txt')
    print('Detailed logs can be viewed in log.txt')
    return unmatched_entities


def load_json_file():
    HERE = os.path.dirname(os.path.abspath(__file__))

    SCHEMA_FILE = os.path.abspath(
        os.path.join(HERE, '../Fuzzy-Matcher/data/json-schema/criteria-json-schema.json')
    )
    SCHEMA_DIR = os.path.dirname(SCHEMA_FILE)

    with open(SCHEMA_FILE, 'r') as f:
        SCHEMA = json.load(f)
    return SCHEMA


def match_and_suggest_corrections(unmatched_entities):
    # Now let us try fuzzy matching names to identify
    # typos or non-standard entries.

    SCHEMA = load_json_file()
    columns_to_fuzzy_match = SCHEMA['fuzzy-match']

    unmatched_entities = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in unmatched_entities.items()]))
    unmatched_entities.to_csv('entries_to_fuzzy_match.csv')
    for column_to_fuzzy_match in columns_to_fuzzy_match:
        standardise_list('entries_to_fuzzy_match.csv',
                         column_name_to_standardise=column_to_fuzzy_match,
                         column_entity_type=columns_to_fuzzy_match[column_to_fuzzy_match])


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Validate and Fuzzy Match non-standard entries')
    parser.add_argument("--path_to_standard_file")
    parser.add_argument("--validate", '-v', action='store_true', help="Validate the data")
    parser.add_argument("--match", '-m', action='store_true', help="Fuzzy Match the data against the standard list provided")
    parser.add_argument('path_to_file_to_standardise')

    args = parser.parse_args()

    if args.validate:
        unmatched_entities = validate_data(args.path_to_file_to_standardise)
        print(unmatched_entities)

    if args.match:
        unmatched_entities = validate_data(args.path_to_file_to_standardise)
        match_and_suggest_corrections(unmatched_entities)

