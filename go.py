'''
CS122 Group Project: COVID-19 and Food Insecurity in Chicago
Sophia Mlawer, Mariel Wiechers, Valeria Balza, and Gabriela Palacios 

This module manages all the sources of data. 
'''

import covid
import food_swamp
import acs_data
import regress
import food_banks
import create_databases


def run():
    '''
    Retrieves and processes each data source. Respective files
    are saved in the output_data folder. Also generates the SQL
    databases required for the Django web application
    '''

    # Saves covid_data.csv to output_data folder
    covid.go()

    # Saves acs_data.csv to output_data folder
    acs_data.go('input_data/ACS_demographic.csv', 'input_data/ACS_employment.csv', 
                'input_data/ACS_housing.csv', 'input_data/zctatozip.csv')
    
    # Saves food_swamp_zip.csv to output_data folder
    food_swamp.go()

    # Conducts regression analysis to generate predicted 'food swamp' indicator
    # and produces data tables to construct databases
    table_data, map_data = regress.model("output_data/food_swamp_zip", 
                                         "output_data/acs_data", 
                                         "output_data/covid_data")

    # Saves food_banks.csv to output_data folder
    food_banks_df = food_banks.go()
    
    # Creates databases and saves them to Django directory (CS_covid_food)
    create_databases.gen_sqlite(table_data)
    create_databases.gen_shapefiles(map_data, food_banks_df)


if __name__ == "__main__":
    run()