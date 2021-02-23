
import bs4
import requests
#pip3 install fuzzywuzzy[speedup]


start = "https://en.wikipedia.org/wiki/List_of_fast_food_restaurant_chains"


def read_in(website):
    '''
    This function reads in the website if it's a website of interest
    Input: website
    Output: Beautiful Soup object of website
    '''
    request = requests.get(website)
    #text = request.text.encode('iso-8859-1')
    # request_text = get_request(website)
    # text = read_request(request_text)
    soup = bs4.BeautifulSoup(request.content, "html.parser")
    return soup

def scrape(soup):
    fast_food = []
    finder_block = soup.find("h5")
    list_food = finder_block.previousSibling.previousSibling
    for li in list_food.find_all("li"):
        fast_food.append(str.upper(li.text))
    
    return fast_food



