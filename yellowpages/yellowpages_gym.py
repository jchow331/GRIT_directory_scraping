from bs4 import BeautifulSoup
from selenium import webdriver

import pandas as pd
import time

url = 'https://www.yellowpages.ca/search/si/{}/Fitness+Gyms/{}'
locations = ['markham', 'scarborough', 'vaughan', 'toronto']

driver = webdriver.Chrome()

all_listings = []
for location in locations:

    driver.get(url.format(1, location))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    pages = int(soup.find('span', {'class':'pageCount'}).find_all('span')[-1].text.strip())

    for page in range(1,pages):

        driver.get(url.format(page, location))
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        listings = soup.find_all('div', {'class':'listing__content__wrap--flexed jsGoToMp'})
        listings = [[x.find('a', {'class':'listing__name--link listing__link jsListingName'}).text,
                    x.find('li', {'class':'mlr__item mlr__item--more mlr__item--phone jsMapBubblePhone'}),
                    ', '.join([y.text for y in x.find_all('span', {'class':'jsMapBubbleAddress'})]),
                    'https://yellowpages.ca' + x.find('link')['href']] for x in listings]
        listings = [[x[0], x[1].find('li', {'class':'mlr__submenu__item'}).text.strip(), x[2], x[3]]           
                    if x[1] else [x[0], None, x[2], x[3]] for x in listings]
        all_listings.extend(listings)

driver.close()

df = pd.DataFrame(columns=['name','phone_number','address','url'], data=all_listings)
df = df.drop_duplicates(subset=['phone_number'])
df.to_csv(r'C:\Users\kumar\OneDrive\Desktop\Jordan\GRIT_directory_scraping\yellowpages\yellowpages_gym_output.csv', index=False)
