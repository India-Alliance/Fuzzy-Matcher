""" Functionality to convert grid csv to json schema"""
import csv
import json
import os

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data')


if __name__ == "__main__":
    schema = {
        "definitions": {
            "university": {
                "type": "string",
                "description": "Proposed uni",
                "enum": [
                ]
            }
        }
    }

    with open(os.path.join(DATA_PATH, "grid.csv"), 'r') as f:
        f.readline()  # Skips first line that contains headers
        for row in csv.reader(f):
            schema["definitions"]["university"]["enum"].append(row[1])

    output_json_path = os.path.join(DATA_PATH, "json-schema/universities.json")

    with open(output_json_path, 'w') as f:
        json.dump(schema, f, sort_keys=True, indent=4)
