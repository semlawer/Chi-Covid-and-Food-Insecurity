# -*- coding: utf-8 -*-
"""
Scrape IPEDS http://nces.ed.gov/ipeds/datacenter/DataFiles.aspx
Hannah Recht, 03-24-16
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

import json
import time
import sys


def scrapetable(content):
    dirurl = "http://nces.ed.gov/ipeds/datacenter/"
    # Scrape table of datasets
    soup = BeautifulSoup(''.join(content), "html5lib")
    table = soup.find("table", {"id": "contentPlaceHolder_tblResult"})
    # Get info and URLs for data zip and dictionary zip
    files = []
    for row in table.find_all('tr')[1:]:
        entry = dict()
        tds = row.find_all('td')
        entry['year'] = int(tds[0].text)
        entry['survey'] = tds[1].text
        entry['title'] = tds[2].text
        entry['dataurl'] = dirurl + tds[3].a.get('href')
        entry['dicturl'] = dirurl + tds[6].a.get('href')
        # File name minus 'data/' and '.zip'
        entry['name'] = (tds[3].a.get('href')[5:-4]).lower()
        files.append(entry)
    return files


# Get info on all the available datasets per year, save
def chooseyear(year, select, driver):
    # Choose year from dropdown
    select.select_by_value(year)

    # Continue to list of datasets
    time.sleep(5)
    driver.find_element_by_xpath(
        "//input[@id='contentPlaceHolder_ibtnContinue']").click()

    # Scrape the table of available datasets, add to 'files'
    time.sleep(5)
    content = driver.page_source
    return scrapetable(content)


def go():

    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    driver = webdriver.Chrome(options=chrome_options)

    # There is no direct link to the complete data files view. Need to
    # press some buttons.  If the site changes this will probably all
    # break yay

    # Complete data files entry point
    driver.get('http://nces.ed.gov/ipeds/datacenter/login.aspx?gotoReportId=7')

    # Press continue
    time.sleep(5)

    driver.find_element_by_id('contentPlaceHolder_ibtnContinue').click()

    # Make a list for all the available years
    time.sleep(5)
    select = Select(driver.find_element_by_id('contentPlaceHolder_ddlYears'))
    valid_years = list()
    for option in select.options:
        valid_years.append(option.get_attribute('value'))

    print(f"IPEDS has data for the following years:{valid_years}")

    # Find data for all years (-1 = All Years)
    files = chooseyear("-1", select, driver)

    # Export to json
    with open('ipedsfiles.json', 'w') as fp:
        json.dump(files, fp)


if __name__ == "__main__":
    go()
