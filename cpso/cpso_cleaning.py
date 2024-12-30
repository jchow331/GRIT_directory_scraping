import pandas as pd
import numpy as np
import re

df = pd.read_csv(r'C:\Users\kumar\OneDrive\Desktop\Jordan\GRIT_directory_scraping\cpso\cpso_output_raw.csv')
df = df.drop_duplicates()

#Reformatting the phone_number column, then dropping empty values
df = df.dropna(subset=['phone_number'])
df['phone_number'] = df['phone_number'].str.lower().str.split('x').str[0]

#First filter numbers to try to remove long distance start and so on
df['phone_number'] = df['phone_number'].replace(r"\D+", "", regex=True).str.strip()
df.loc[df['phone_number'].str.len() > 10, 'phone_number'] = df['phone_number'].str[1:]
df['phone_number'] = df['phone_number'].str.strip().replace('', np.nan)
df = df.dropna(subset=['phone_number'])

#Second filtered drop of numbers of length > 10
df.loc[df['phone_number'].str.len() > 10, 'phone_number'] = None
df = df.dropna(subset=['phone_number'])

#Trying to handle if the number is a hospital number or something of the sort, if duplicate phone numbers exist, they're probably a hospital
df = df.sort_values(by=['phone_number'])
df = df.drop_duplicates(subset=['phone_number'], keep=False)

#Bring relevant numbers to top
df_905 = df[df['phone_number'].str[0:3] == '905']
df_647 = df[df['phone_number'].str[0:3] == '647']
df_416 = df[df['phone_number'].str[0:3] == '416']

df_sorted = pd.concat([df_905, df_647, df_416, df])
df_sorted = df_sorted.drop_duplicates(subset=['phone_number'], keep='first')

df_sorted.to_csv(r'C:\Users\kumar\OneDrive\Desktop\Jordan\GRIT_directory_scraping\cpso\cpso_output_sorted_filtered.csv', index=False)