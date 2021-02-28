import numpy as np
import pandas as pd
import os
import re
from sqlalchemy import create_engine
import sqlite3

def read_and_clean_data(csv_file):
    '''
    '''
    if not os.path.exists(csv_file):
        return None
    all_data = pd.read_csv(csv_file, header = 1, low_memory = False)
    df = all_data[all_data.columns.difference(all_data.filter(like='Margin of Error', axis = 1))]
    cols = list(df.columns)
    for i, col in enumerate(cols):
        cols[i] = re.sub('Estimate!!','',col)
    df.columns = cols
    
    return df

def city_zips(csv_file):
    '''
    Dataframe of all chicago ZIP codes mapped to ZCTAs
    '''
    zips = pd.read_csv(csv_file)
    chicago = zips.loc[:,'PO_NAME'] == 'Chicago'
    zips_chicago = zips[chicago]

    return zips_chicago

def summarize_employment(csv_file):
    build = ['ZCTA','% Unemployment rate', 'Median household income', '% Poverty']

    #income = employ.filter(regex = re.compile(r'median household income', re.IGNORECASE))

    extract = ['Geographic Area Name',
                'Percent!!EMPLOYMENT STATUS!!Civilian labor force!!Unemployment Rate',
                'INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!Median household income (dollars)',
                'Percent!!PERCENTAGE OF FAMILIES AND PEOPLE WHOSE INCOME IN THE PAST 12 MONTHS IS BELOW THE POVERTY LEVEL!!All families']

    employ = read_and_clean_data(csv_file)
    employ = employ.loc[:,extract]
    employ.columns = build
    employ = employ.set_index('ZCTA')

    return employ


def summarize_demographics(csv_file):
    '''
    '''
    build = ['ZCTA','Total population', '% Female', '% Black or African American',
            '% Hispanic or Latino (of any race)']

    extract = ['Geographic Area Name','SEX AND AGE!!Total population', 
                'SEX AND AGE!!Total population!!Female',
                'RACE!!Total population!!One race!!Black or African American',
                'HISPANIC OR LATINO AND RACE!!Total population!!Hispanic or Latino (of any race)']
    
    demo = read_and_clean_data(csv_file)
    demo = demo.loc[:,extract]
    demo.columns = build

    for i, col in enumerate(demo.columns):
        if i > 1:
            demo[build[i]] = 100*demo.loc[:,col]/demo.iloc[:,1]
    demo = demo.set_index('ZCTA')

    return demo

def summarize_household(csv_file):
    '''
    '''
    build = ['ZCTA','% Homeowners']

    extract = ['Geographic Area Name',
            'Percent!!HOUSING TENURE!!Occupied housing units!!Owner-occupied']

    homes = read_and_clean_data(csv_file)
    homes = homes.loc[:,extract]
    homes.columns = build
    homes = homes.set_index('ZCTA')

    return homes


def create_acs_data(csv_demographics, csv_employment, csv_homes, csv_zips):
    '''
    Join all on ZCTA
    '''

    demo = summarize_demographics(csv_demographics)
    employ = summarize_employment(csv_employment)
    homes = summarize_household(csv_homes)
    zips = city_zips(csv_zips)

    acs_sub = pd.merge(demo, employ, how = 'inner', on = 'ZCTA')
    acs = pd.merge(acs_sub, homes, how = 'inner', on = 'ZCTA')
    acs.index = acs.index.str[6:]

    for zcta in acs.index:
        if zcta in zips.values:
            zip_c = zips.loc[zips['ZCTA'] == zcta, 'ZIP_CODE']
            zcta = zip_c 
        else: 
            acs.drop(index = zcta, axis = 0, inplace = True)

    acs.index.rename('ZIP', inplace = True)

    acs.to_csv('acs_data.csv')
    
    engine = create_engine('sqlite://acs_data.sqlite3', echo = False)
    connection = engine.connect()

    acs.to_sql('acs', con = engine, index = True)

    return acs




    




    