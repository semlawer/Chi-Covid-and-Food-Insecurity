'''
This module manages all the sources of data. 

Sophia Mlawer, Mariel Wiechers, Valeria Balza, and Gabriela Palacios 
'''

import covid
import food_swamp
import acs_data
import regress
# import gen_map
# import geopandas as gpd
# import food_banks


def run():
    '''
    '''
    # Covid Data
    covid.go()
    # # Food Swamp Data
    # # ACS Data
    acs_data.go('input_data/ACS_demographic.csv', 'input_data/ACS_employment.csv', 'input_data/ACS_housing.csv', 'input_data/zctatozip.csv')
    food_swamp.go()
    # # Combine together and run regression
    table_data, map_data = regress.model("output_data/food_swamp_zip", "output_data/acs_data", "output_data/covid_data")
    table_data.to_pickle('output_data/table_data.pkl')
    map_data.to_pickle('output_data/map_data.pkl')
    # # Food bank data
    # food_banks()
    # # # # Generate maps
    # gen_map()


if __name__ == "__main__":
    run()