from fuzzywuzzy import process, fuzz
from fuzzywuzzy.utils import full_process
import pandas as pd
import time
from matcher.initialise_standard_univ_list import initialise_standard_univ_list
from matcher.convert_to_data_frame import convert_to_data_frame
from tqdm import tqdm


def get_standard_univs_names():
    standard_univs = initialise_standard_univ_list()
    return standard_univs['Name']


def standardise_name(uploaded_name, standard_univs):
    acronym_match = standard_univs.loc[
        standard_univs['acronym'] == uploaded_name, 'Name'
    ]

    if not acronym_match.empty:
        val = acronym_match.values[0]
        return val, 100, acronym_match.index[0]

    processed_name = full_process(uploaded_name, force_ascii=True)


    # Name match scores
    standard_univs['full_name_similarity'] = standard_univs['Name'].apply(
        lambda x: fuzz.ratio(processed_name, x)
    )
    full_name_match_idx = standard_univs['full_name_similarity'].nlargest(n=1, keep='all').index

    full_name_matches = [
        (row['Name'], row['full_name_similarity'], idx)
        for idx, row in standard_univs.iloc[full_name_match_idx].iterrows()
    ]

    # Alias match scores
    standard_univs['alias_similarity'] = standard_univs['alias'].apply(
        lambda x: fuzz.ratio(processed_name, x)
    )
    alias_match_idx = standard_univs['alias_similarity'].nlargest(n=1, keep='all').index

    # Looks weird to use row['name'] for alias
    # but we want to return the name in the end
    # We are comparing the correct similarity though.
    alias_matches = [
        (row['Name'], row['alias_similarity'], idx)
        for idx, row in standard_univs.iloc[alias_match_idx].iterrows()
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

    print(alias_matches)
    print(full_name_matches)

    if len(alias_matches) == 0 or alias_matches[0][1] <= full_name_matches[0][1]:
        return full_name_matches[0]
    else:
        return alias_matches[0]


def standardise_list(file, column_name_to_standardise='uploaded_names'):
    t1 = time.time()
    uploaded_data = pd.read_csv(file)

    if column_name_to_standardise not in uploaded_data.columns:
        print(f"No column {column_name_to_standardise} in Uploaded Data")
        return pd.DataFrame()

    uploaded_names = uploaded_data[column_name_to_standardise].dropna().unique()

    # Initialises list of universities
    standard_univs = initialise_standard_univ_list()
    # Processes list of universities
    for column in ['Name', 'alias']:
        standard_univs[column] = standard_univs[column].apply(
            lambda x: full_process(x, force_ascii=True)
        )

    matched_names = [standardise_name(uploaded_name, standard_univs)
                     for uploaded_name in tqdm(uploaded_names)]

    matched_names_df = convert_to_data_frame(matched_names, uploaded_names)
    matched_names_df['Correct (1/0)'] = pd.Series()
    # The above column has to be manually filled in by the reviewer
    matched_names_df.to_csv('Suggestions.csv')
    print(f"Total time taken for Fuzzy Matching - {time.time() - t1} seconds")
    return matched_names_df
