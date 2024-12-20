from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

import re

def scrape_page(driver):

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    listings = soup.find_all('tr', {'id':'physician-extra-info'})
    listings = [[re.findall('>(.+?)<', x.find('td', {'id':'physician-name'}).contents[0]),
                 x.find('span', {'class':'cpso-badge'}).contents,
                 x.find('div', {'class':'specialities-container'}).contents,
                 x.find('div', {'id':'address-container'}).contents,
                 x.find('div', {'id':'phone-fax'}).contents,
                 x['data-href'] 
                ] for x in listings]
    #fixup right here, finish getting full listings information


def scrape_hospital(driver):
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    pages = soup.find('div', {'id':'entriesInfo'}).contents[0]
    pages = int(re.findall('Showing 1 of (.+?) pages', pages)[0])

    for page in range(1,pages):
        scrape_page(driver)
        driver.find_element(By.XPATH, '//*[@id="physicianTable_paginate"]/div/a[4]').click()

driver = webdriver.Chrome()
driver.get('https://register.cpso.on.ca/Advanced-Search/')

#Get all hospitals; we are splitting by hospitals because searches of >100 listings is not supported
soup = BeautifulSoup(driver.page_source, 'html.parser')
hospitals = soup.find('select', {'id':'hospitalName'})
hospitals = hospitals.find_all('option')[1:]
hospitals = [[re.findall('location="(.+?)"', str(x))[0], x.contents[0]] for x in hospitals]

for hospital in hospitals:

    driver.get('https://register.cpso.on.ca/Advanced-Search/')
    #For this moment, only scrape Markham hospitals; can expand later
    if hospital[0] != 'Markham':
        continue

    #Select chosen hospital, then submit
    select = Select(driver.find_element(By.ID, 'hospitalName'))
    select.select_by_visible_text(hospital[1])
    driver.find_element(By.XPATH, '//*[@id="advancedSearchForm"]/div[13]/button[1]').click()






#select = Select(driver.find_element(By.ID, 'hospitalName'))
