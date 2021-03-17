'''
CS122 Group Project: COVID-19 and Food Insecurity in Chicago
Authors: Valeria Balza, Gabriela Palacios, Sophia Mlawer and Mariel Wiechers
Contact: Sophia Mlawer

This module combines all the data together and calculates a regression
predicting a food swamp measure given demographic and socioeconomic
variables and returns data table.
'''

import pandas as pd
import numpy as np
import csv
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.impute import SimpleImputer

def read_in(datas):
    '''
    Reads in CSV datasets and outputs as Pandas dataframe
    '''
    intro = "{}.csv".format(datas)
    df = pd.read_csv(intro)
    return df


def regression(food, acs, covid):
    '''
    Merges the ACS socioeconomic factors to the Food measures and performs
    a regression between them. Creates predicted measure of food swamp.
    Adjusts for the fact that some zip codes do not have demographic information.
    '''

    merge = acs.merge(food, on="zipcode", how="inner")
    X = merge[["perc_black", "perc_hispanic" , "perc_unemployed", "perc_poverty",
        "perc_homeowners", "median_income"]]
    y = merge["fs_ratio"]
    reg = LinearRegression().fit(X, y)
    predict_food = reg.predict(X)
    score = reg.score(X,y)
    merge["pr_fs_ratio"] = predict_food
    merge_full = merge.merge(food, on =["zipcode", "Chains", "Fast Food", "grocery_store", "fs_ratio"], how="outer")
    merge_full = merge_full.merge(covid, on="zipcode", how="outer").round(2)

    return merge_full


def model(food_swamp_data, acs_data, covid_data):
    '''
    Preps the data for the Django interface by combining the ACS, Food Swamp,
    and COVID-19 data together. Creates two Pandas dataframes, one for each
    element of the Django interface.
    '''

    food_swamp = read_in(food_swamp_data)
    acs = read_in(acs_data)
    covid = read_in(covid_data)
    covid = covid.rename(columns={"zip_code":"zipcode"})
    regress_results = regression(food_swamp, acs, covid)
    regress_results = regress_results.rename(columns={"perc_non_white":"perc_minority"})

    map_data = regress_results[['zipcode', 'fs_ratio', 'pr_fs_ratio', 
            'death_rate_cumulative']]
    table_data = regress_results[['zipcode', 'total_population', 'perc_black',
            'perc_minority','perc_hispanic','perc_unemployed', 'median_income',
            'perc_poverty','fs_ratio', 'pr_fs_ratio', 'death_rate_cumulative']]

    return table_data, map_data
