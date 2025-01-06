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
new_df['phone_number'] = new_df['phone_number'].str.strip()
new_df['phone_number'] = new_df['phone_number'].replace(r"\D+", "", regex=True).str.strip()
#new_df.to_csv(r'C:\Users\kumar\OneDrive\Desktop\Jordan\GRIT_directory_scraping\coo_opticians\coo_opticians_output_raw.csv', index=False)

df_905 = new_df[new_df['phone_number'].str[0:3] == '905']
df_647 = new_df[new_df['phone_number'].str[0:3] == '647']
df_416 = new_df[new_df['phone_number'].str[0:3] == '416']

df_sorted = pd.concat([df_905, df_647, df_416, new_df])
df_sorted = df_sorted.drop_duplicates(subset=['phone_number'], keep='first')

df_sorted.to_csv(r'C:\Users\kumar\OneDrive\Desktop\Jordan\GRIT_directory_scraping\coo_opticians\coo_opticians_output.csv', index=False)
