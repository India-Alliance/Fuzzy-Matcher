from fuzzywuzzy import process, fuzz
from fuzzywuzzy.utils import full_process
from matcher.initialise_standard_univ_list import initialise_standard_univ_list
from matcher.convert_to_data_frame import convert_to_data_frame
from tqdm import tqdm

import pandas as pd
import time
from argparse import ArgumentParser

def get_standard_names_names():
    standard_names = initialise_standard_univ_list()
    return standard_names['Name']


def standardise_name(uploaded_name, standard_names):
    acronym_match = standard_names.loc[
        standard_names['acronym'] == uploaded_name, 'Name'
    ]

    if not acronym_match.empty:
        val = acronym_match.values[0]
        return val, 100, acronym_match.index[0]

    processed_name = full_process(uploaded_name, force_ascii=True)

    # Name match scores
    standard_names['full_name_similarity'] = standard_names['Name'].apply(
        lambda x: (fuzz.ratio(processed_name, x) if pd.notna(x) else 0)
    )
    full_name_match_idx = standard_names['full_name_similarity'].nlargest(n=1, keep='all').index

    full_name_matches = [
        (row['Name'], row['full_name_similarity'], idx)
        for idx, row in standard_names.iloc[full_name_match_idx].iterrows()
    ]

    # Alias match scores
    standard_names['alias_similarity'] = standard_names['alias'].apply(
        lambda x: (fuzz.ratio(processed_name, x) if pd.notna(x) else 0)
    )
    alias_match_idx = standard_names['alias_similarity'].nlargest(n=1, keep='all').index

    # Looks weird to use row['name'] for alias
    # but we want to return the name in the end
    # We are comparing the correct similarity though.
    alias_matches = [
        (row['Name'], row['alias_similarity'], idx)
        for idx, row in standard_names.iloc[alias_match_idx].iterrows()
    ]

    # The tuples - alias_match and full_name_match have three values -
    # (Name Matched, Confidence and Index Number in the standard list)
    # We are here comparing confidence between the full name match and the alias match
    # and returing the one with greater confidence.

    if len(alias_matches) == 0 or len(full_name_matches) == 0:
        print("No match for input name in our database")
        return ()

    # Since, the aim is to return standard names,
    # in case of an alias value name with higher confidence, we return the corresponding full name

    # TODO: This is only returning the FIRST match. What if there are two
    #  names with the same score?

    if len(alias_matches) == 0 or alias_matches[0][1] <= full_name_matches[0][1]:
        return full_name_matches[0]
    else:
        return alias_matches[0]



def standardise_list(file, column_name_to_standardise, column_entity_type):
    t1 = time.time()
    uploaded_data = pd.read_csv(file)

    if column_name_to_standardise not in uploaded_data.columns:
        print(f"No column {column_name_to_standardise} in Uploaded Data")
        return pd.DataFrame()

    print(f'Generating suggestions for {column_name_to_standardise}')
    uploaded_names = uploaded_data[column_name_to_standardise].dropna().unique()

    standard_names = None
    if column_entity_type == 'affiliation':
        # Initialises list of universities
        standard_names = initialise_standard_univ_list()
    else:
        print('Column Type not supported')
        return pd.DataFrame()

    # Processes list of universities
    for column in ['Name', 'alias']:
        standard_names[column] = standard_names[column].apply(
            lambda x: full_process(x, force_ascii=True)
        )

    matched_names = [standardise_name(uploaded_name, standard_names)
                     for uploaded_name in tqdm(uploaded_names)]

    matched_names_df = convert_to_data_frame(matched_names, uploaded_names)
    matched_names_df['Correct (1/0)'] = pd.Series()
    # The above column has to be manually filled in by the reviewer
    matched_names_df.to_csv(f'{column_name_to_standardise}Suggestions.csv')
    print(f'Suggestions for {column_name_to_standardise} written into {column_name_to_standardise}Suggestions.csv')
    print(f"Total time taken for Fuzzy Matching - {time.time() - t1} seconds")
    return matched_names_df


# This is for independent usage of the standardiser and for a custom standardising process
def generic_standardiser(uploaded_list, standard_list):
        uploaded_list = pd.read_csv(uploaded_list)
        standard_list = pd.read_csv(standard_list)
        processed_names = [full_process(name, force_ascii=True) for name in uploaded_list]
        suggestions = [standard_list.apply(
        lambda x: (fuzz.ratio(processed_name, x) if pd.notna(x) else 0))
        for processed_name in processed_names]

        print(suggestions)



if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('path_to_file_to_standardise')
    parser.add_argument("path_to_standard_file")
    args = parser.parse_args()

    if(len(args) != 2):
        print('Enter path of file to standardise and path to file containing the standard names')    
    generic_standardiser(args.path_to_file_to_standardise, args.path_to_standard_file)
    
