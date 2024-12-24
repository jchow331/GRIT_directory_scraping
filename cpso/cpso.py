from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

import time
import re

def catch(func, handle=lambda e : e, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        return ''
    
def load_select_hospital(driver, hospital):

    driver.get('https://register.cpso.on.ca/Advanced-Search/')

    #Select hospital
    select = Select(driver.find_element(By.ID, 'hospitalName'))
    select.select_by_visible_text(hospital[1])
    driver.execute_script("window.scrollTo(0, 1000)")
    time.sleep(1)

    return driver

def scrape_page(driver):

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    listings = soup.find_all('tr', {'id':'physician-extra-info'})
    listings = [[catch(lambda: x.find('td', {'id':'physician-name'}).contents[0].contents[0].contents[0]),
                 catch(lambda: x.find('span', {'class':'cpso-badge'}).contents[0]),
                 catch(lambda: x.find('span', {'class':'speciality-badge'}).contents[0]),
                 catch(lambda: x.find('div', {'id':'address-container'}).contents[0].contents[0]),
                 catch(lambda: x.find('div', {'id':'phone-fax'}).contents[0].contents[0].replace('Phone: ','')),
                 catch(lambda: 'https://register.cpso.on.ca' + x['data-href'])] for x in listings]
    listings = [[' '.join(x.split()) for x in y] for y in listings]
    return listings

def scrape_hospital(driver):
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    pages = soup.find('div', {'id':'entriesInfo'}).contents[0]
    pages = int(re.findall('Showing 1 of (.+?) pages', pages)[0])

    for page in range(1,pages):
        scrape_page(driver)
        driver.find_element(By.XPATH, '//*[@id="physicianTable_paginate"]/div/a[4]').click()

def iterate_through_scrape(driver):
    listings = []

    #Continue if NO listings, not >100 listings
    if driver.find_element(By.ID, 'noResultsMessageMobile').text != '':
        return listings
    
    #Get number of pages
    try:
        pages = int(driver.find_element(By.ID, 'page-select').text.split('\n')[-1])
    except:
        pages = 2
    for page in range(1,pages+1):
        listings.append(scrape_page(driver))
        try:
            html = driver.find_element(By.TAG_NAME, 'html')
            html.send_keys(Keys.END)
            time.sleep(1)
            driver.find_element(By.XPATH, '//*[@id="pagination-controls"]/a/span').click()
        except:
            pass
    return listings


driver = webdriver.Chrome()
driver.get('https://register.cpso.on.ca/Advanced-Search/')

#Get all hospitals; we are splitting by hospitals because searches of >100 listings is not supported
soup = BeautifulSoup(driver.page_source, 'html.parser')
hospitals = soup.find('select', {'id':'hospitalName'})
hospitals = hospitals.find_all('option')[1:]
hospitals = [[re.findall('location="(.+?)"', str(x))[0], x.contents[0]] for x in hospitals]
#Get all specialties, for later
driver.execute_script("window.scrollTo(0, 1000)")
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, "input[type='radio'][value='Specialist']").click()
specialties = driver.find_element(By.ID, 'specialistType').text.split('\n')
specialties = list(filter(None, [x.strip() for x in specialties]))[1:]

all_listings = []
for hospital in hospitals:

    #Have to further split the searches into family doctor/specialist because of the results limitation 
    for x in range(0,2):

        #Load page and hospital selection
        driver = load_select_hospital(driver, hospital)

        #Select family doctor or specialist
        if x == 0:
            driver.find_element(By.CSS_SELECTOR, "input[type='radio'][value='Family Doctor']").click()
        elif x == 1:
            driver.find_element(By.CSS_SELECTOR, "input[type='radio'][value='Specialist']").click()
        driver.find_element(By.XPATH, '//*[@id="advancedSearchForm"]/div[13]/button[1]').click()

        #Load page/see if matches are found, continue if takes too long/no matches found
        try:
            myElem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'physician-extra-info')))
        except TimeoutException:

            #If yielded >100 results, iterate through specialities
            if driver.find_element(By.ID, 'maximumResultsCountMessageMobile').text != '':
                
                for specialty in specialties:
                    #Select specialty options, then proceed
                    driver = load_select_hospital(driver, hospital)
                    driver.find_element(By.CSS_SELECTOR, "input[type='radio'][value='Specialist']").click()
                    select = Select(driver.find_element(By.ID, 'specialistType'))
                    select.select_by_visible_text(specialty)
                    driver.find_element(By.XPATH, '//*[@id="advancedSearchForm"]/div[13]/button[1]').click()

                    all_listings.extend(iterate_through_scrape(driver))

            continue

        all_listings.extend(iterate_through_scrape(driver))

import pandas as pd

df = pd.DataFrame(columns=['name','id','specialty','address','phone_number','link'], data=all_listings)
df.to_csv(r'C:\Users\kumar\OneDrive\Desktop\Jordan\GRIT_directory_scraping\cpso\cspo_output_raw.csv', index=False)