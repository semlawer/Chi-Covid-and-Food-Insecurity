'''
CS122 Group Project: COVID-19 and Food Insecurity in Chicago
Authors: Valeria Balza, Gabriela Palacios, Sophia Mlawer and Mariel Wiechers
Contact: Mariel Wiechers

This module collects and cleans data from the American Community Survey and
exports the data as one CSV file
'''

import numpy as np
import pandas as pd
import os
import re


def read_and_clean_data(csv_file):
    '''
    Create pandas dataframe from csv file and extracting only columns with data 
    estimates and percentages

    Input: csv_file

    Retuns: df, a clean dataframe to extract desired columns from
    '''

    if not os.path.exists(csv_file):
        return None
    all_data = pd.read_csv(csv_file, header=1, low_memory=False)
    df = all_data[all_data.columns.drop(all_data.filter(like='Margin of Error', axis=1))]
    cols = list(df.columns)
    for i, col in enumerate(cols):
        cols[i] = re.sub('Estimate!!', '', col)
    df.columns = cols
    
    return df


def city_zips(csv_file):
    '''
    Holds data on which zip codes belong to Chicago

    Inputs: csv file with zip code information

    Returns: pandas dataframe with zip to ZCTA for specific city, in this case, Chicago. 
    '''

    zips = pd.read_csv(csv_file)
    chicago = zips.loc[:, 'PO_NAME'] == 'Chicago'
    zips_chicago = zips[chicago]

    return zips_chicago


def summarize_employment(csv_file):
    '''
    Extracts desired data from employment data available from ACS surveys. 

    Inputs:
        csv_file: downloaded from ACS website

    Returns:
        homes: panda dataframe with information extracted from employment data
    '''

    build = ['ZCTA','perc_unemployed', 'median_income', 'perc_poverty']

    extract = ['Geographic Area Name',
                'Percent!!EMPLOYMENT STATUS!!Civilian labor force!!Unemployment Rate',
                'INCOME AND BENEFITS (IN 2019 INFLATION-ADJUSTED DOLLARS)!!Total households!!Median household income (dollars)',
                'Percent!!PERCENTAGE OF FAMILIES AND PEOPLE WHOSE INCOME IN THE PAST 12 MONTHS IS BELOW THE POVERTY LEVEL!!All families']

    employ = read_and_clean_data(csv_file)
    employ = employ.loc[:, extract]
    employ.columns = build
    employ = employ.set_index('ZCTA')

    return employ


def summarize_demographics(csv_file):
    '''
     Extracts desired data from demographic data available from ACS surveys. 

    Inputs:
        csv_file: downloaded from ACS website

    Returns:
        demo: panda dataframe with column data on race and gender.
    '''

    build = ['ZCTA','total_population', 'perc_female', 'perc_non_white', 'perc_black',
            'perc_hispanic']

    extract = ['Geographic Area Name','SEX AND AGE!!Total population', 
                'SEX AND AGE!!Total population!!Female',
                'Race alone or in combination with one or more other races!!Total population!!White',
                'RACE!!Total population!!One race!!Black or African American',
                'HISPANIC OR LATINO AND RACE!!Total population!!Hispanic or Latino (of any race)']
    
    demo = read_and_clean_data(csv_file)
    demo = demo.loc[:, extract]
    demo.columns = build

    for i, col in enumerate(demo.columns):
        if i > 1:
            demo[build[i]] = 100 * demo.loc[:, col]/demo.iloc[:, 1]
    demo = demo.set_index('ZCTA')
    demo['perc_non_white'] = 100 - demo['perc_non_white']

    return demo

def summarize_household(csv_file):
    '''
    Extracts desired data from houshold data available from ACS surveys. 

    Inputs:
        csv_file: downloaded from ACS website

    Returns:
        homes: panda dataframe with information extracted from household data
    '''

    build = ['ZCTA','perc_homeowners']

    extract = ['Geographic Area Name',
            'Percent!!HOUSING TENURE!!Occupied housing units!!Owner-occupied']

    homes = read_and_clean_data(csv_file)
    homes = homes.loc[:, extract]
    homes.columns = build
    homes = homes.set_index('ZCTA')

    return homes


def go(csv_demographic, csv_employment, csv_housing, csv_zips):
    '''
    Join all ACS data on ZCTA. 

    Inputs:
        csv files to extract columns from 

    Outputs:
        dataframe: pandas dataframe for futher analysis
        csv: Creates csv file at location folder
        sql: Creates an sql db for querying
    '''

    demo = summarize_demographics(csv_demographic)
    employ = summarize_employment(csv_employment)
    homes = summarize_household(csv_housing)
    zips = city_zips(csv_zips)

    acs_sub = pd.merge(demo, employ, how='inner', on='ZCTA')
    acs = pd.merge(acs_sub, homes, how='inner', on='ZCTA')
    acs.index = acs.index.str[6: ]

    for zcta in acs.index:
        if zcta in zips.values:
            zip_c = zips.loc[zips['ZCTA']==zcta, 'ZIP_CODE']
            zcta = zip_c 
        else: 
            acs.drop(index=zcta, axis=0, inplace=True)

    acs.index.rename('zipcode', inplace=True)

    acs_csv = acs.to_csv('output_data/acs_data.csv')

