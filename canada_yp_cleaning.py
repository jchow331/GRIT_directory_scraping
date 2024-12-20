import pandas as pd

df = pd.read_csv('canadayp_output_1.csv')

df_dict = df.groupby(['name'])['category'].apply(', '.join).to_dict()#.reset_index()
#df_dict = df_dict.set_index('name').to_dict()

#f['category'].replace(df_dict, inplace=False)
for i in range(0,len(df)):
    try:
        df.loc[i, 'category'] = ', '.join(list(set([x.strip() for x in df_dict[df.loc[i,'name']].split(',')])))
    except:
        pass

df.drop_duplicates(inplace=True)

df.to_csv('canadayp_output_clean_1.csv',index=False, encoding='utf_8_sig')


#df.loc[i,'category'] = [x.strip() for x in df.loc[i,'category'].split(',')]