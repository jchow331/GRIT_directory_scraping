import pandas as pd

df = pd.read_csv(r'C:\Users\kumar\OneDrive\Desktop\Jordan\GRIT_directory_scraping\coo_optometrists\coo_optometrists_output_raw.csv')
df = df.drop_duplicates()
df = df.sort_values(by=['phone_number'])
df = df.reset_index()

df['phone_number'] = df['phone_number'].str.strip()
df['phone_number'] = df['phone_number'].replace(r"\D+", "", regex=True).str.strip()
df.loc[df['phone_number'].str.len() > 10, 'phone_number'] = df['phone_number'].str[1:]

df = df[df['phone_number'] != '0000000000']

df = df.drop_duplicates(subset=['phone_number'], keep='first')

df_905 = df[df['phone_number'].str[0:3] == '905']
df_647 = df[df['phone_number'].str[0:3] == '647']
df_416 = df[df['phone_number'].str[0:3] == '416']

df_sorted = pd.concat([df_905, df_647, df_416, df])
df_sorted = df_sorted.drop_duplicates(subset=['phone_number'], keep='first')

df_sorted.to_csv(r'C:\Users\kumar\OneDrive\Desktop\Jordan\GRIT_directory_scraping\coo_optometrists\coo_optometrists_output_sorted_filtered.csv', index=False)