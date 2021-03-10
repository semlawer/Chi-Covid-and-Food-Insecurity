


import pandas as pd
import numpy as np
import csv
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.impute import SimpleImputer

def read_in(datas):
    intro = "data/{}.csv".format(datas)
    print(intro)
    df = pd.read_csv(intro)
    return df

def clean_food(food_swamp):
    food_swamp = food_swamp[food_swamp["zip"] != "NAN"]
    food_swamp["ratio"] = (food_swamp["Chains"] + food_swamp["Fast Food"])/(
        food_swamp["grocery_store"]+1)
    food = food_swamp.rename(columns={"zip":"zipcode"})
    food.drop(["Unnamed: 0"], axis = 1, inplace=True)
    food = food.astype({"zipcode":int})
    return food


def regression(food, acs, covid):
    #print("food", food.shape, "acs", acs.shape, "covid", covid.shape)
    merge = acs.merge(food, on="zipcode", how="inner")
    #print(merge)

    X = merge[["percent_black", "perc_hispanic" , "perc_unemployed", "perc_poverty",
        "perc_homeowners", "median_income"]]
    y = merge["ratio"]
    reg = LinearRegression().fit(X, y)
    predict_food = reg.predict(X)
    score = reg.score(X,y)
    merge["pr_food"] = predict_food
    merge_full = merge.merge(food, on =["zipcode", "Chains", "Fast Food", "grocery_store", "ratio"], how="outer")
    print(merge_full.shape)
    merge_full = merge_full.merge(covid, on="zipcode", how="outer")
    print(merge_full.shape)
    return merge_full

def model(food_swamp_data, acs_data, covid_data):
    food_swamp = read_in(food_swamp_data)
    acs = read_in(acs_data)
    covid = read_in(covid_data)
    covid = covid.rename(columns={"zip_code":"zipcode"})
    food = clean_food(food_swamp)
    regress_results = regression(food, acs, covid)
    regress_results.to_csv("data/full_zip.csv")
    return regress_results
