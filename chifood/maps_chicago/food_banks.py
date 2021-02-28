import requests
from urllib.request import Request, urlopen
import urllib.parse
import bs4
import pandas as pd


def get_html_document(url):
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = bs4.BeautifulSoup(r.text, "html5lib")
    return soup

def get_locations(url):
    df_locs = pd.DataFrame()
    fb_soup = get_html_document(url)
    div_location = fb_soup.find_all("div", class_="list--row")
    for location in div_location:
        inf_df = location.attrs
        inf_df["address"] = location.find("div", class_ = "location location--address").text.replace("\n", "").replace("  ", "")
        df_locs = df_locs.append(inf_df, ignore_index=True)
    return df_locs
