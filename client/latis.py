import numpy
import pandas as pd
import requests
import urllib.parse


def data(baseUrl, latis3, dataset, returnType, operations=[]):
    instance = LatisInstance(baseUrl, latis3)
    dsObj = instance.getDataset(dataset)
    for o in operations:
        dsObj.operate(o)
    if returnType == 'NUMPY':
        return dsObj.asNumpy()
    elif returnType == 'PANDAS':
        return dsObj.asPandas()
    else:
        return None

class LatisInstance:

    def __init__(self, baseUrl, latis3):
        self.baseUrl = baseUrl
        self.latis3 = latis3
        self.__formatBaseUrl()

        self.catalog = self.__getCatalog()

    def getDataset(self, name):
        return Dataset(self, name)

    def __formatBaseUrl(self):
        if not self.baseUrl[-1] == '/':
            self.baseUrl += '/'
        if self.latis3:
            self.baseUrl += 'dap2/'
        else:
            self.baseUrl += 'dap/'

    def __getCatalog(self):
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
        self.operation = []
        self.query = None

        self.metadata = Metadata(latisInstance, self)
        self.buildQuery()

    def operate(self, operation):
        self.operation.append(operation)
        self.buildQuery()
        return self

    def buildQuery(self):
        self.query = self.latisInstance.baseUrl + self.name + '.csv?'

        for o in self.operation:
            self.query = self.query + urllib.parse.quote(o) + '&'

        return self.query

    def asPandas(self):
        return pd.read_csv(self.query, parse_dates=[0], index_col=[0])

    def asNumpy(self):
        return pd.read_csv(self.query, parse_dates=[0],
                           index_col=[0]).to_numpy()

    def getFile(self, filename, format='csv'):
        suffix = '.' + format
        if '.' not in filename:
            filename += suffix

        if filename is not None:
            csv = requests.get(self.query.replace('.csv', suffix)).text
            f = open(filename, 'w')
            f.write(csv)


class Metadata:

    def __init__(self, latisInstance, dataset):

        self.properties = {}

        if latisInstance.latis3:
            q = latisInstance.baseUrl + dataset.name + '.meta'
            variables = pd.read_json(q)['variable']
            for i in range(len(variables)):
                self.properties[variables[i]['id']] = variables[i]
        else:
            q = latisInstance.baseUrl + dataset.name + '.jsond?first()'
            self.properties = pd.read_json(q).iloc[1][0]
