from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import requests

import pandas as pd
import math
import re

#Scrapes all links to businesses on page
def get_links_on_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    links = soup.find_all('a', {'class':'btn btn-success btn-block'})
    links = ['https://www.canadayp.ca' + x['href'] for x in links]
    return links

#Gathers the categorical ids to iterate through
def get_all_ids():
    page = requests.get('https://www.canadayp.ca/')
    soup = BeautifulSoup(page.text, 'html.parser')
    ids = soup.find(id='bd-chained')
    ids = ids.find_all('option')
    return [[x['value'], x.contents[0]] for x in ids if x.contents]

#Gathers all links to businesses, across the website
def get_all_links():
    ids = get_all_ids()
    all_links = []

    for i in ids:
        page = requests.get('https://www.canadayp.ca/search_results?tid={}'.format(i[0]))
        soup = BeautifulSoup(page.text, 'html.parser')

        #Get number of iteratable pages
        try:
            num_pages = soup.find('div', {'class':'col-sm-7 nopad bmargin'}).contents[0]
        except:
            continue
        num_pages = math.ceil(int(re.findall(' (.+?) 結果', num_pages)[0].strip())/9)

        for page_num in range(0,num_pages):
            scraped_links = [[x, i[1]] for x in get_links_on_page('https://www.canadayp.ca/search_results?page={}&tid={}'.format(page_num, i[0]))]
            all_links.extend(scraped_links)
            print(len(all_links))

    return all_links

def scrape_link(url, category):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    try:
        name = next(iter(soup.find('div', {'class':'table-view-group clearfix table-display-company'}).find('span').contents))
    except:
        name = ''
    try:
        number = next(iter(soup.find('div', {'class':'table-view-group clearfix table-display-phone_number'}).find('span').contents))
    except:
        number = ''
    try:
        email = next(iter(soup.find('div', {'class':'table-view-group clearfix table-display-email'}).find('span').contents))
    except:
        email = ''
    try:
        website = soup.find('a', {'class':'weblink'})['href']
    except:
        website = ''

    return [name, number, email, website, category, url]


def main():

    all_links = get_all_links()
    all_info = []
    
    #Can't use concurrent futures without bricking the IP address
    #with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    #    all_info = list(executor.map(scrape_link, [x[0] for x in all_links], [x[1] for x in all_links]))
    for link in all_links:
        print('{}/{}'.format(all_links.index(link), len(all_links)))
        info = scrape_link(link[0], link[1])
        all_info = all_info.append(info)

    df = pd.DataFrame(columns=['name', 'number', 'email', 'website', 'category', 'url'], data=all_info)
    df.to_csv('canadayp_output.csv', index=False, encoding='utf_8_sig')

