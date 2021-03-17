'''
This module scrapes the Greater Chicago Food Depository for data
    on the location of food-related resources, including mobile pantries,
    soup kitchens, Producemobiles, etc.

Valeria Balza, Gabriela Palacios, Sophia Mlwawer and Mariel Wiechers
'''

import requests
import bs4
import pandas as pd
from geopy.geocoders import Nominatim

OUTPUT_FILENAME = 'output_data/food_banks_data.csv'
URL = 'https://www.chicagosfoodbank.org/find-food/'
VALID_ZIPS = ['60601', '60602', '60603', '60604', '60605','60606', '60607',
                  '60608', '60609', '60610', '60611', '60612', '60613', '60614', 
                  '60615', '60616', '60617', '60618', '60619', '60620', '60621', 
                  '60622', '60623', '60624','60625', '60626', '60628', '60629',
                  '60630', '60631', '60632', '60633', '60634', '60636','60637',
                  '60638', '60639', '60640', '60641', '60642', '60643', '60644',
                  '60645', '60646', '60647', '60649', '60651', '60652', '60653',
                  '60654', '60655', '60656', '60657', '60659', '60660', '60661',
                  '60666', '60707','60827']

def go(output_filename=OUTPUT_FILENAME):
    '''

    '''

    df = get_locations()
    food_banks_df = process_df(df)
    food_banks_df.to_csv(output_filename, index=False)

    return food_banks_df
    


def get_html_document(url=URL):
    '''
    Retrieves HTML document
    '''

    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    if r.status_code != 200:
        print('Request failed:', url)
        return None

    soup = bs4.BeautifulSoup(r.text, "html5lib")
    return soup


def get_locations(url=URL):
    '''
    Extracts information from HTML. Converts
        address to lat, lon coordinates
    '''

    df_locs = pd.DataFrame()

    fb_soup = get_html_document(url)
    food_banks = fb_soup.find_all("div", class_="list--row")

    geolocator = Nominatim(user_agent="vbalza@uchicago.edu")

    for location in food_banks:
        inf_df = location.attrs
        inf_df["address"] = location.find("div", class_ = "location location--address").text.replace("\n", "").replace("  ", "")
        inf_df.pop("class")

        if inf_df["data-location-zip"] in VALID_ZIPS:
            coords = geolocator.geocode(inf_df["address"])
            if coords != None:
                inf_df["lat"] = coords.latitude
                inf_df["lon"] = coords.longitude
                df_locs = df_locs.append(inf_df, ignore_index=True)

    return df_locs


def process_df(df):
    '''
    Processes data. Fixes two point mistakes. Drops duplicate row. Renames columns.
    '''

    df.loc[df["address"] == "1048 N Campbell Ave, Chicago, IL 60622", ["lat"]] = 41.900899
    df.loc[df["address"] == "1919 S Ashland Ave, Chicago, IL 60608", ["lat"]] = 41.855516
    df = df.drop(df.loc[df["address"] == "1919 S Ashland Ave , Chicago, IL 60608"].index)
    df.columns = ['address', 'category', 'location_id', 'name', 'zip_code', 'lat', 'lon']

    return df
