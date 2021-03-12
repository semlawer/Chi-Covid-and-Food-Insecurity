'''
This module manages all the sources of data. 

Sophia Mlawer, Mariel Wiechers, Valeria Balza, and Gabriela Palacios 
'''

import covid
import food_swamp
import acs
import regress
import gen_map
import geopandas as gpd
import food_banks


def run():
    # Covid Data
    covid.go()
    # Food Swamp Data
    food_swamp.food_swamp()
    # ACS Data
    acs()
    # Combine together and run regression
    table_data, map_data = regress.model("data/food_swamp_zip", "acs/acs_data", "data/covid_data")
    # Food bank data
    food_banks()
    # # # Generate maps
    gen_map()


if __name__ == "__main__":
    run()