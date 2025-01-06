import requests

from bs4 import BeautifulSoup
import pandas as pd

def scrape_id(optician_id):

    page = requests.get(url.format(optician_id))
    soup = BeautifulSoup(page.text, 'html.parser')

    data = soup.find_all('div', {'id':'IQAResults'})[0]
    data = [data.contents[1].get_text()]
    prac_locs = soup.find_all('tr', {'id':'ctl01_TemplateBody_WebPartManager1_gwpciPracticeLocationsIQA_ciPracticeLocationsIQA_ResultsGrid_Grid1_ctl00__0'})
    prac_locs = [[y.get_text() for y in x.contents] for x in prac_locs]
    prac_locs = [[x[2], x[3], x[5]] for x in prac_locs][0]
    data.extend(prac_locs)

    return data


df = pd.read_csv(r'C:\Users\kumar\OneDrive\Desktop\Jordan\GRIT_directory_scraping\coo_opticians\coo_opticians_ids.csv')
url = "https://members.collegeofopticians.ca/coo/Public%20Register/Reigstrant-Information.aspx?UserID={}"

all_data = []
for optician_id in df['id'].tolist():

    all_data.append(scrape_id(optician_id))
    
new_df = pd.DataFrame(columns=['name','location','phone_number','address'], data=all_data)
new_df.to_csv(r'C:\Users\kumar\OneDrive\Desktop\Jordan\GRIT_directory_scraping\coo_opticians\coo_opticians_output_raw.csv', index=False)


