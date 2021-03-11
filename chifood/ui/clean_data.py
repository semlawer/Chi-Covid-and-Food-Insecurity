'''
Turn csv into an sqlite3 database
'''

import pandas as pd
from sqlalchemy import create_engine

input_filename = 'full_zip.csv'
output_filename = 'data'

def convert(input_filename):
    '''
    Saves pandas df to .sqlite3
    '''

    data = clean_colnames(input_filename)
    engine = create_engine('sqlite:///chifood.sqlite3', echo=True)
    sqlite_connection = engine.connect()
    data.to_sql(output_filename, sqlite_connection)
    sqlite_connection.close()


def clean_colnames(input_filename):
    '''
    '''

    data = pd.read_csv('full_zip.csv')
    
    data = data.drop(['Unnamed: 0', 'perc_female', 'perc_homeowners',
                      'Chains', 'Fast Food', 'grocery_store'], axis=1).round(2)
    data.columns = ['zipcode', 'total_pop', 'perc_black', 'perc_hisp',
                    'perc_unempl', 'median_income', 'perc_poverty',
                    'fs_ratio', 'pr_food_ins', 'death_rate_cumulative']

    return data
