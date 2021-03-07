'''
This module generates a static map of the City of Chicago with
layers of COVID-19 death rates data and food bank locations

Valeria Balza, Gabriela Palacios, Sophia Mlwawer and Mariel Wiechers
'''

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

ZIP_BOUNDARIES = 'data/zip_bndries/zip_bndries.shp'
COVID_DATA = 'data/pickle_covd.pkl'
FOOD_BANK = 'data/food_banks.pkl'


def gen_basemap(base_map=ZIP_BOUNDARIES, covid=COVID_DATA):
    '''
    Generates geopandas df containing base_map of covid data
    '''
    
    base_map = gpd.read_file(ZIP_BOUNDARIES)
    base_map.rename(columns={'zip': 'zip_code'}, inplace=True)
    covid_df = pd.read_pickle(COVID_DATA)
    food_df = pd.read_pickle(FOOD_BANKS)

    covid_map = base_map.merge(covid_df[["zip_code", "death_rate_cumulative"]], 
                               how="inner", on="zip_code")
    food_banks = gpd.GeoDataFrame(food_df, 
                                 geometry=gpd.points_from_xy(food_df.lon, 
                                                             food_df.lat))

    food_banks.loc[food_banks["address"] == \
        "1048 N Campbell Ave, Chicago, IL 60622", ["lat"]] = 41.900899
    food_banks.loc[food_banks["address"] == \
        "1919 S Ashland Ave, Chicago, IL 60608", ["lat"]] = 41.855516
    food_banks = food_banks.drop(food_banks.loc[food_banks["address"] == \
        "1919 S Ashland Ave , Chicago, IL 60608"].index)

    return covid_map


def gen_layers(covid_map, output_filename='covid_food_atlas.png'):
    '''
    Generates static map. Saves figure as png.
    '''

    fig, ax = plt.subplots(figsize=(15, 10))
    out_map = covid_map.plot(ax=ax,
               column="death_rate_cumulative",
               cmap='Blues',
               legend=True, 
               edgecolor='lightsteelblue', 
               linewidth=0.3)
    food_banks.plot(ax=ax, marker='o', color='red', markersize=10)
    out_map.axis('off')
    out_map.set_title('Chicago COVID-19 Food Atlas', fontsize=20)
    plt.savefig(output_filename)
