import ast
import json
import os

import jsonschema
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))

SCHEMA_FILE = os.path.abspath(
    os.path.join(HERE, '../data/json-schema/main-schema.json')
)
SCHEMA_DIR = os.path.dirname(SCHEMA_FILE)

with open(SCHEMA_FILE, 'r') as f:
    SCHEMA = json.load(f)

RESOLVER = jsonschema.RefResolver(base_uri='file://' + SCHEMA_DIR + '/',
                                           referrer=SCHEMA_FILE)
VALIDATOR = jsonschema.Draft7Validator(schema=SCHEMA, resolver=RESOLVER)


def validate_json_instance(json_instance):
    """Validates a json instance according to schema"""
    errors = []
    for error in VALIDATOR.iter_errors(json_instance):
        message = error.message
        if 'enum' in error.absolute_schema_path:
            message = f"{error.instance} is not a valid value for schema " \
                      f"property ({error.absolute_schema_path[1]})"

        errors.append(message)

    return errors


def validate_csv_dataset(path_to_file, log_file=None):
    with open(path_to_file, 'r') as f:
        errors_map = {}

        df = pd.read_csv(path_to_file)

        for i, row in df.iterrows():
            json_instance = row.to_dict()
            errors_map[i+1] = validate_json_instance(json_instance)

    return errors_map


if __name__ == "__main__":
    errors_map = validate_csv_dataset('test.csv')
