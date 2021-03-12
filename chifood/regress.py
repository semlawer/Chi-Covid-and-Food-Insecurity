


import pandas as pd
import numpy as np
import csv
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.impute import SimpleImputer

def read_in(datas):
    intro = "{}.csv".format(datas)
    df = pd.read_csv(intro)
    return df

def clean_food(food_swamp):
    food_swamp = food_swamp[food_swamp["zip"] != "NAN"]
    food_swamp["fs_ratio"] = (food_swamp["Chains"] + food_swamp["Fast Food"]+1)/(
        food_swamp["grocery_store"]+1)
    food = food_swamp.rename(columns={"zip":"zipcode"})
    food = food.drop(["Unnamed: 0"], axis = 1)
    food = food.astype({"zipcode":int})
    return food


def regression(food, acs, covid):
    merge = acs.merge(food, on="zipcode", how="inner")
    X = merge[["perc_black", "perc_hispanic" , "perc_unemployed", "perc_poverty",
        "perc_homeowners", "median_income"]]
    y = merge["fs_ratio"]
    reg = LinearRegression().fit(X, y)
    predict_food = reg.predict(X)
    print(merge.columns)
    score = reg.score(X,y)
    merge["pr_fs_ratio"] = predict_food
    merge_full = merge.merge(food, on =["zipcode", "Chains", "Fast Food", "grocery_store", "fs_ratio"], how="outer")
    merge_full = merge_full.merge(covid, on="zipcode", how="outer").round(2)
    return merge_full


def model(food_swamp_data, acs_data, covid_data):
    food_swamp = read_in(food_swamp_data)
    acs = read_in(acs_data)
    covid = read_in(covid_data)
    covid = covid.rename(columns={"zip_code":"zipcode"})
    food = clean_food(food_swamp)
    regress_results = regression(food, acs, covid)
    regress_results = regress_results.rename(columns={"perc_non_white":"perc_minority"})
    map_data = regress_results[['zipcode', 'fs_ratio', 'pr_fs_ratio', 
            'death_rate_cumulative']]
    table_data = regress_results[['zipcode', 'total_population', 'perc_black',
            'perc_minority','perc_hispanic','perc_unemployed', 'median_income',
            'perc_poverty','fs_ratio', 'pr_fs_ratio', 'death_rate_cumulative']]
    regress_results.to_csv("data/full_zip.csv")
    return table_data, map_data
