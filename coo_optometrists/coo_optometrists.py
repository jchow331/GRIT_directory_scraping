from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import pandas as pd
import time
import re

def myzip(*args):
    try:
        x = [iter(i) for i in [*args]]
        while True:
        # for i in range(5):
            yield [next(ii) for ii in x]
            # I want to know why the commented line below won't work
            # yield [next(ii) for ii in [iter(i) for i in [*args]]]
            # or why this outputs [1, 'a']
            # return [next(ii) for ii in [iter(i) for i in [*args]]]
    except:
        pass


def scrape_page(soup):
    
    #Gets each member and corresponding info into list
    all_info = soup.find_all('tbody')[1].find('tbody')
    all_info = all_info.find_all('tr')[4].find('tbody')
    all_info = all_info.find_all('tr')[1:]

    #Seperates each optometrist and their location of practice
    buffer = [[re.findall('FullName">(.+?)</a>', str(x)), x] for x in all_info]
    buffer = [[x[0],
              [y.contents for y in x[1].find_all('td', {'style':'width: 63%; text-align: left; vertical-align: top;'})],
              [y.contents for y in x[1].find_all('td', {'style':'width: 63%; text-align: left; vertical-align: top;'})]
              ] for x in buffer if x[0]]
    buffer = [[[x[0]]*len(x[1]),
              [re.findall('<b>(.+?)</b>', ''.join(str(y))) for y in x[1]],
              [re.findall("Phone:(.+?)'", ''.join(str(y))) for y in x[2]]
              ] for x in buffer]
    #Keeps member if they have a practice location, fixes the list comprehension issue by zipping the lists up
    buffer = [list(myzip(x[0],x[1],x[2])) for x in buffer if x[2][0]]
    buffer = [element for innerList in buffer for element in innerList]
    buffer = [[next(iter(y), None) for y in x] for x in buffer]

    return buffer
    

#Initiate webdriver
driver = webdriver.Chrome()
driver.get('https://members.collegeoptom.on.ca/COO/PublicDirectory/Public_Directory_Member_Process/Public_Register/PublicRegisterMemberProcess.aspx?hkey=349c676e-cbe0-4052-927d-08cc49d4f537')
soup = BeautifulSoup(driver.page_source, 'html.parser')

#Get number of pages
#soup.find('select',{'name':'ctl01$TemplateBody$WebPartManager1$gwpste_container_MainControl$ciMainControl$ddlSearchResultsPage'})
pages = [x['value'] for x in soup.find_all('option')]

all_info = []
for page in pages:

    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    if soup.find('option',{'selected':'selected'})['value'] != page:
        time.sleep(10)

    all_info.extend(scrape_page(soup))
    next_button = driver.find_element(By.ID, 'ctl01_TemplateBody_WebPartManager1_gwpste_container_MainControl_ciMainControl_lbtnNext').click()

df = pd.DataFrame(columns=['name','practice_location','phone_number'], data=all_info)   
df.to_csv(r'C:\Users\kumar\OneDrive\Desktop\Jordan\GRIT_directory_scraping\coo_optometrists\coo_optometrists_output_raw.csv', index=False)

