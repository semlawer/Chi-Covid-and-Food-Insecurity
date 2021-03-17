'''
CS122 Group Project: COVID-19 and Food Insecurity in Chicago
Authors: Valeria Balza, Gabriela Palacios, Sophia Mlawer and Mariel Wiechers
Contact: Sophia Mlawer

This module scrapes the main fast food restaurants in the United States
from Wikipedia
'''

import bs4
import requests


def read_in(website):
    '''
    This function reads in the website if it's a website of interest
    Input: website
    Output: Beautiful Soup object of website
    '''

    request = requests.get(website)
    soup = bs4.BeautifulSoup(request.content, "html.parser")
    return soup


def scrape(soup):
    '''
    This function scrapes through the website to extract American 
    fast food information.
    '''

    fast_food = []
    finder_block = soup.find("h5")
    list_food = finder_block.previousSibling.previousSibling
    for li in list_food.find_all("li"):
        fast_food.append(str.upper(li.text))
    
    return fast_food


def ff_by_zip(df):
    '''
    Collapses data by zip code and returns
    '''

    df["ZIP CODE"] = df["ZIP CODE"].astype("string")
    df[["zip_code", "zip_extra"]] = df["zip"].str.split(".", expand=True)
    collapse = df["zip_code"].value_counts()
    collapse.name = "fast_food"

    return collapse
