import numpy
import pandas as pd
import requests
import urllib.parse


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

        self.datasets = {}

        if latisInstance.latis3:
            js = requests.get(latisInstance.baseUrl).json()
            dataset = js['dataset']
            titles = numpy.array([k['title'] for k in dataset])
            self.list = numpy.array([k['identifier'] for k in dataset])
            for i in range(len(self.list)):
                self.datasets[titles[i]] = self.list[i]
        else:
            q = latisInstance.baseUrl + 'catalog.csv'
            df = pd.read_csv(q)
            names = df['name']
            self.list = df['accessURL'].to_numpy()
            for i in range(len(self.list)):
                self.datasets[names[i]] = self.list[i]

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
        self.buildQuery()

    def buildQuery(self, projection=[], selection=[], operation=[]):
        self.query = self.latisInstance.baseUrl + self.name + '.csv?'

        for p in projection:
            self.query = self.query + urllib.parse.quote(p) + ','

        for s in selection:
            self.query = self.query + urllib.parse.quote(s) + '&'

        for o in operation:
            self.query = self.query + urllib.parse.quote(o) + '&'

        return self.query

    def asPandas(self):
        return pd.read_csv(self.query, parse_dates=[0], index_col=[0])
    
    def asNumpy(self):
        return pd.read_csv(self.query, parse_dates=[0],
                               index_col=[0]).to_numpy()

    def getFile(self, filename, format='csv'):
        suffix = '.' + format
        if filename is not None:
            csv = requests.get(self.query.replace('.csv', format)).text
            trueFilename = filename + format if '.' not in filename else filename
            f = open(trueFilename, 'w')
            f.write(csv)


class Metadata:

    def __init__(self, latisInstance, dataset):

        self.properties = {}

        if latisInstance.latis3:
            q = latisInstance.baseUrl + dataset.name + '.meta'
            print(q)
            variables = pd.read_json(q)['variable']
            for i in range(len(variables)):
                self.properties[variables[i]['id']] = variables[i]
        else:
            q = latisInstance.baseUrl + dataset.name + '.jsond?first()'
            self.properties = pd.read_json(q).iloc[1][0]
