from selenium import webdriver
from bs4 import BeautifulSoup


import pandas as pd
import re


def get_user_ids(driver):
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    #rows = soup.find_all('tr', {'role':'row'})
    rows = soup.find_all('tr', {'class':'rgRow'})
    rows.extend(soup.find_all('tr', {'class':'rgAltRow'}))
    rows = [x.find_all('td', {'role':'gridcell'}) for x in rows]
    rows = [x[4].find('span')['onclick'] for x in rows if 
             (next(iter(x[1].contents), None) == 'Entitled to Practise') or
             (next(iter(x[1].contents), None) == 'Current and Inactive') or
             (next(iter(x[1].contents), None) == 'Entitled to Practise under Supervision')]

    return [re.findall(r'\d+', x)[0] for x in rows]


driver = webdriver.Chrome()
driver.get('https://members.collegeofopticians.ca/Public-Register')


#CLICK FIND

#SCROLL TO BOTTOM

#CLICK 50 RESULTS