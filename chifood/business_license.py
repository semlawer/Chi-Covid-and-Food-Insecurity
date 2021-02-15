'''
'''

import json
import requests
import os
import csv
import pandas as pd

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

def read_data(csv_file):
    script_dir = os.getcwd()
    full_path = os.path.join(script_dir, 'data/{}'.format(csv_file))
    #full_path = os.path.expanduser('~/data/csv_file')
    data1 = pd.read_csv(full_path)

    return data1

def clean_bus(csv_file):
    data = read_data(csv_file)
    name_zip = data[["LEGAL NAME", "DOING BUSINESS AS NAME", "ZIP CODE", "LOCATION"]]
    name_zip["DOING BUSINESS AS NAME"] = name_zip["DOING BUSINESS AS NAME"].str.upper()
    name_zip["LEGAL NAME"] = name_zip["LEGAL NAME"].str.upper()
    name_zip[["NAME", "extra"]] = name_zip["DOING BUSINESS AS NAME"].str.split("#", expand=True)
    df = name_zip.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    fast_food = fast_food.read_in("https://en.wikipedia.org/wiki/List_of_fast_food_restaurant_chains")
    fast_food_list = fast_food.scrape(fast_food)
    ff_list = pd.DataFrame(np.array(fast_food_list), columns = ["NAME"])
    ff_loc = df.merge(ff_list, on = "NAME", how = "inner")



