'''
CS122 Group Project: COVID-19 and Food Insecurity in Chicago
Authors: Valeria Balza, Gabriela Palacios, Sophia Mlawer and Mariel Wiechers
Contact: Sophia Mlawer

This module compares fast food restaurants in Chicago to national chains. Please 
note part of this module was inspired by:
    https://stackoverflow.com/questions/13636848/is-it-possible-to-do-fuzzy-match-merge-with-python-pandas
'''

import json
import requests
import os
import re
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import fast_food


def read_data(csv_file):
    '''
    Reads csv file and outputs a CSV
    '''

    data = pd.read_csv(csv_file)

    return data


def clean_bus(data):
    '''
    Cleans the data and standardizes format
    '''

    name_zip = data[["LEGAL NAME", "DOING BUSINESS AS NAME", "ZIP CODE", "LOCATION"]]
    name_zip = name_zip.apply(lambda x: x.astype(str).str.upper())
    name_zip[["NAME", "extra"]] = name_zip["DOING BUSINESS AS NAME"].str.split("#", expand=True)
    name_zip = name_zip.replace({"KENTUCKY FRIED CHICKEN": "KFC"}, regex = True)
    df = name_zip.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    return df

def dollar_chains():
    '''
    This creates a list of the main variety stores where residents
    buy food that are traditionally cheaper, unhealthier, and with less options
    than a grocery store.
    '''

    list_dollar = ["WALGREENS", "CVS", "7 ELEVEN", "DOLLAR TREE", "FAMILY DOLLAR", "DOLLAR GENERAL"]
    dollar_df = pd.DataFrame(list_dollar, columns = ["FF_NAME"])
    dollar_df["type"] = "Chains"

    return dollar_df


def read_in_ff(website):
    '''
    Performs the fast_food.py web scraping, cleans the data, and combines it
    with the list of chain variety stores.
    '''

    ff = fast_food.read_in(website)
    fast_food_list = fast_food.scrape(ff)
    df_ff = pd.DataFrame(fast_food_list, columns=['FF_NAME'])
    extra = {"FF_NAME": ["HAROLDS CHICKEN SHACK", "LITTLE CAESAR PIZZA", "CHURCHS CHICKEN"]}
    df_extra = pd.DataFrame(extra)
    df = pd.concat([df_ff,df_extra], ignore_index = True)
    df.reset_index()
    df["type"] = "Fast Food"
    dollar_df = dollar_chains()
    frames = [df, dollar_df]
    df_full = pd.concat(frames)

    return df_full


def fuzzy_match_names(df_1, df_2, key1, key2, threshold, limit):
    '''
    Merges the business license food store names with the list of fast food
    restaurants and performs a fuzzy match between the two. If the match chance
    is higher than the set threshold, then it is considered a name match.
    Keeps only the business license information for the records that match.
    '''

    s = df_2[key2].tolist()
    m = df_1[key1].apply(lambda x: process.extract(x, s, limit=limit))    
    df_1['matches'] = m
    m2 = df_1['matches'].apply(lambda x: ', '.join([i[0] for i in x if i[1] >= 
        threshold]))
    df_1['matches'] = m2
    fast_food_match = df_1[df_1["matches"].astype(bool)]
    merge = fast_food_match.merge(df_2, left_on="matches", right_on=key2)
    output = merge[["LEGAL NAME", "DOING BUSINESS AS NAME", "ZIP CODE", "LOCATION", "matches", "type"]]
    output.rename({"ZIP CODE":"ZIP"}, inplace =True)
    output.columns = output.columns.str.lower()
    output.to_csv("output_data/unhealthy_food.csv")

    return merge


def ff_by_zip(df):
    '''
    Collapses data by zip code and returns
    '''

    df[["zip", "zip_extra"]] = df["ZIP CODE"].str.split(".", expand=True)
    collapse = df.groupby("type")["zip"].value_counts().unstack(level = 0)
    collapse.name = "fast_food"
    return collapse


def business_license(website, csv_file):
    '''
    Runs the above functions in the proper order
    '''

    data = read_data(csv_file)
    df = clean_bus(data)
    ff = read_in_ff(website)
    merge = fuzzy_match_names(df, ff, "NAME", "FF_NAME", 90, 2)
    by_zip = ff_by_zip(merge)

    return by_zip
