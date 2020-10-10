import pandas as pd
import os.path


def initialise_standard_univ_list():
    path = 'https://raw.githubusercontent.com/MaximumEndurance/'
    sub_path = 'Fuzzy-Matcher/master/GridUnivsData/'
    # path and sub_path declared to match max line length rule which
    # was breaking because of the length of the URL string
    all_univs = None
    acronyms = None

    if not os.path.exists('data/GridUnivsData/grid.csv'):
        all_univs = pd.read_csv(f"{path}{sub_path}grid.csv")
        print("Fetch from remote Grid")
    else:
        all_univs = pd.read_csv('data/GridUnivsData/grid.csv')
    # Using acronyms to make the fuzzy matcher acronym sensitive as well
    if not os.path.exists('data/GridUnivsData/acronyms.csv'):
        acronyms = pd.read_csv(f"{path}{sub_path}acronyms.csv")
        print("Fetch from remote Acronym")

    standard_and_alias_univ_names = pd.merge(all_univs, aliases, on='ID', how='left')

    acronyms = acronyms.rename(columns={"grid_id": "ID"})

    return pd.merge(standard_and_alias_univ_names, acronyms, on='ID', how='left')
