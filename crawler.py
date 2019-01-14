from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime as dt


class Crawler(object):
    def __init__(self):
        self.url = ''
        self.page = None
        self.soup = None
        
    def load_page(self, url):
        self.url = url
        self.page = requests.get(url)
        self.soup = BeautifulSoup(self.page.text, 'html.parser')
        
    def find_all(self, **kwargs):
        return self.soup.find_all(**kwargs)
        
    def get_page_data(self):
        tmp_data = list()
        raw_page_data = self.find_all(class_='result-info')
        for page in raw_page_data:
            title = page.find(class_='result-title hdrlnk')
            price = page.find(class_='result-price')
            m2_and_peices = page.find(class_='housing')
            neighborhood = page.find(class_='result-hood')
            link = page.find('a')

            title = title.get_text().strip() if title is not None else ''
            price = price.get_text().strip() if price is not None else ''
            m2_and_peices = m2_and_peices.get_text().strip() if m2_and_peices is not None else ''
            neighborhood = neighborhood.get_text().strip() if neighborhood is not None else ''
            link = link['href'].strip() if link is not None else ''

            tmp_data.append((title, price, m2_and_peices, neighborhood, link))
            
        return self.convertdf(pd.DataFrame(tmp_data, columns=['TITRE', 'PRIX', 'M2_ET_PIECES', 'ARR', 'LINK']))
    
    def get_site_data(self):
        start_time = dt.now()
        
        self.load_page('https://paris.craigslist.org/d/logement-%C3%A0-louer/search/apa')
        batch_size = len(self.find_all(class_='result-info'))
        total_record_count = int(self.soup.find(class_='totalcount').get_text())
        site_data = self.get_page_data()
        print('total_record_count= {}'.format(total_record_count))
        for idx in range(batch_size, total_record_count, batch_size):
            new_url = 'https://paris.craigslist.org/search/apa?s=%i' % idx
            self.load_page(new_url)
            site_data = pd.concat((site_data, self.get_page_data()), axis=0)
            
        site_data['ARR'] = site_data['ARR'].apply(lambda x: x.replace("(","").replace(")",""))
            
        elapsed = (dt.now() - start_time).seconds
        print('Collected %i records in %i seconds.' % (site_data.shape[0], elapsed))
        return site_data
      
     

    def add_description(self, site_data):

      site_data['DESCRIPTION'] = ''

    
