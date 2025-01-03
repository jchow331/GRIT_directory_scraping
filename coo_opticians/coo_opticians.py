from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup


import pandas as pd
import time
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

#Get results and expand to 50 listings per page properly
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
driver.find_element(By.ID, 'ctl01_TemplateBody_WebPartManager1_gwpciNewQueryMenuCommon_ciNewQueryMenuCommon_ResultsGrid_Sheet0_SubmitButton').click()
time.sleep(30)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

pages = driver.find_element(By.XPATH, '//*[@id="ctl01_TemplateBody_WebPartManager1_gwpciNewQueryMenuCommon_ciNewQueryMenuCommon_ResultsGrid_Grid1_ctl00"]/tfoot/tr/td/table/tbody/tr/td/div[5]').text
driver.find_element(By.ID, 'ctl01_TemplateBody_WebPartManager1_gwpciNewQueryMenuCommon_ciNewQueryMenuCommon_ResultsGrid_Grid1_ctl00_ctl03_ctl01_PageSizeComboBox_Input').click()
driver.find_element(By.ID, 'ctl01_TemplateBody_WebPartManager1_gwpciNewQueryMenuCommon_ciNewQueryMenuCommon_ResultsGrid_Grid1_ctl00_ctl03_ctl01_PageSizeComboBox_Input').send_keys(Keys.DOWN)
driver.find_element(By.XPATH, '//*[@id="ctl01_TemplateBody_WebPartManager1_gwpciNewQueryMenuCommon_ciNewQueryMenuCommon_ResultsGrid_Grid1_ctl00"]/tfoot/tr/td/table/tbody/tr/td/div[5]').click()
new_pages = pages
while new_pages == pages:
    new_pages = driver.find_element(By.XPATH, '//*[@id="ctl01_TemplateBody_WebPartManager1_gwpciNewQueryMenuCommon_ciNewQueryMenuCommon_ResultsGrid_Grid1_ctl00"]/tfoot/tr/td/table/tbody/tr/td/div[5]').text
    time.sleep(5)
    print('waiting')
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

all_user_ids = []
pages = int(re.findall('in (.+?) pages', new_pages)[0])
for page in range(1,pages-1):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    all_user_ids.extend(get_user_ids(driver))

    old_num = driver.find_element(By.CLASS_NAME, 'rgCurrentPage')
    new_num = old_num
    driver.find_element(By.CLASS_NAME, 'rgPageNext').click()
    while old_num == new_num:
        new_num = driver.find_element(By.CLASS_NAME, 'rgCurrentPage')
        time.sleep(5)
    