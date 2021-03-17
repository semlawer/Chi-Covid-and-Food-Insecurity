'''
CS122 Group Project: COVID-19 and Food Insecurity in Chicago
Authors: Valeria Balza, Gabriela Palacios, Sophia Mlawer and Mariel Wiechers
Contact: Valeria Balza

This module generates two shapefiles for the Django web application: one containing
ZIP code-level data on COVID-19 death rates, food insecurity and demographic indicators;
and another containing the coordinates of food banks. This module also generates
an SQLite database of all the data used for the search engine in the Django web app
'''

import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine

ZIP_BOUNDARIES = 'input_data/zip_bndries/zip_bndries.shp'
BASE_MAP = gpd.read_file(ZIP_BOUNDARIES)


def gen_sqlite(data):
    '''
    Creates a SQLite database from a pandas dataframe

    Inputs: pandas df
    Returns: None
    '''

    engine = create_engine('sqlite:///CS_covid_food/chifood.sqlite3', echo=False)
    sqlite_connection = engine.connect()
    data.to_sql('data', sqlite_connection)
    sqlite_connection.close()


def gen_shapefiles(map_data, food_banks_df, base_map=BASE_MAP):
    '''
    Creates two shapefiles. One contains data of COVID-19
    death rates and food insecurity by zip code. The other contains
    the food bank locations.

    Inputs:
        - map_data (df): pandas dataframe containing the data 
        use to create Django map layers
        - food_banks_df: pandas dataframe containing the data for the
        locations of food banks
        - base_map: geopandas dataframe containing zip code layer
    '''

    map_data.columns = ["zip", "fs_ratio", "pr_fs_ratio", "death_rate"]
    base_map = base_map.astype({"zip": 'int64'})
    covid_food = base_map.merge(map_data[["zip", "fs_ratio", "pr_fs_ratio", "death_rate"]],
                               how="inner", on="zip")
    covid_food.to_file("CS_covid_food/map_query/data/covid_food.shp")
    
    food_banks_gpd = gpd.GeoDataFrame(food_banks_df, 
                                  geometry=gpd.points_from_xy(food_banks_df.lon, 
                                                              food_banks_df.lat))
    food_banks_gpd.to_file("CS_covid_food/map_query/data/food_banks.shp")









