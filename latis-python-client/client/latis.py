from dataclasses import dataclass

import numpy
import pandas as pd
import requests

@dataclass
class Config:
    baseUrl: str
    latis3: bool
    dataset: str
    manualOption: str

class LatisDataset:

    def __init__(self, config):
        self.config = config

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

    def getMetadata(self, structureData=False):
        if self.config.latis3:
            q = self.config.baseUrl + self.config.dataset + '.meta'
            self.metadata = pd.read_json(q)

            self.structdata = None #FIX LATER
        else:
            q = self.config.baseUrl + self.config.dataset + '.das'
            self.metadata = requests.get(q).text
            q = self.config.baseUrl + self.config.dataset + '.dds'
            self.structdata = requests.get(q).text

        if structureData:
            return self.structdata
        else:
            return self.metadata

    def select(self, constraint):
        q = self.query + constraint
        r = requests.get(q).text
        return r

    def toDataFrame(self, constraint):
        q = self.query + constraint
        return pd.read_csv(q, parse_dates=[0], index_col=[0])

    def __formatBaseUrl(self):
        if not self.config.baseUrl[-1] == '/':
            self.config.baseUrl += '/'
        if self.config.latis3:
            self.config.baseUrl += 'dap2/'
        else:
            self.config.baseUrl += 'dap/'

    def __createQuery(self):
        self.query = self.config.baseUrl + self.config.dataset + '.csv?'
        if self.config.manualOption:
            self.query += self.config.manualOption
