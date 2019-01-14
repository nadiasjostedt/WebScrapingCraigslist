from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime as dt


class Crawler(object):
    def __init__(self):
        self.url = ''
        self.page = None
        self.soup = None
        self.raw_page_data = None
        self.clean_page_data = None
        self.total_count = None
        self.site_data = None
        self.batch_size = None
        
    def load_page(self, url, css_class='result-info'):
        self.url = url
        self.page = requests.get(self.url)
        self.soup = BeautifulSoup(self.page.text, 'html.parser')
        self.raw_page_data = self.soup.find_all(class_=css_class)
        self.batch_size = len(self.raw_page_data)
        self.total_count = int(self.soup.find(class_='totalcount').get_text())
        
    def _get_page_data(self):
        tmp_data = list()
        for page in self.raw_page_data:
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
            
        self.clean_page_data = pd.DataFrame(tmp_data, 
                                    columns=['TITRE', 'PRIX', 'M2_ET_PIECES', 'ARR', 'LINK'])
        del tmp_data
        return self.clean_page_data
    
    def get_site_data(self):
        start_time = dt.now()
        self.load_page('https://paris.craigslist.org/d/logement-%C3%A0-louer/search/apa')
        self.site_data = self._get_page_data()
        for idx in range(self.batch_size, self.total_count, self.batch_size):
            new_url = 'https://paris.craigslist.org/search/apa?s=%i' % idx
            self.load_page(new_url)
            self.site_data = pd.concat((self.site_data, self._get_page_data()), axis=0)
            
        elapsed = (dt.now() - start_time).seconds
        print('Collected %i records in %i seconds.' % (self.site_data.shape[0], elapsed))
        return self.site_data
            
