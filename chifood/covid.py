'''
'''

import requests
import json
import pandas as pd

DATA_URL = 'https://data.cityofchicago.org/resource/yhhz-zm2v.json' + '?'
APP_TOKEN = 'LVyOCrPCoUZBEPkMulznMLC3Y'
COLS = ['zip_code', 'week_number', 'cases_cumulative', 
        'tests_cumulative', 'deaths_cumulative', 'death_rate_cumulative', 
        'population', 'zip_code_location']


def build_request(data_url=DATA_URL, app_token=APP_TOKEN, limit=5000, select=COLS):
    '''
    '''

    api_request = DATA_URL
    api_request += '$limit=' + str(limit) + '&'
    api_request += '$$app_token={}'.format(app_token)
    api_request += "&$select={}".format(", ".join(COLS))

    return api_request


def get_request(api_request):
    '''
    '''

    r = requests.get(api_request)
    covid_data = r.json()

    return covid_data


def process_data(covid_data):
    '''
    '''

    df = pd.DataFrame.from_dict(covid_data)
    latest_week = df.week_number.max()
    filter = df['week_number']==latest_week
    df['deaths_cumulative'] = df['deaths_cumulative'].astype(int)
    df['cases_cumulative'] = df['cases_cumulative'].fillna(0)
    df['cases_cumulative'] = df['cases_cumulative'].astype(int)

    return df[filter]





