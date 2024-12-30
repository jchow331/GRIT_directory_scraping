from bs4 import BeautifulSoup
from selenium import webdriver

import pandas as pd

def scrape_page(soup):
    
    


driver = webdriver.Chrome()
driver.get('https://members.collegeoptom.on.ca/COO/PublicDirectory/Public_Directory_Member_Process/Public_Register/PublicRegisterMemberProcess.aspx?hkey=349c676e-cbe0-4052-927d-08cc49d4f537')
soup = BeautifulSoup(driver.page_source, 'html.parser')

all_info = []
all_info.append(scrape_page(soup))


