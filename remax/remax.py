from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

import pandas as pd
import re

def scrape_location():
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    listings = soup.find_all('ul')[3]
    listings = listings.find_all('li')
    listings = [[re.findall('<h2 class="d-text d-agent-card-name unstyled" data-testid="d-text">(.+?)</h2>', str(x))[0].strip(),
                 location.title(),
                 next(iter(re.findall('"tel:(.+?)"', str(x))), None)] for x in listings]
    
    return listings


locations = ['markham', 'richmond-hill', 'vaughan']
url = 'https://www.remax.ca/on/{}-real-estate-agents'

location = locations[0]

driver = webdriver.Chrome()
driver.get(url.format(location))

all_data = []
#MANUALLY SCROLLED THROUGH PAGES HERE, SINCE NEGLIGIBLE NUMBER OF PAGES TO ITERATE THROUGH


df = pd.DataFrame(columns=['name','location','phone_number'], data=all_data)
df['phone_number'] = df['phone_number'].replace(r"\D+", "", regex=True).str.strip()
df = df.dropna(subset=['phone_number'])

df.to_csv(r'C:\Users\kumar\OneDrive\Desktop\Jordan\GRIT_directory_scraping\remax\remax_output.csv', index=False)