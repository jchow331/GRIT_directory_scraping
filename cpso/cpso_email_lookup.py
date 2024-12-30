from bs4 import BeautifulSoup
import requests

import pandas as pd
import random

df = pd.read_csv(r'C:\Users\kumar\OneDrive\Desktop\Jordan\GRIT_directory_scraping\cpso\cpso_output_clean.csv', index_col=False)
all_urls = df['link'].tolist()

def scrape_for_email(url):

    page = requests.get('https://register.cpso.on.ca/physician-info/?cpsonum=105075')
    soup = BeautifulSoup(page.text, 'html.parser')
    email = soup.find('div', {'class':'list-content-section scrp-businessemail'}).contents[-1].strip()
    print(email)

    if email == 'No Information Available':
        return
    else:
        return email
    
all_emails = []
for url in random.sample(all_urls, 500):

    email = scrape_for_email(url)
    if email:
        all_emails.append(email)
    