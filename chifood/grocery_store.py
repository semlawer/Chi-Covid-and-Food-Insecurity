'''
This module collects City of Chicago data from the City of Chicago
Data Portal API

Valeria Balza, Gabriela Palacios, Sophia Mlwawer and Mariel Wiechers
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
    Returns JSON of COVID-19 Data by Zip Code.
    '''

    r = requests.get(api_request)
    grocery_data = r.json()

    return grocery_data


def process_data(grocery_data):
    '''
    Returns a processed pandas dataframe
    '''
    raw = pd.DataFrame.from_dict(grocery_data)
    return raw


def grocery_by_zip(df):
    '''
    Collapses data by zip code and returns
    '''
    df[["zip_code", "zip_extra"]] = df["zip"].str.split("-", expand=True)
    collapse = df["zip_code"].value_counts()
    collapse.name = "grocery_store"
    return collapse