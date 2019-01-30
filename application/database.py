from .crawler import Crawler
from sqlalchemy import create_engine
import pandas as pd


class Database(object):

    def __init__(self):
        # self.column_names = ['listing_title', 'listing_price', 'listing_m2',
        #                      'listing_pieces', 'listing_neighborhood',
        #                      'link_to_listing']
        self.column_names = ['ID', 'TITRE', 'PRIX', 'ARR', 'LINK', 'M2', 'PIECES']
        self.crawler = Crawler()
        self.engine = create_engine('sqlite:///immeubles.sqlite3', echo=False)
        self.data = None
        self.params = {
            'name': 'immeubles',
            'con': self.engine,
            'if_exists': 'replace',
            'index': True,
            'index_label': 'ID'
        }
        self._initialize_database()

    def _initialize_database(self):
        self.data = self.crawler.get_site_data()
        self.data.to_sql(**self.params)

    def read(self):
        query_data = self.engine.execute("SELECT * FROM %s" % self.params['name']).fetchall()
        self.data = pd.DataFrame(data=query_data, columns=self.column_names)
        return self.data

    def create(self, titre, prix, arr, link, m2, pieces):
        query = "INSERT INTO %s (%s, %s, %s, %s, %s, %s, %s) VALUES (%i, '%s', '%s', '%s', '%s', '%s', '%s')" % \
                    (self.params['name'],
                     self.column_names[0],
                     self.column_names[1], self.column_names[2],
                     self.column_names[3], self.column_names[4],
                     self.column_names[5], self.column_names[6],
                     self.data.shape[0],
                     titre, prix, arr, link, m2, pieces)
        self.engine.execute(query)
        print('Added record #%i' % self.data.shape[0])
        return self.read()

    def update(self, id, titre, prix, arr, link, m2, pieces):
        update_values = ''.join(["{}='{}', ".format(column, value) for column, value in
                                 zip(self.column_names, [id, titre, prix, arr, link, m2, pieces])])
        query = "UPDATE %s SET %s WHERE ID=%i" % (self.params['name'], update_values[:-2], id)
        self.engine.execute(query)
        print('Updated record #%i' % id)
        return self.read()

    def delete(self, id):
        query = "DELETE FROM %s WHERE ID=%i" % (self.params['name'], id)
        self.engine.execute(query)
        print('Deleted record #%i' % id)
        return self.read()

    @staticmethod
    def export_to_csv(data, filename='apartment_data', compress=False):
        if compress:
            subfolder = './{}.xz'.format(filename)
            data.to_csv(path_or_buf=subfolder, index=False, compression='xz')
        else:
            subfolder = './{}.csv'.format(filename)
            data.to_csv(path_or_buf=subfolder, index=False)
