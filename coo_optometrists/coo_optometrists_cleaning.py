import pandas as pd

df = pd.read_csv(r'C:\Users\kumar\OneDrive\Desktop\Jordan\GRIT_directory_scraping\coo_optometrists\coo_optometrists_output_raw.csv')
df = df.drop_duplicates()
df = df.sort_values(by=['phone_number'])
df = df.reset_index()

df['phone_number'] = df['phone_number'].str.strip()
df['phone_number'] = df['phone_number'].replace(r"\D+", "", regex=True).str.strip()

df = df[df['phone_number'] != '(000) 000-0000']