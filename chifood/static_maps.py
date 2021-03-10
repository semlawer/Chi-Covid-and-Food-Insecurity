'''
This module generates a static map of the City of Chicago with
layers of COVID-19 death rates data and food bank locations

Valeria Balza, Gabriela Palacios, Sophia Mlwawer and Mariel Wiechers
'''

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

ZIP_BOUNDARIES = 'data/zip_bndries/zip_bndries.shp'
ALL_DATA = 'data/full_zip.csv'

def read_in(data):
    df = pd.read_csv(data)
    return df

def gen_basemap(base_map, data, var):
    '''
    Generates geopandas df containing base_map of covid data
    '''
    
    base_map = gpd.read_file(ZIP_BOUNDARIES)
    base_map.rename(columns={'zip': 'zipcode'}, inplace=True)
    base_map["zipcode"] = base_map["zipcode"].astype(int)
    df = read_in(data)
    #df = df[~df["zipcode"].isin([60666, 60606, 60602, 60604])]

    map = base_map.merge(df[["zipcode", var]], 
                               how="inner", on="zipcode")

    return map


def gen_layers(map, var, output_filename):
    '''
    Generates static map. Saves figure as png.
    '''

    fig, ax = plt.subplots(figsize=(15, 10))
    out_map = map.plot(ax=ax,
               column=var,
               cmap='RdPu',
               legend=True, 
               edgecolor='lightsteelblue', 
               linewidth=0.3)
    out_map.axis('off')
    out_map.set_title('Chicago COVID-19 Food Atlas', fontsize=20)
    plt.savefig(output_filename)

def go():
    covid_map = gen_basemap(ZIP_BOUNDARIES, ALL_DATA, "death_rate_cumulative")
    ratio_map = gen_basemap(ZIP_BOUNDARIES, ALL_DATA, "ratio")
    predict_ratio_map = gen_basemap(ZIP_BOUNDARIES, ALL_DATA, "pr_food")
    gen_layers(covid_map, "death_rate_cumulative", "COVID Death Rate.png")
    gen_layers(ratio_map, "ratio", "Food Insecurity Ratio.png")
    gen_layers(predict_ratio_map, "pr_food", "Predicted Food Insecurity Ratio.png")

