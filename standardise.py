from fuzzywuzzy import process
import pandas as pd
import time
from initialise_standard_univ_list import initialise_standard_univ_list
from convert_to_data_frame import convert_to_data_frame
from tqdm import tqdm


def get_standard_univs_names():
    standard_univs = initialise_standard_univ_list()
    return standard_univs['Name']


def standardiseName(uploaded_name):
    standard_univs = initialise_standard_univ_list()
    standard_univs_names = standard_univs['Name']
    if (len(uploaded_name) < 6 or (
            (uploaded_name.isupper() and len(uploaded_name) < 10))):
        return pd.DataFrame(standard_univs.loc[standard_univs['acronym']
                            == uploaded_name, 'Name'])

    matched_names = process.extract(uploaded_name, standard_univs_names)
    return convert_to_data_frame(matched_names, uploaded_name)


def standardiseList(file):
    t1 = time.time()
    uploaded_data = pd.read_csv(file)
    lead_applicant_organisation = 'Lead Applicant Applicant Organisation'
    uploaded_names = uploaded_data[lead_applicant_organisation].dropna()
    standard_univs_names = get_standard_univs_names()
    uploaded_names = uploaded_names[:100]  # Testing. Remove on production
    matched_names = [process.extractOne(uploaded_name, standard_univs_names)
                     for uploaded_name in tqdm(uploaded_names)]

    matched_names_df = convert_to_data_frame(matched_names, uploaded_names)
    matched_names_df.to_csv('StandardUnivNames.csv')
    print(time.time() - t1)
    return matched_names_df
