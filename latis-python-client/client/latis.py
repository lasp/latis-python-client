from dataclasses import dataclass

import numpy
import pandas as pd
import requests

@dataclass
class Config:
    baseUrl: str
    latis3: bool
    dataset: str

class LatisInstance:

    def __init__(self, config):
        self.config = config

        self.projection=[]
        self.selection=[]
        self.operation=[]

        self.__createDataset(config.dataset)
        self.__formatBaseUrl()
        self.__buildQuery()
        self.__createCatalog()
        self.__createMetadata()
        
    def project(self, projection=[]):
        self.projection = projection
        self.__buildQuery()

    def select(self, selection=[]):
        self.selection = selection
        self.__buildQuery()

    def operate(self, operation=[]):
        self.operation = operation
        self.__buildQuery()

    def getData(self, type):
        if type == 'PANDAS':
            return pd.read_csv(self.query, parse_dates=[0], index_col=[0])
        elif type == 'NUMPY':
            return pd.read_csv(self.query, parse_dates=[0], index_col=[0]).to_numpy()
        else:
            return None
    
    def getFile(self, filename, suffix='.csv'):
        if not filename == None:
            csv = requests.get(self.query.replace('.csv', suffix)).text
            f = open(filename, 'w')
            f.write(csv)

    def getBaseUrl(self):
        return self.config.baseUrl

    def getQuery(self):
        return self.query

    def getCatalog(self, searchTerm=None):
        return self.catalog

    def getMetadata(self):
        return self.metadata

    def __formatBaseUrl(self):
        if not self.config.baseUrl[-1] == '/':
            self.config.baseUrl += '/'
        if self.config.latis3:
            self.config.baseUrl += 'dap2/'
        else:
            self.config.baseUrl += 'dap/'

    def __buildQuery(self):
        self.query = self.config.baseUrl + self.dataset.name + '.csv?'

        for p in self.projection:
            self.query = self.query + p + ','
        
        for s in self.selection:
            self.query = self.query + s + '&'

        for o in self.operation:
            self.query = self.query + o + '&'
        
    def __createDataset(self, dataset):
        self.dataset = Dataset(dataset)

    def __createCatalog(self):
        self.catalog = Catalog(self)

    def __createMetadata(self):
        self.metadata = Metadata(self)

class Catalog:
    
    def __init__(self, latisInstance):

        if latisInstance.config.latis3:
            js = requests.get(latisInstance.config.baseUrl).json()
            dataset = js['dataset']
            self.catalogList = numpy.array([k['identifier'] for k in dataset])
        else:
            q = latisInstance.config.baseUrl + 'catalog.csv'
            df = pd.read_csv(q, parse_dates=[0], index_col=[0])
            self.catalogList = df['accessURL'].to_numpy()

    def search(self, searchTerm):
        if searchTerm:
            return [k for k in self.catalogList if searchTerm in k]
        else:
            return self.catalogList

class Metadata:

    def __init__(self, latisInstance):
        if latisInstance.config.latis3:
            q = latisInstance.config.baseUrl + latisInstance.dataset.name + '.meta'
            self.json = pd.read_json(q)
        else:
            q = latisInstance.config.baseUrl + latisInstance.dataset.name + '.jsond?first()'
            self.json = pd.read_json(q).iloc[1][0]

class Dataset:

    def __init__(self, name):
        self.name = name

    def selectDataset(self, name):
        self.name = name