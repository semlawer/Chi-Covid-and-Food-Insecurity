'''
This module generates a static map of the City of Chicago with
layers of COVID-19 death rates data and food bank locations

Valeria Balza, Gabriela Palacios, Sophia Mlwawer and Mariel Wiechers
'''

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

COVID_DATA = 'data/pickle_covd.pkl'
ZIP_BOUNDARIES = 'data/zipcode_bndries.zip'


def gen_basemap(base_mape=ZIP_BOUNDARIES, covid=COVID_DATA):
    '''
    Generates geopandas df containing base_map of covid data
    '''
    
    base_map = gpd.read_file(ZIP_BOUNDARIES)
    base_map.rename(columns={'zip': 'zip_code'}, inplace=True)
    covid_df = pd.read_pickle(COVID_DATA)

    covid_map = base_map.merge(covid_df[["zip_code", "death_rate_cumulative"]], 
                               how="inner", on="zip_code")
    
    return covid_map


def gen_layers(covid_map, output_filename='covid_food_atlas.png'):
    '''
    Generates static map. Saves figure as png.
    '''

    out_map = covid_map.plot(column="death_rate_cumulative",
               cmap='Blues',
               legend=True, 
               edgecolor='lightsteelblue', 
               linewidth=0.3, figsize=(15,10))
    out_map.axis('off')
    out_map.set_title('Chicago COVID-19 Food Atlas', fontsize=20)
    plt.savefig('covid_food_atlas.png')
