'''
CS122 Group Project: COVID-19 and Food Insecurity in Chicago
Authors: Valeria Balza, Gabriela Palacios, Sophia Mlawer and Mariel Wiechers
Contact: Sophia Mlawer

This module compares the healthy versus unhealthy food options in Chicago
by ZIP code
'''

import csv
import pandas as pd
import numpy as np
import fast_food
import business_license
import grocery_store


WEBSITE = "https://en.wikipedia.org/wiki/List_of_fast_food_restaurant_chains"
CSV_FILE = "input_data/business_licenses.csv"

def clean_food(food_swamp):
    """
    This function cleans the food data and standardizes it. Creates the ratio
    of unhealthy to healthy food.
    """
    food_swamp = food_swamp[food_swamp["zip"] != "NAN"]
    food_swamp["fs_ratio"] = (food_swamp["Chains"] + food_swamp["Fast Food"]+1)/(
        food_swamp["grocery_store"]+1)
    food = food_swamp.rename(columns={"zip":"zipcode"})
    food = food.astype({"zipcode":int})
    return food

def go():
    '''
    This function combines all the sources of food data together
    and outputs a single CSV of the food measures by zip code.
    '''

    grocery = grocery_store.grocery_store()
    unhealthy_food = business_license.business_license(WEBSITE, CSV_FILE)
    groc = grocery.to_frame().reset_index()
    groc = groc.rename(columns={"index":"zip"})
    merge = unhealthy_food.merge(groc, on="zip", how="outer")
    merge = merge.fillna(0)
    full_food = clean_food(merge)
    full_food.to_csv("output_data/food_swamp_zip.csv")

    return merge