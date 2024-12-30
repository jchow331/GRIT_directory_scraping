from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import pandas as pd
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


    


driver = webdriver.Chrome()
driver.get('https://members.collegeoptom.on.ca/COO/PublicDirectory/Public_Directory_Member_Process/Public_Register/PublicRegisterMemberProcess.aspx?hkey=349c676e-cbe0-4052-927d-08cc49d4f537')
soup = BeautifulSoup(driver.page_source, 'html.parser')

all_info = []
all_info.append(scrape_page(soup))


