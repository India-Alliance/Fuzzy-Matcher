import pandas as pd


def initialise_standard_univ_list():
    path = 'https://raw.githubusercontent.com/MaximumEndurance/'
    sub_path = 'Fuzzy-Matcher/master/GridUnivsData/'
    # path and sub_path declared to match max line length rule which
    # was breaking because of the length of the URL string

    all_univs = pd.read_csv(f"{path}{sub_path}grid.csv")

    # Using acronyms to make the fuzzy matcher acronym sensitive as well
    acronyms = pd.read_csv(f"{path}{sub_path}acronyms.csv")
    acronyms.head()
    acronyms = acronyms.rename(columns={"grid_id": "ID"})

    return pd.merge(all_univs, acronyms, on='ID')
