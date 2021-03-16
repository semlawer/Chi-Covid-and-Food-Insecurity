
import csv
import pandas as pd
import numpy as np
import fast_food
import business_license
import grocery_store


DATA_URL = 'https://data.cityofchicago.org/resource/3e26-zek2.json' + '?'
APP_TOKEN = 'z5KjXAXxTTp4GoA5lWxfrIMQx'
COLS = {'store_name': str, 'address': str, 'zip': str, 
        'new_status': str, 'last_updated': str,
        'location': str}
WEBSITE = "https://en.wikipedia.org/wiki/List_of_fast_food_restaurant_chains"
CSV_FILE = "Business_Licenses_-_Current_Active.csv"

# def read_load():
#     grocery_store = grocery_store.grocery_store(DATA_URL, APP_TOKEN, COLS)
#     unhealthy_food = business_license.business_license(WEBSITE, CSV_FILE)


def food_swamp():
    print(CSV_FILE)
    grocery = grocery_store.grocery_store(DATA_URL, APP_TOKEN)
    unhealthy_food = business_license.business_license(WEBSITE, CSV_FILE)
    groc = grocery.to_frame().reset_index()
    groc = groc.rename(columns={"index":"zip"})
    merge = unhealthy_food.merge(groc, on="zip", how="outer")
    merge = merge.fillna(0)
    merge.to_csv("data/food_swamp_zip.csv")

    return merge