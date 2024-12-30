import pandas as pd

df = pd.read_csv(r'C:\Users\kumar\OneDrive\Desktop\Jordan\GRIT_directory_scraping\canadayp_output_clean.csv')

df_dict = df.groupby(['name'])['category'].apply(', '.join).to_dict()#.reset_index()
#df_dict = df_dict.set_index('name').to_dict()

#f['category'].replace(df_dict, inplace=False)
for i in range(0,len(df)):
    try:
        df.loc[i, 'category'] = ', '.join(list(set([x.strip() for x in df_dict[df.loc[i,'name']].split(',')])))
    except:
        pass

df.drop_duplicates(inplace=True)
df.to_csv('canadayp_output_clean.csv',index=False, encoding='utf_8_sig')
