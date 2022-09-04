from dataclasses import dataclass

import numpy
import pandas as pd
import requests

class LatisInstance:

    def __init__(self, baseUrl, latis3):
        self.baseUrl = baseUrl
        self.latis3 = latis3
        self.__formatBaseUrl()
        
        self.catalog = self.__createCatalog()

    def createDataset(self, name):
        return Dataset(self, name)    

    def __formatBaseUrl(self):
        if not self.baseUrl[-1] == '/':
            self.baseUrl += '/'
        if self.latis3:
            self.baseUrl += 'dap2/'
        else:
            self.baseUrl += 'dap/'

    def __createCatalog(self):
        return Catalog(self)

class Catalog:
    
    def __init__(self, latisInstance):

        if latisInstance.latis3:
            js = requests.get(latisInstance.baseUrl).json()
            dataset = js['dataset']
            self.list = numpy.array([k['identifier'] for k in dataset])
        else:
            q = latisInstance.baseUrl + 'catalog.csv'
            print(q)
            df = pd.read_csv(q, parse_dates=[0], index_col=[0])
            self.list = df['accessURL'].to_numpy()

    def search(self, searchTerm):
        if searchTerm:
            return [k for k in self.list if searchTerm in k]
        else:
            return self.list

class Dataset:

    def __init__(self, latisInstance, name):
        self.latisInstance = latisInstance
        self.name = name
        self.query = None

        self.metadata = Metadata(latisInstance, self)

    def buildQuery(self, projection=[], selection=[], operation=[]):
        self.query = self.latisInstance.baseUrl + self.name + '.csv?'

        for p in projection:
            self.query = self.query + p + ','
        
        for s in selection:
            self.query = self.query + s + '&'

        for o in operation:
            self.query = self.query + o + '&'

        return self.query

    def getData(self, type='PANDAS'):
        if type == 'PANDAS':
            print(self.query)
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

class Metadata:

    def __init__(self, latisInstance, dataset):
        if latisInstance.latis3:
            q = latisInstance.baseUrl + dataset.name + '.meta'
            self.json = pd.read_json(q)
        else:
            q = latisInstance.baseUrl + dataset.name + '.jsond?first()'
            self.json = pd.read_json(q).iloc[1][0]
