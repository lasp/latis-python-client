"""
This script allows for retrieving and manipulating datasets
from a Latis instance. It provides functionality to retrieve
the dataset in either numpy or pandas format, and optionally
download the dataset to a file.
"""

import numpy
import pandas as pd
import requests
import urllib.parse


def __datasetWillUseVersion3(baseUrl, dataset, preferVersion2):
    """Check which version of Latis dataset will be used.

    Args:
        baseUrl (str): The base URL of the Latis instance.
        dataset (str): The name of the dataset.
        preferVersion2 (bool): If True, prefer Latis version 2.

    Returns:
        bool: True if dataset will use Latis version 3, False otherwise.
    """

    if preferVersion2:
        try:
            instanceV2 = LatisInstance(baseUrl, False)
            instanceV2.getDataset(dataset)

            return False
        except Exception:
            print("[WARN]: " + dataset +
                  " cannot be accessed through Latis version 2." +
                  " Auto switching to version 3.")

            return True
    else:
        try:
            instanceV3 = LatisInstance(baseUrl, True)
            instanceV3.getDataset(dataset)

            return True
        except Exception:
            print("[WARN]: " + dataset +
                  " cannot be accessed through Latis version 3." +
                  " Auto switching to version 2.")

            return False


def data(baseUrl, dataset, returnType,
         projections=[], selections=[], operations=[], preferVersion2=False):
    """Retrieve dataset from Latis instance.

    Args:
        baseUrl (str): The base URL of the Latis instance.
        dataset (str): The name of the dataset.
        returnType (str): Desired return type ('NUMPY' or 'PANDAS').
        projections (list, optional): List of projections to use.
        selections (list, optional): List of selections to use.
        operations (list, optional): List of operations to apply.
        preferVersion2 (bool, optional): If True, prefer Latis version 2.

    Returns:
        numpy.ndarray or pandas.DataFrame or None: Dataset data.
    """

    latis3 = __datasetWillUseVersion3(baseUrl, dataset, preferVersion2)
    instance = LatisInstance(baseUrl, latis3)
    dsObj = instance.getDataset(dataset, projections, selections, operations)

    if returnType == 'NUMPY':
        return dsObj.asNumpy()
    elif returnType == 'PANDAS':
        return dsObj.asPandas()
    else:
        return None


def download(baseUrl, dataset, filename, fileFormat,
             projections=[], selections=[], operations=[],
             preferVersion2=False):
    """Download dataset from Latis instance to file.

    Args:
        baseUrl (str): The base URL of the Latis instance.
        dataset (str): The name of the dataset.
        filename (str): The name of the file to download.
        fileFormat (str): The format of the file to download.
        projections (list, optional): List of projections to use.
        selections (list, optional): List of selections to use.
        operations (list, optional): List of operations to apply.
        preferVersion2 (bool, optional): If True, prefer Latis version 2.
    """

    latis3 = __datasetWillUseVersion3(preferVersion2)
    instance = LatisInstance(baseUrl, latis3)
    dsObj = instance.getDataset(dataset, projections, selections, operations)
    dsObj.getFile(filename, fileFormat)


class LatisInstance:
    """A class that represents a Latis instance.

    Attributes:
        baseUrl (str): The base URL of the Latis instance.
        latis3 (bool): True if Latis version 3 is used, False otherwise.
        catalog (Catalog): Stores catalog object.

    Args:
        baseUrl (str): The base URL of the Latis instance.
        latis3 (bool): True if Latis version 3 is to be used, False otherwise.
    """

    def __init__(self, baseUrl, latis3):
        self.baseUrl = baseUrl
        self.latis3 = latis3
        self.__formatBaseUrl()

        self.catalog = self.__getCatalog()

    def getDataset(self, name, projections=[], selections=[], operations=[]):
        """Creates and returns a Dataset object

        Args:
            name (str): Latis dataset name (ex: 'cls_radio_flux_f8').
            projections (list, optional): List of projections to use.
            selections (list, optional): List of selections to use.
            operations (list, optional): List of operations to apply.

        Returns:
            latis.Dataset: Dataset object
        """
        return Dataset(self, name, projections, selections, operations)

    def __formatBaseUrl(self):
        """
        Appends dap2 or dap3 depending on latis version.
        """
        if not self.baseUrl[-1] == '/':
            self.baseUrl += '/'
        if self.latis3:
            self.baseUrl += 'dap2/'
        else:
            self.baseUrl += 'dap/'

    def __getCatalog(self):
        return Catalog(self)


