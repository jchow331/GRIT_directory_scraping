from selenium import webdriver
from bs4 import BeautifulSoup

import pandas as pd
import re

url = 'https://www.rcdso.org/find-a-dentist/search-results?Alpha=&City=&MbrSpecialty=&ConstitID=&District=&AlphaParent=&Address1=&PhoneNum=&SedationType=&SedationProviderType=&GroupCode=&DetailsCode='

driver = webdriver.Chrome()
driver.get(url)
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.close()

listings = soup.find_all('section')[1:]
listings = [[x.find('h2').contents[0].contents[0].strip(), x.find('address'), x.find_all('a')] for x in listings]
listings = [[x[0], x[1].find('span').text, x[2]] if x[1] else [x[0], x[1], x[2]] for x in listings]
listings = [[x[0], x[1], x[2][1]['href']] if len(x[2]) > 1 else [x[0], x[1], ''] for x in listings]
listings = [[x[0], x[1], next(iter(re.findall('tel:(.+?)$', x[2])), None)] if 'tel' in x[2] else [x[0], x[1], None] for x in listings]

df = pd.DataFrame(columns=['name','primary_practice','phone_number'], data=listings)

df = df.dropna(subset=['phone_number'])
df = df.drop_duplicates(subset=['phone_number'])
df_905 = df[df['phone_number'].str[0:3] == '905']
df_647 = df[df['phone_number'].str[0:3] == '647']
df_416 = df[df['phone_number'].str[0:3] == '416']
df_sorted = pd.concat([df_905, df_647, df_416, df])
df_sorted = df_sorted.drop_duplicates(subset=['phone_number'], keep='first')

df_sorted.to_csv(r'C:\Users\kumar\OneDrive\Desktop\Jordan\GRIT_directory_scraping\dentists_directory\rcdso_output.csv', index=False)