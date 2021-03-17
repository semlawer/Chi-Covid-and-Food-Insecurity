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


def gen_sqlite(data):
    '''
    Creates a SQLite database from a pandas
    df

    Inputs: pandas df
    Returns: None
    '''

    engine = create_engine('sqlite:///CS_covid_food/chifood2.sqlite3', echo=False)
    sqlite_connection = engine.connect()
    data.to_sql('data2', sqlite_connection)
    sqlite_connection.close()






