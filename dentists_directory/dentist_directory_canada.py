from bs4 import BeautifulSoup
import requests

import pandas as pd


def scrape_location(location):
    pass


locations = ['markham', 'richmond-hill', 'scarborough', 'toronto']

url = 'https://www.dentistdirectorycanada.ca/ontario-dentists-directory/{}-dentists-directory/'

#for location in locations:
    
page = requests.get(url.format(location))