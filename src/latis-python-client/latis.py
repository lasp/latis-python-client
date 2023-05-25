import numpy
import pandas as pd
import requests
import urllib.parse


def __datasetWillUseVersion3(baseUrl, dataset, preferVersion2):
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
    """Shortcut function that directly returns data.
    
    This does not require the user to create a LatisInstance object, or Dataset object.
    Additionally, a latis version will be auto selected based on avaiablilty and prefrence.
    The data format can either be a Numpy array or Pandas dataframe.

    Args:
        baseUrl (str): 
            Latis base url (ex: 'https://lasp.colorado.edu/lisird/latis').
        dataset (str): 
            Latis dataset name (ex: 'cls_radio_flux_f8').
        returnType (str): 
            Specify numpy or pandas data format ('NUMPY' or 'PANDAS').
        projections (list, optional): 
            Stores list of projections for latis query. Each projection must be a list. Defaults to [].
        selections (list, optional): 
            Stores list of selections for latis query. Defaults to [].
        operations (list, optional): 
            Stores list of operations for latis query. Defaults to [].
        preferVersion2 (bool, optional): 
            Prefer latis version 2. If not avaiable will auto switch. Defaults to False.

    Returns:
        Return type depends on returnType value

        A returnType of 'NUMPY' will yeild:
            numpy.ndarray: Numpy data

        A returnType of 'PANDAS' will yeild:
            pandas.core.frame.DataFrame: Pandas data

        Anything else will return None.
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
             projections=[], selections=[], operations=[], preferVersion2=False):
    """Shortcut function to download data to a file.
    
    This does not require the user to create a LatisInstance object, or Dataset object.
    Additionally, a latis version will be auto selected based on avaiablilty and prefrence.
    The file format may be selected.

    Args:
        baseUrl (str):
            Latis base url (ex: 'https://lasp.colorado.edu/lisird/latis').
        dataset (str):
            Latis dataset name (ex: 'cls_radio_flux_f8').
        filename (str):
            Name of file downloaded.
        fileFormat (str):
            File format (ex: 'csv')
        projections (list, optional):
            Stores list of projections for latis query. Each projection must be a list. Defaults to [].
        selections (list, optional):
            Stores list of selections for latis query. Defaults to [].
        operations (list, optional):
            Stores list of operations for latis query. Defaults to [].
        preferVersion2 (bool, optional):
            Prefer latis version 2. If not avaiable will auto switch. Defaults to False.
    """
    latis3 = __datasetWillUseVersion3(preferVersion2)
    instance = LatisInstance(baseUrl, latis3)
    dsObj = instance.getDataset(dataset, projections, selections, operations)
    dsObj.getFile(filename, fileFormat)

    print(type(baseUrl), type(dataset), type(filename), type(fileFormat), type(projections), type(selections), type(operations), type(preferVersion2))


class LatisInstance:
    """Instantiates access latis catalogs and datasets.

    Attributes:
        baseUrl (str): 
            Latis base url (ex: 'https://lasp.colorado.edu/lisird/latis').
        latis3 (bool): 
            Select latis version 3 (True) or latis version 2 (False).
        catalog (latis.Catalog):
            Stores catalog object.
    """

    def __init__(self, baseUrl, latis3):
        """Init LatisInstance Object.

        Sets class baseUrl, latis3 parameters.
        Formats baseUrl (use dap vs dap2).
        Creates catalog object from LatisInstance.

        Args:
            baseUrl (str): 
                Latis base url (ex: 'https://lasp.colorado.edu/lisird/latis').
            latis3 (bool): 
                Select latis version 3 (True) or latis version 2 (False).
        """
        self.baseUrl = baseUrl
        self.latis3 = latis3
        self.__formatBaseUrl()

        self.catalog = self.__getCatalog()
        print(type(self.baseUrl), type(self.latis3), type(self.catalog))

    def getDataset(self, name, projections=[], selections=[], operations=[]):
        """Creates and returns a Dataset object

        Args:
            name (str): 
                Latis dataset name (ex: 'cls_radio_flux_f8').
            projections (list, optional):
                Stores list of projections for latis query. Each projection must be a list. Defaults to [].
            selections (list, optional):
                Stores list of selections for latis query. Defaults to [].
            operations (list, optional):
                Stores list of operations for latis query. Defaults to [].

        Returns:
            latis.Dataset: Dataset object
        """
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
    """Stores catalog datasets and privides a method to search for specific datasets.

    Attributes:
        datasets (dict):
            Dictionary of all datasets in the catalog with the format {Formatted name: latis name}.
        list (numpy.ndarray):
            List of all dataset latis names in catalog.

    """

    def __init__(self, latisInstance):
        """Init Catalog Object.

        Populates class datasets and list attributes.

        Args:
            latisInstance (latis.LatisInstance): LatisInstance object.
        """

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
        """Filter catalog by search term.

        Args:
            searchTerm (String): Filter term for catalog.

        Returns:
            list: Filtered catalog of latis names.
        """
        print(type(self.datasets), type(self.list))

        if searchTerm:
            return [k for k in self.list if searchTerm in k]
        else:
            return self.list


class Dataset:
    """Provides methods obtain a dataset content in various formats and apply projections, selections or operations.

     Attributes:
        latisInstance (laits.LatisInstance):
            
        name (str):
            
        projections (list):
            Stores list of projections for latis query. Each projection must be a list.
        selections (list):
            Stores list of selections for latis query.
        operations (list):
            Stores list of operations for latis query.
        query (str):
            Latis query.
        metadata (latis.Metadata):
            Metadata object.

    """

    def __init__(self, latisInstance, name,
                 projections=[], selections=[], operations=[]):
        """Init Dataset object

        Args:
            latisInstance (LatisInstance): 
                LatisInstance Object.
            name (String): 
                Latis dataset name.
            projections (list, optional):
                Stores list of projections for latis query. Each projection must be a list. Defaults to [].
            selections (list, optional):
                Stores list of selections for latis query. Defaults to [].
            operations (list, optional):
                Stores list of operations for latis query. Defaults to [].
        """
        self.latisInstance = latisInstance
        self.name = name
        self.projections = list(projections)
        self.selections = list(selections)
        self.operations = list(operations)
        self.query = None

        self.metadata = Metadata(latisInstance, self)
        self.buildQuery()

    def select(self, target="time", start="", end="", inclusive=True):
        """Adds selection to selection list

        Args:
            target (str, optional): _description_. Defaults to "time".
            start (str, optional): _description_. Defaults to "".
            end (str, optional): _description_. Defaults to "".
            inclusive (bool, optional): _description_. Defaults to True.

        Returns:
            _type_: _description_
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
        """Adds a projection list to query projection list

        Args:
            projectionList (list): _description_

        Returns:
            _type_: _description_
        """
        for p in projectionList:
            self.projections.append(p)
        return self

    def operate(self, operation):
        """Adds operation to query operation list

        Args:
            operation (String): _description_

        Returns:
            _type_: _description_
        """
        self.operations.append(operation)
        return self

    def buildQuery(self):
        """_summary_

        Returns:
            _type_: _description_
        """
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
        """_summary_

        Returns:
            _type_: _description_
        """
        self.buildQuery()
        return pd.read_csv(self.query)

    def asNumpy(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        self.buildQuery()
        return pd.read_csv(self.query).to_numpy()

    def getFile(self, filename, format='csv'):
        """_summary_

        Args:
            filename (_type_): _description_
            format (str, optional): _description_. Defaults to 'csv'.
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
        """Clears projections list
        """
        self.projections = []

    def clearSelections(self):
        """Clears selections list
        """
        self.selections = []

    def clearOperations(self):
        """Clears operations list
        """
        self.operations = []


class Metadata:
    """Metadata object
    """

    def __init__(self, latisInstance, dataset):
        """Init metadata object

        Populates properties attribute.

        Args:
            latisInstance (LatisInstance): 
                Stores LatisInstance object.
            dataset (Dataset): 
                Stores Dataset object.
        """
        self.properties = {}

        if latisInstance.latis3:
            q = latisInstance.baseUrl + dataset.name + '.meta'
            variables = pd.read_json(q)['variable']
            for i in range(len(variables)):
                self.properties[variables[i]['id']] = variables[i]
        else:
            q = latisInstance.baseUrl + dataset.name + '.jsond?first()'
            self.properties = pd.read_json(q).iloc[1][0]
