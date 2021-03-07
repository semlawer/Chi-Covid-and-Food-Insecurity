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

def retrieve_html(url=URL):
    '''
    '''
    req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    if req.status_code != 200:
        print('Request failed:', url)
        return None

    fbank_soup = bs4.BeautifulSoup(req.text, "html5lib")
    return fbank_soup


def get_locations(url):
    '''
    '''

    soup = retrieve_html(URL)
    df = pd.DataFrame()
    food_divs = soup.find_all("div", class_="list--row")
    geolocator = Nominatim(user_agent="vbalza@uchicago.edu")

    for f_bank in food_divs:
        info = f_bank.attrs
        info["address"] = f_bank.find("div", class_ = "location location--address").text.replace("\n", "").replace("  ", "")
        info.pop("class")

        if info["data-location-zip"] in VALID_ZIPS:
            coords = geolocator.geocode(info["address"])
            if coords != None:
                info["lat"] = coords.latitude
                info["lon"] = coords.longitude
                df = df.append(info, ignore_index=True)

    return df