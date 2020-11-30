import os
import pandas as pd

path_folder='data_zillow/'
data=[]
for name_file in os.listdir(path_folder):
    file=path_folder+name_file
    dftmp=pd.read_excel(file)
    data.append(dftmp)

df=pd.concat(data,ignore_index=True)
columns=['zipcode','url','url_detail']
df.columns=columns
columns=['zipcode','url_detail']
df = df.groupby(columns).agg({'url_detail': ['count']}).reset_index().droplevel(level = 1, axis = 1)
columns=['zipcode','url_detail','count_url_detail']
df.columns=columns

for i in range(df.shape[0]):
    df.loc[i, 'id_zillow'] =i


df.to_excel("db.xlsx", sheet_name='db', index=False)
