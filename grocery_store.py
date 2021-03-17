'''
CS122 Group Project: COVID-19 and Food Insecurity in Chicago
Authors: Valeria Balza, Gabriela Palacios, Sophia Mlawer and Mariel Wiechers
Contact: Sophia Mlawer

This module retrieves data from the City of Chicago Data Portal on the
active grocery stores in Chicago using an API
'''

import requests
import json
import pandas as pd

DATA_URL = 'https://data.cityofchicago.org/resource/3e26-zek2.json' + '?'
APP_TOKEN = 'z5KjXAXxTTp4GoA5lWxfrIMQx'
COLS = {'store_name': str, 'address': str, 'zip': str, 
        'new_status': str, 'last_updated': str,
        'location': str}


def build_request(data_url=DATA_URL, app_token=APP_TOKEN, limit=10000, select=COLS):
    '''
    Returns string to feed into get_request.
    '''

    api_request = DATA_URL
    api_request += '$limit=' + str(limit) + '&'
    api_request += '$$app_token={}'.format(app_token)
    api_request += "&$select={}".format(", ".join(COLS.keys()))

    return api_request


def get_request(api_request):
    '''
    Returns JSON of Grovery Stores Data by Zip Code.
    '''

    r = requests.get(api_request)
    grocery_data = r.json()

    return grocery_data


def process_data(grocery_data):
    '''
    Returns a processed pandas dataframe
    '''

    raw = pd.DataFrame.from_dict(grocery_data)
    raw.to_csv("output_data/grocery_store.csv")
    return raw


def grocery_by_zip(df):
    '''
    Collapses data by zip code and returns
    '''

    df[["zip_code", "zip_extra"]] = df["zip"].str.split("-", expand=True)
    collapse = df["zip_code"].value_counts()
    collapse.name = "grocery_store"
    return collapse


def grocery_store():
    '''
    Main function that runs the rest of the functions in order
    '''

    build = build_request()
    data = get_request(build)
    df = process_data(data)
    by_zip = grocery_by_zip(df)
    return by_zip