'''
This module collects City of Chicago data from the City of Chicago
Data Portal API

Valeria Balza, Gabriela Palacios, Sophia Mlwawer and Mariel Wiechers
'''

import requests
import json
import pandas as pd

OUTPUT_FILENAME = 'data/covid_data.csv'
DATA_URL = 'https://data.cityofchicago.org/resource/yhhz-zm2v.json' + '?'
APP_TOKEN = 'LVyOCrPCoUZBEPkMulznMLC3Y'
COLS = {'zip_code': str, 'week_number': int, 'death_rate_cumulative': float}


def go(output_filename=OUTPUT_FILENAME):
    '''
    Writes csv file of COVID-19 death rate data
        at the zip code level
    '''

    api_request = build_request()
    covid_json = get_request(api_request)
    covid_df = process_data(covid_json)

    covid_df.to_csv(output_filename, index=False)


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
    covid_json = r.json()

    return covid_json


def process_data(covid_json):
    '''
    Returns a processed pandas dataframe
    '''

    raw = pd.DataFrame.from_dict(covid_json)
    raw['week_number'] = raw['week_number'].astype(int)
    latest_week = raw.week_number.max()

    df = raw[raw['week_number']==latest_week].fillna(0).astype(COLS)
    df = df[['zip_code', 'death_rate_cumulative']].drop(df[df['zip_code']=='Unknown'].index)

    return df
