from fuzzywuzzy import process
import pandas as pd
import time
from matcher.initialise_standard_univ_list import initialise_standard_univ_list
from matcher.convert_to_data_frame import convert_to_data_frame
from tqdm import tqdm


def get_standard_univs_names():
    standard_univs = initialise_standard_univ_list()
    return standard_univs['Name']


def standardise_name(uploaded_name):
    standard_univs = initialise_standard_univ_list()
    standard_univs_names = standard_univs['Name']

    acronym_match = pd.DataFrame(standard_univs.loc[standard_univs['acronym']
                                == uploaded_name, 'Name'])
    if not acronym_match.empty:
        return acronym_match

    return process.extractOne(uploaded_name, standard_univs_names)


def standardise_list(file, column_name_to_standardise='uploaded_names'):
    t1 = time.time()
    uploaded_data = pd.read_csv(file)

    if column_name_to_standardise not in uploaded_data.columns:
        print(f"No column {column_name_to_standardise} in Uploaded Data")
        return pd.DataFrame()

    uploaded_names = uploaded_data[column_name_to_standardise].dropna().unique()
    matched_names = [standardise_name(uploaded_name)
                     for uploaded_name in tqdm(uploaded_names)]

    matched_names_df = convert_to_data_frame(matched_names, uploaded_names)
    matched_names_df['Correct (True/False)'] = pd.Series()
    # The above column has to be manually filled in by the reviewer
    matched_names_df.to_csv('Suggestions.csv')
    print(f"Total time taken for operation - {time.time() - t1}")
    return matched_names_df
