import pandas as pd
import os.path


def download_file_if_unavailable(path, sub_path, local_path):
    if not os.path.exists(local_path):
        print("Fetching from remote (grid.ac)")
        name_of_file = local_path.split('/')[2]
        return pd.read_csv(f"{path}{sub_path}{name_of_file}")
    else:
        return pd.read_csv(local_path)


def initialise_standard_univ_list():
    path = 'https://raw.githubusercontent.com/MaximumEndurance/'
    sub_path = 'Fuzzy-Matcher/master/GridUnivsData/'
    # path and sub_path declared to match max line length rule which
    # was breaking because of the length of the URL string
    all_univs = None
    acronyms = None

    all_univs = download_file_if_unavailable(path, sub_path, 'data/GridUnivsData/grid.csv')
    acronyms = download_file_if_unavailable(path, sub_path, 'data/GridUnivsData/acronyms.csv')
    aliases = download_file_if_unavailable(path, sub_path, 'data/GridUnivsData/aliases.csv')

    aliases = aliases.rename(columns={"grid_id": "ID"})

    standard_and_alias_univ_names = pd.merge(all_univs, aliases, on='ID', how='outer')

    acronyms = acronyms.rename(columns={"grid_id": "ID"})

    return pd.merge(standard_and_alias_univ_names, acronyms, on='ID', how='outer')
