'''
https://stackoverflow.com/questions/13636848/is-it-possible-to-do-fuzzy-match-merge-with-python-pandas
'''

import json
import requests
import os
import csv
import re
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import fast_food


path = ""
# website = "https://en.wikipedia.org/wiki/List_of_fast_food_restaurant_chains"
# csv_file = "Business_Licenses_-_Current_Active.csv"

def read_data(csv_file):
    # script_dir = os.getcwd()
    full_path = "data/{}".format(csv_file)
    #full_path = os.path.expanduser('~/data/csv_file')
    data1 = pd.read_csv(full_path)

    return data1

def clean_bus(csv_file):
    data = read_data(csv_file)
    name_zip = data[["LEGAL NAME", "DOING BUSINESS AS NAME", "ZIP CODE", "LOCATION"]]
    name_zip = name_zip.apply(lambda x: x.astype(str).str.upper())
    name_zip[["NAME", "extra"]] = name_zip["DOING BUSINESS AS NAME"].str.split("#", expand=True)
    name_zip = name_zip.replace({"KENTUCKY FRIED CHICKEN": "KFC"}, regex = True)
    df = name_zip.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    return df

def dollar_chains():
    list_dollar = ["WALGREENS", "CVS", "7 ELEVEN", "DOLLAR TREE", "FAMILY DOLLAR", "DOLLAR GENERAL"]
    dollar_df = pd.DataFrame(list_dollar, columns = ["FF_NAME"])
    dollar_df["type"] = "Chains"
    return dollar_df


def read_in_ff(website):
    ff = fast_food.read_in(website)
    fast_food_list = fast_food.scrape(ff)
    df_ff = pd.DataFrame(fast_food_list, columns=['FF_NAME'])
    extra = {"FF_NAME": ["HAROLDS CHICKEN SHACK", "LITTLE CAESAR PIZZA", "CHURCHS CHICKEN"]}
    df_extra = pd.DataFrame(extra)
    df = pd.concat([df_ff,df_extra], ignore_index = True)
    df.reset_index()
    df["type"] = "Fast Food"
    dollar_df = dollar_chains()
    df.append(dollar_df)
    return df


def fuzzy_match_names(df_1, df_2, key1, key2, threshold, limit):
    s = df_2[key2].tolist()
    m = df_1[key1].apply(lambda x: process.extract(x, s, limit=limit))    
    df_1['matches'] = m
    m2 = df_1['matches'].apply(lambda x: ', '.join([i[0] for i in x if i[1] >= threshold]))
    df_1['matches'] = m2
    fast_food_match = df_1[df_1["matches"].astype(bool)]
    merge = fast_food_match.merge(ff, left_on="matches", right_on=key2)
    return merge


def ff_by_zip(df):
    '''
    Collapses data by zip code and returns
    '''
    #df["ZIP CODE"] = df.groupby("type")["ZIP CODE"].astype("string")
    df[["zip_code", "zip_extra"]] = df["zip"].str.split(".", expand=True)
    collapse = df["zip_code"].value_counts().unstack(level = 0)
    collapse.name = "fast_food"
    return collapse


def business_license(website, csv_file):
    data = read_data(csv)
    df = clean_bus(data)
    ff = read_in_ff(website)
    merge = fuzzy_match_names(df, ff, "NAME", "FF_NAME", 90, 2)
    by_zip = ff_by_zip(merge)
    return by_zip
