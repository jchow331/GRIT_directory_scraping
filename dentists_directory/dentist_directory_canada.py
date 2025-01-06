from bs4 import BeautifulSoup
import requests

import pandas as pd
import re


def scrape_location(location):

    page = requests.get(url.format(location))
    soup = BeautifulSoup(page.text, 'html.parser')
    listings = soup.find_all('div', {'class':'one_third'})[1:-2]
    #listings.extend(soup.find_all('div', {'class':'one_third last'})[1:-2])
    listings = [[next(iter(re.findall('<strong>(.+?)</strong>', str(x))), None),
                location.title(),
                next(iter(re.findall('Phone(.+?)\n', x.text)), None),
                x.find('a')] for x in listings]
    listings = [[x[0], x[1], x[2], x[3]['href']] if x[3] else x for x in listings]

    return listings


locations = ['markham', 'richmond-hill', 'scarborough', 'toronto']
url = 'https://www.dentistdirectorycanada.ca/ontario-dentists-directory/{}-dentists-directory/'

all_data = []
for location in locations:
    all_data.extend(scrape_location(location))

df = pd.DataFrame(columns=['name','location','phone_number','website'], data=all_data)

df['phone_number'] = df['phone_number'].str.strip()
df['phone_number'] = df['phone_number'].replace(r"\D+", "", regex=True).str.strip()

df.to_csv(r'C:\Users\kumar\OneDrive\Desktop\Jordan\GRIT_directory_scraping\dentists_directory\dentist_directory_canada_output.csv', index=False)