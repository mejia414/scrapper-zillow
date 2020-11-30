import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import time
import json


class ZillowDetail():
    def __init__(self, url, id_zillow):
        self.url = url
        self.id_zillow = id_zillow

        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, sdch, br',
            'accept-language': 'en-GB,en;q=0.8,en-US;q=0.6,ml;q=0.4',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }

    def query_zillow_detail_requests(self):
        res = requests.get(url=self.url, headers=self.headers)

        self.status_code = res.status_code
        self.html = res.text

        return (self.url, self.status_code)

    def extract_zillow_detail_info(self):
        dicc = {}

        if self.status_code == 200:
            soup = BeautifulSoup(self.html, 'html.parser')

        contents = soup.find_all('span',class_='Text-c11n-8-11-1__aiai24-0 hqfqED')
        i=0
        
        for content in contents:
            dicc[str(i)]= str(content.get_text())
            i=i+1
        
        self.dicc=dicc

        return self.dicc
    
    def Create_file_json_detail(self):
        data=[]
        data.append(self.dicc)
        file_name_json = "data_zillow_detail\zillow_detail_{0}.json".format(self.id_zillow)
        with open(file_name_json, 'w') as file:
            json.dump(data, file, indent=4)



    def sleep_scrapper_detail(self):
        if self.status_code==200:
            print(self.status_code)
            time.sleep(30)
        else:
            print(self.status_code)
            time.sleep(1800)




df = pd.read_excel(io='db.xlsx', sheet_name='db')

for i in range(df.shape[0]):
    url = df.loc[i, 'url_detail']
    id_zillow = df.loc[i, 'id_zillow']

    mizillowdetail = ZillowDetail(url=url, id_zillow=id_zillow)
    mizillowdetail.query_zillow_detail_requests()
    mizillowdetail.extract_zillow_detail_info()
    mizillowdetail.Create_file_json_detail()
    mizillowdetail.sleep_scrapper_detail()