import pandas as pd

df_small = pd.read_csv(r'C:\Users\kumar\OneDrive\Desktop\Jordan\GRIT_directory_scraping\dentists_directory\dentist_directory_canada_output.csv')
df_large = pd.read_csv(r'C:\Users\kumar\OneDrive\Desktop\Jordan\GRIT_directory_scraping\dentists_directory\rcdso_output.csv')
df_small = df_small.drop_duplicates(subset=['phone_number'])
df_large = df_large.drop_duplicates(subset=['phone_number'])

df_combined = pd.concat([df_small, df_large])
df_combined = df_combined[df_combined.duplicated(['phone_number'], keep=False)]
df_combined = df_combined.sort_values(by=['phone_number'])

#df_combined.to_csv(r'C:\Users\kumar\OneDrive\Desktop\Jordan\GRIT_directory_scraping\dentists_directory\cross_reference.csv', index=False)

df_smaller = pd.concat([df_small, df_combined])
df_smaller = df_smaller.drop_duplicates(subset=['phone_number'], keep=False)
df_smaller.to_csv(r'C:\Users\kumar\OneDrive\Desktop\Jordan\GRIT_directory_scraping\dentists_directory\cross_reference.csv', index=False)