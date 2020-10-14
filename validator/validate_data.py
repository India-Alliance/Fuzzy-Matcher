import ast
import json
import os

import jsonschema
import pandas as pd
from collections import defaultdict

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


def validate_json_instance(json_instance, UNMATCHED_ENTITIES):
    """Validates a json instance according to schema"""
    errors = []
    for error in VALIDATOR.iter_errors(json_instance):
        message = error.message
        if 'enum' in error.absolute_schema_path:
            message = f"{error.instance} is not a valid value for schema " \
                      f"property ({error.absolute_schema_path[1]})"

        errors.append(message)
        UNMATCHED_ENTITIES[error.absolute_schema_path[1]].append(error.instance)

    return errors


def _safe_eval_items(input_dict):
    """Safely evaluate items of dictionary, falling back to string"""
    output_dict = {}
    for key, value in input_dict.items():
        if value:
            try:
                eval_value = ast.literal_eval(value)
            except (ValueError, SyntaxError):
                eval_value = value
            finally:
                output_dict[key] = eval_value

    return input_dict


def validate_csv_dataset(path_to_file, log_file=None):
    errors_map = {}
    path_to_file = os.path.join(os.path.abspath(os.getcwd()), path_to_file)
    df = pd.read_csv(path_to_file, dtype=object,
                     keep_default_na=False, na_values=None)

    UNMATCHED_ENTITIES = defaultdict(list)

    for i, row in df.iterrows():
        json_instance = _safe_eval_items(row.to_dict())
        errors_map[i+1] = validate_json_instance(
            json_instance, UNMATCHED_ENTITIES
        )

    if log_file:
        with open(log_file, 'w') as f:
            for row, errors in errors_map.items():
                for error in errors:
                    f.write(f"Row {row}. Error: {error}\n")
    else:
        print(errors_map)

    return UNMATCHED_ENTITIES
