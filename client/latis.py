import numpy
import pandas as pd
import requests
import urllib.parse
    

def __datasetWillUseVersion3(baseUrl, dataset, preferVersion2):
    if preferVersion2:
        try:
            instanceV2 = LatisInstance(baseUrl, False)
            dsObj = instanceV2.getDataset(dataset)
            
            return False
        except:
            print("[WARN]: " + dataset + " cannot be accessed through Latis version 2. Auto switching to version 3.")

            return True
    else:
        try:
            instanceV3 = LatisInstance(baseUrl, True)
            dsObj = instanceV3.getDataset(dataset)

            return True
        except:
            print("[WARN]: " + dataset + " cannot be accessed through Latis version 3. Auto switching to version 2.")

            return False


def data(baseUrl, dataset, returnType, projections=[], selections=[], operations=[], preferVersion2=False):
    latis3 = __datasetWillUseVersion3(baseUrl, dataset, preferVersion2)
    instance = LatisInstance(baseUrl, latis3)
    dsObj = instance.getDataset(dataset, projections, selections, operations)

    if returnType == 'NUMPY':
        return dsObj.asNumpy()
    elif returnType == 'PANDAS':
        return dsObj.asPandas()
    else:
        return None

def download(baseUrl, dataset, filename, fileFormat, projections, selections, operations, preferVersion2=False):
    latis3 = __datasetWillUseVersion3(preferVersion2)
    instance = LatisInstance(baseUrl, latis3)
    dsObj = instance.getDataset(dataset, projections, selections, operations)
    dsObj.getFile(filename, fileFormat)
  
class LatisInstance:

    def __init__(self, baseUrl, latis3):
        self.baseUrl = baseUrl
        self.latis3 = latis3
        self.__formatBaseUrl()

        self.catalog = self.__getCatalog()

    def getDataset(self, name, projections=[], selections=[], operations=[]):
        return Dataset(self, name, projections, selections, operations)

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

    def __init__(self, latisInstance, name, projections=[], selections=[], operations=[]):
        self.latisInstance = latisInstance
        self.name = name
        self.projections = list(projections)
        self.selections = list(selections)
        self.operations = list(operations)
        self.query = None

        self.metadata = Metadata(latisInstance, self)
        self.buildQuery()

    def select(self, target="time", start="", end="", inclusive=True):
        
        if start:
            startBound = ">" if inclusive else ">="
            select = target + startBound + str(start)
            self.selections.append(select)

        if end:
            endBound = "<" if inclusive else "<="
            select = target + endBound + str(end)
            self.selections.append(select)

        return self

    def project(self, projectionList):
        for p in projectionList:
            self.projections.append(p)
        return self

    def operate(self, operation):
        self.operations.append(operation)
        return self

    def buildQuery(self):
        self.query = self.latisInstance.baseUrl + self.name + '.csv?'

        for i in range(len(self.projections)):
            p = self.projections[i]
            self.query = self.query + urllib.parse.quote(p)
            if not i == len(self.projections) - 1:
                self.query = self.query + ','

        for s in self.selections:
            self.query = self.query + '&' + urllib.parse.quote(s)

        for o in self.operations:
            self.query = self.query + '&' + urllib.parse.quote(o)

        return self.query

    def asPandas(self):
        self.buildQuery()
        return pd.read_csv(self.query)

    def asNumpy(self):
        self.buildQuery()
        return pd.read_csv(self.query).to_numpy()

    def getFile(self, filename, format='csv'):
        self.buildQuery()
        suffix = '.' + format
        if '.' not in filename:
            filename += suffix

        if filename is not None:
            csv = requests.get(self.query.replace('.csv', suffix)).text
            f = open(filename, 'w')
            f.write(csv)

    def clearProjections(self):
        self.projections = []

    def clearSelections(self):
        self.selections = []

    def clearOperations(self):
        self.operations = []


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
