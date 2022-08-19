from dataclasses import dataclass

import numpy
import pandas as pd
import requests

@dataclass
class Config:
    baseUrl: str
    latis3: bool
    dataset: str

class LatisDataset:

    def __init__(self, config):
        self.config = config

        self.projection=[]
        self.selection=[]
        self.operation=[]

        self.__formatBaseUrl()
        self.__createQuery()

    def getBaseUrl(self):
        return self.config.baseUrl

    def getQuery(self):
        return self.query

    def getCatalog(self, searchTerm=None):
        if self.config.latis3:
            js = requests.get(self.config.baseUrl).json()
            dataset = js['dataset']
            self.catalog = numpy.array([k['identifier'] for k in dataset])
        else:
            q = self.config.baseUrl + 'catalog.csv'
            df = pd.read_csv(q, parse_dates=[0], index_col=[0])
            self.catalog = df['accessURL'].to_numpy()

        if searchTerm:
            self.catalog = [k for k in self.catalog if searchTerm in k]
        
        return self.catalog

    def getMetadata(self):
        if self.config.latis3:
            q = self.config.baseUrl + self.config.dataset + '.meta'
            self.metadata = pd.read_json(q)
        else:
            q = self.config.baseUrl + self.config.dataset + '.jsond?first()'
            self.metadata = pd.read_json(q).iloc[1][0]

        return self.metadata
        
    def project(self, projection=[]):
        self.projection = projection
        self.__createQuery()

    def select(self, selection=[]):
        self.selection = selection
        self.__createQuery()

    def operate(self, operation=[]):
        self.operation = operation
        self.__createQuery()

    def toDataFrame(self):
        print(self.query)
        return pd.read_csv(self.query, parse_dates=[0], index_col=[0])

    def __formatBaseUrl(self):
        if not self.config.baseUrl[-1] == '/':
            self.config.baseUrl += '/'
        if self.config.latis3:
            self.config.baseUrl += 'dap2/'
        else:
            self.config.baseUrl += 'dap/'

    def __createQuery(self):
        self.query = self.config.baseUrl + self.config.dataset + '.csv?'

        for p in self.projection:
            self.query = self.query + p + ','
        
        for s in self.selection:
            self.query = self.query + s + '&'

        for o in self.operation:
            self.query = self.query + o + '&'
        
