'''
This module manages all the sources of data. 

Sophia Mlawer, Mariel Wiechers, Valeria Balza, and Gabriela Palacios 
'''

import covid
import food_swamp
import acs
import food_banks
import regress
import gen_map

def run():
    # Covid Data
    covid.go()
    # Food Swamp Data
    food_swamp.food_swamp()
    # ACS Data
    acs()
    # Combine together and run regression
    full_data_by_zip = regress.model("food_swamp_data", "acs_data", "covid_data")
    # Food bank data
    food_banks()
    # # Generate maps
    gen_map()


if __name__ == "__main__":
    run()