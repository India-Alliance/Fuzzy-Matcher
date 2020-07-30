from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd
import time
from initialise_standard_univ_list import initialise_standard_univ_list
from convert_to_data_frame import convert_to_data_frame

def get_standard_univs_names():
	standard_univs = initialise_standard_univ_list()
	return standard_univs['Name']

def standardiseName(uploaded_name):
	standard_univs_names = get_standard_univs_names()
	matched_names=process.extract(uploaded_name, standard_univs_names)
	return convert_to_data_frame(matched_names, uploaded_name)

def standardiseList(file):
	uploaded_data = pd.read_csv(file)
	uploaded_names = uploaded_data['name']
	print(uploaded_names)
	standard_univs_names = get_standard_univs_names()
	matched_names = [process.extractOne(uploaded_name, standard_univs_names)
					for uploaded_name in uploaded_names]
	return convert_to_data_frame(matched_names, uploaded_names)
