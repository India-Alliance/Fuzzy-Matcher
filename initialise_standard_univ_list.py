import pandas as pd

def initialise_standard_univ_list():
	all_univs = pd.read_csv('https://raw.githubusercontent.com/MaximumEndurance/Fuzzy-Matcher/master/GridUnivsData/grid.csv')

    # Using acronyms to make the fuzzy matcher acronym sensitive as well
	acronyms = pd.read_csv('https://raw.githubusercontent.com/MaximumEndurance/Fuzzy-Matcher/master/GridUnivsData/acronyms.csv')
	acronyms.head()
	acronyms = acronyms.rename(columns={"grid_id": "ID"})

	return pd.merge(all_univs, acronyms, on='ID')

