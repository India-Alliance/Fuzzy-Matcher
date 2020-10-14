import sys
from validator.validate_data import validate_csv_dataset
from matcher.standardise import standardise_list
import pandas as pd


def setup_input_output_paths(path_to_file):
    path_to_input_file = sys.argv[1] if len(sys.argv) > 1 else 'test.csv'
    path_to_output_file = sys.argv[2] if len(sys.argv) > 2 else 'log.txt'

    if path_to_input_file is None:
        if path_to_file is not None:
            path_to_input_file = path_to_file
        else:
            path_to_input_file = 'test.csv'

    if path_to_output_file is None:
        path_to_output_file = 'log.txt'

    return path_to_input_file, path_to_output_file


def validate_and_suggest_corrections(path_to_file=None):
    path_to_input_file, path_to_output_file = setup_input_output_paths(path_to_file)

    unmatched_entities = validate_csv_dataset(path_to_input_file,
                                              log_file=path_to_output_file)
    print('Entries which were not matched \n\n', unmatched_entities)
    # Now let us try fuzzy matching names to identify
    # typos or non-standard entries.

    # First let's run the university standardiser
    uploaded_names_df = pd.DataFrame({'uploaded_names': unmatched_entities['affiliationCurrent']})
    uploaded_names_df.to_csv('entries_to_fuzzy_match.csv')

    standardise_list('entries_to_fuzzy_match.csv',
                     column_name_to_standardise='uploaded_names')


if __name__ == "__main__":
    validate_and_suggest_corrections()
