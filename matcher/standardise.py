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

    acronym_match = standard_univs.loc[standard_univs['acronym']
                                == uploaded_name, 'Name']
    if not acronym_match.empty:
        print(acronym_match)
        print(type(acronym_match))
        val = acronym_match.values[0]
        return (val, 100, acronym_match.index[0])

    # Alias matches

    alias_match = process.extractOne(uploaded_name, standard_univs['alias'])
    full_name_match = process.extractOne(uploaded_name, standard_univs['Name'])
    print(alias_match)
    print(full_name_match)
    # The tuples - alias_match and full_name_match have three values -
    # (Name Matched, Confidence and Index Number in the standard list)
    # We are here comparing confidence between the full name match and the alias match
    # and returing the one with greater confidence.
    if not alias_match and not full_name_match:
        print("No match for input name in our database")
        return ()
    # Since, the aim is to return standard names,
    # in case of an alias value name with higher confidence, we return the corresponding full name
    if (len(alias_match) == 0 or alias_match[1] <= full_name_match[1]):
        return full_name_match
    else:
        return (standard_univs.at[alias_match[2], 'Name'], alias_match[1], alias_match[2])


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
    matched_names_df['Correct (1/0)'] = pd.Series()
    # The above column has to be manually filled in by the reviewer
    matched_names_df.to_csv('Suggestions.csv')
    print(f"Total time taken for operation - {time.time() - t1}")
    return matched_names_df