class Catalog:
    """Catalog for a Latis instance.

    Attributes:
        datasets (dict): Dictionary: {Formatted name: latis name}.
        list (numpy.ndarray): List of all dataset latis names in catalog.

    Args:
        latisInstance (LatisInstance): The Latis instance.
    """

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
        """
        Filter catalog by search term.

        Args:
            searchTerm (str, optional): Filter term for catalog.

        Returns:
            list: Filtered catalog of latis names.
        """

        if searchTerm:
            return [k for k in self.list if searchTerm in k]
        else:
            return self.list


class Dataset:
    """A class that represents a dataset from a Latis instance.

    Attributes:
        latisInstance (LatisInstance): The Latis instance object.
        name (str): The name of the dataset.
        projections (list): The list of projections for the dataset.
        selections (list): The list of selections for the dataset.
        operations (list): The list of operations for the dataset.
        query (str): The built query for the dataset.
        metadata (Metadata): Metadata object.

    Args:
        latisInstance (LatisInstance): The Latis instance.
        name (str): The name of the dataset.
        projections (list, optional): List of projections to use.
        selections (list, optional): List of selections to use.
        operations (list, optional): List of operations to apply.
    """

    def __init__(self, latisInstance, name,
                 projections=[], selections=[], operations=[]):
        self.latisInstance = latisInstance
        self.name = name
        self.projections = list(projections)
        self.selections = list(selections)
        self.operations = list(operations)
        self.query = None

        self.metadata = Metadata(latisInstance, self)
        self.buildQuery()

    def select(self, target="time", start="", end="", inclusive=True):
        """
        Define selection parameters for the dataset query.

        Args:
            target (str, optional): Target parameter for selection.
                Defaults to 'time'.
            start (str, optional): Start bound for selection. Empty by default.
            end (str, optional): End bound for selection. Empty by default.
            inclusive (bool, optional): If True, bounds are inclusive.
                Defaults to True.

        Returns:
            Dataset: The Dataset instance, allowing for method chaining.
        """

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
        """
        Append a projection list for the dataset query.

        Args:
            projectionList (list): List (str) of projections.

        Returns:
            Dataset: The Dataset instance, allowing for method chaining.
        """

        for p in projectionList:
            self.projections.append(p)
        return self

    def operate(self, operation):
        """
        Append an operation for the dataset query.

        Args:
            operation (str): Define Latis operation.

        Returns:
            Dataset: The Dataset instance, allowing for method chaining.
        """

        self.operations.append(operation)
        return self

    def buildQuery(self):
        """
        Builds the query for the Latis API using the selections,
        projections and operations added.

        Returns:
            str: Query for the Latis API.
        """

        self.query = self.latisInstance.baseUrl + self.name + '.csv?'

        self.query += ','.join(urllib.parse.quote(p) for p in self.projections)

        for s in self.selections:
            self.query = self.query + '&' + urllib.parse.quote(s)

        for o in self.operations:
            self.query = self.query + '&' + urllib.parse.quote(o)

        return self.query

    def asPandas(self):
        """
        Returns data from Latis API as pandas dataframe.

        Returns:
            pandas.DataFrame: Data as pandas dataframe.
        """

        self.buildQuery()
        return pd.read_csv(self.query)

    def asNumpy(self):
        """
        Returns data from Latis API as numpy array.

        Returns:
            numpy.ndarray: Data as numpy array.
        """

        self.buildQuery()
        return pd.read_csv(self.query).to_numpy()

    def getFile(self, filename, format='csv'):
        """
        Downloads file of Latis data in specified format.

        Args:
            filename (str): Name of file.
            format (str): Format of file. Defaults to 'csv'.
        """

        self.buildQuery()
        suffix = '.' + format
        if '.' not in filename:
            filename += suffix

        if filename is not None:
            csv = requests.get(self.query.replace('.csv', suffix)).text
            f = open(filename, 'w')
            f.write(csv)

    def clearProjections(self):
        """
        Clears projections list.
        """
        self.projections = []

    def clearSelections(self):
        """
        Clears selections list.
        """
        self.selections = []

    def clearOperations(self):
        """
        Clears operations list.
        """
        self.operations = []


class Metadata:
    """A class that represents metadata for a dataset.

    Attributes:
        properties (dict): The metadata properties of the dataset.

    Args:
        latisInstance (LatisInstance): The Latis instance.
        dataset (Dataset): The dataset.
    """

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
