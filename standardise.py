from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd
import time
from initialise_standard_univ_list import initialise_standard_univ_list
from convert_to_data_frame import convert_to_data_frame

def standardise(uploaded_name):
	t1 = time.time()
	standard_univs = initialise_standard_univ_list()
	standard_univs_names = standard_univs['Name']
	# uploaded_names = ['Cambridge', 'IITB', 'L V Prasad']
	matched_names= process.extractOne(uploaded_name, standard_univs_names)
	return convert_to_data_frame([matched_names], [uploaded_name])
	# print("Total Time taken :", time.time()-t1)
