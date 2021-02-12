'''
'''

import json
import requests
import pandas as pd

url ='https://data.cityofchicago.org/resource/yhhz-zm2v.json'

def get_request(url):
    '''
    '''

    try:
        r = requests.get(url)
        if r.status_code == 404 or r.status_code == 403:
            r = None
    except Exception:
        r = None

    return r


def read_request(r):
    '''
    '''

    df = None

    if r is not None:
        files = r.json()
        df = pd.DataFrame.from_dict(files)

    return df
