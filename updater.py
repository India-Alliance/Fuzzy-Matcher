import pandas as pd
import argparse
from tqdm import tqdm


def update_the_correct_entries():
    parser = argparse.ArgumentParser()
    parser.add_argument('path_to_input_file', help='Path to the input File')
    parser.add_argument("column_to_update", help="Name of the column to update")
    args = parser.parse_args()
    suggestions = pd.read_csv('Suggestions.csv')
    entries_to_update = suggestions.loc[suggestions['Correct (True/False)'] == True]
    uploaded_data = pd.read_csv(args.path_to_input_file)
    for index in tqdm(entries_to_update.index):
        entry = entries_to_update.loc[index]
        uploaded_data.loc[uploaded_data[args.column_to_update]
                          == entry.at['Uploaded Name'], args.column_to_update] = entry.at['Matched Names']
    uploaded_data.to_csv('ValidatedData.csv')


if __name__ == "__main__":
    update_the_correct_entries()
