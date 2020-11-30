import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import time


class Zillow():
    def __init__(self, zipcode, count_of_query):
        self.zipcode = zipcode
        self.count_of_query = count_of_query

        self.method_url= 0
        self.headers= {
                        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'accept-encoding':'gzip, deflate, sdch, br',
                        'accept-language':'en-GB,en;q=0.8,en-US;q=0.6,ml;q=0.4',
                        'cache-control':'max-age=0',
                        'upgrade-insecure-requests':'1',
                        'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
            }
    def create_url(self):
        if self.method_url==0:
            url = "https://www.zillow.com/homes/for_sale/{0}/0_singlestory/days_sort".format(self.zipcode)
        if self.method_url==1:
            url = "https://www.zillow.com/homes/for_sale/{0}/0_singlestory/pricea_sort".format(self.zipcode)
        
        self.url = url

        return self.url

    def query_zillow_requests(self):
        res=requests.get(url=self.url, headers=self.headers)

        self.status_code = res.status_code
        self.html = res.text

        return (self.url, self.status_code)
    
    def extract_zillow_info(self):
        dicc={}

        if self.status_code==200:
          soup = BeautifulSoup(self.html, 'html.parser')
          contents = soup.find_all('a',class_='list-card-link list-card-link-top-margin list-card-img')

          i=0
          for content in contents:
              dicc[str(i)]= [str(self.zipcode),str(self.url) ,str(content.attrs.get('href'))]
              i=i+1
        
        self.dicc=dicc

        return self.dicc    

    def Create_file_excel(self):
        file_name_excel = "data_zillow\zillow_{0}_{1}_{2}.xlsx".format(self.zipcode, self.count_of_query,self.method_url)
        df = pd.DataFrame(self.dicc)
        df = df.T
        df.to_excel(file_name_excel, sheet_name='info', index=False)
        return file_name_excel
    
    def sleep_scrapper(self):
        if self.status_code==200:
            print(self.status_code)
            time.sleep(30)
        else:
            print(self.status_code)
            time.sleep(1800)


df = pd.read_excel(io='master.xlsx', sheet_name='master')

for i in range(df.shape[0]):
    if df.loc[i, 'state_of_query'] == 1:
        zipcode = df.loc[i, 'zipcode']
        count_of_query = df.loc[i, 'count_of_query'] + 1

        mizillow = Zillow(zipcode=zipcode, count_of_query=count_of_query)

        mizillow.create_url()
        mizillow.query_zillow_requests()
        mizillow.extract_zillow_info()
        mizillow.Create_file_excel()
        mizillow.sleep_scrapper()

        df.loc[i, 'count_of_query'] = count_of_query
        df.loc[i, 'last_date_of_query'] = datetime.datetime.now()

        df.to_excel("master.xlsx", sheet_name='master', index=False)
