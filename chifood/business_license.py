'''
'''

import json
import requests
import os
import csv
import re
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import fast_food

url ='https://data.cityofchicago.org/resource/uupf-x98q.json?token=5862xfk4f1uhlxqaas83frytd&license_code=1006'
api_key = "5862xfk4f1uhlxqaas83frytd"

def read_request(url):
    '''
    '''

    r = requests.get(url)
    if r is not None:
        files = r.json()
        df = pd.DataFrame.from_dict(files)

    return df

path = ""
website = "https://en.wikipedia.org/wiki/List_of_fast_food_restaurant_chains"
csv_file = "Business_Licenses_-_Current_Active.csv"

def read_data(csv_file):
    # script_dir = os.getcwd()
    full_path = "data/{}".format(csv_file)
    #full_path = os.path.expanduser('~/data/csv_file')
    data1 = pd.read_csv(full_path)

    return data1

def clean_bus(csv_file):
    data = read_data(csv_file)
    name_zip = data[["LEGAL NAME", "DOING BUSINESS AS NAME", "ZIP CODE", "LOCATION"]]
    name_zip = name_zip.apply(lambda x: x.astype(str).str.upper())
    name_zip[["NAME", "extra"]] = name_zip["DOING BUSINESS AS NAME"].str.split("#", expand=True)
    name_zip = name_zip.replace({"KENTUCKY FRIED CHICKEN": "KFC"}, regex = TRUE)
    df = name_zip.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    return df

def read_in_ff(website):
    ff = fast_food.read_in(website)
    fast_food_list = fast_food.scrape(ff)
    df_ff = pd.DataFrame(fast_food_list,columns=['FF_NAME'])
    extra = {"FF_NAME": ["HAROLDS CHICKEN SHACK", "LITTLE CAESAR PIZZA"]}
    df_extra = pd.DataFrame(extra)
    df = pd.concat([df_ff,df_extra], ignore_index = True)
    df.reset_index()
    return df
    
def fuzzy_match_names(df_1, df_2, key1, key2, threshold = 85, limit = 2):
    s = df_2[key2].tolist()
    
    m = df_1[key1].apply(lambda x: process.extract(x, s, limit=limit))    
    df_1['matches'] = m
    
    m2 = df_1['matches'].apply(lambda x: ', '.join([i[0] for i in x if i[1] >= threshold]))
    df_1['matches'] = m2
    fast_food_match = df_1[df_1["matches"].astype(bool)]
    
    return fast_food_match





