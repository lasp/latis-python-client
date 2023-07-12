"""
A script to retrieve and manipulate datasets from a LaTiS instance.

This script provides functionality to retrieve the dataset in either numpy
or pandas format, and optionally download the dataset to a file.
"""

import logging
import numpy as np
import pandas as pd
import requests
import urllib.parse

from typing import List, Dict, Any, Union, Optional

FORMAT = '[%(levelname)s: %(filename)s: %(funcName)s: %(lineno)d]: \n %(message)s \n'
logging.basicConfig(format=FORMAT)

def _datasetWillUseVersion3(baseUrl: str, dataset: str, preferVersion2: bool) -> bool:
    """Checks which version of LaTiS dataset will be used.

    Args:
        baseUrl (str): The base URL of the LaTiS instance.
        dataset (str): The name of the dataset.
        preferVersion2 (bool): If True, prefer LaTiS version 2.

    Returns:
        bool: True if dataset will use LaTiS version 3, False otherwise.
    """

    if preferVersion2:
        try:
            instanceV2 = LatisInstance(baseUrl, False)
            instanceV2.getDataset(dataset)

            return False
        except Exception:
            logging.warning(dataset +
                  " cannot be accessed through LaTiS version 2." +
                  " Auto switching to version 3.")

            return True
    else:
        try:
            instanceV3 = LatisInstance(baseUrl, True)
            instanceV3.getDataset(dataset)

            return True
        except Exception:
            logging.warning(dataset +
                  " cannot be accessed through LaTiS version 3." +
                  " Auto switching to version 2.")

            return False

def _checkQuery(query, expectTextError=True):
    """Checks to see if query will return an error from LaTiS.

    Args:
        query (str): The query to be checked.
        expectTextError (bool, optional): 
            Error is expected in request text if True.
            Error is expected only via a status code if False.

    Returns:
        bool: True if query has no errors, False otherwise.
    """

    r = requests.get(query)
    if r.status_code > 399: # Is an error and not just a nominal status code.
        if expectTextError:
            logging.error("Query is invalid: " + query + "\r\n Got: " + r.text)
        else:
            logging.error("Query is invalid: " + query + " Got: " + str(r.status_code))
        return False
    else:
        return True

def data(baseUrl: str, dataset: str, returnType: str,
         projections: Optional[List[str]] = None,
         selections: Optional[List[str]] = None,
         operations: Optional[List[str]] = None,
         preferVersion2: bool = False) -> Union[np.ndarray, pd.DataFrame, None]:
    """
    Retrieves a dataset from LaTiS instance.

    This method fetches the dataset data from a LaTiS instance and
    transforms it into the specified format.

    Args:
        baseUrl (str): The base URL of the LaTiS instance.
        dataset (str): The name of the dataset.
        returnType (str): Desired return type ('NUMPY' or 'PANDAS').
        projections (list[str], optional): List of projections to use.
        selections (list[str], optional): List of selections to use.
        operations (list[str], optional): List of operations to apply.
        preferVersion2 (bool, optional): If True, prefer LaTiS version 2.

    Returns:
        np.ndarray or pandas.DataFrame or None: Dataset data.
    """

    latis3 = _datasetWillUseVersion3(baseUrl, dataset, preferVersion2)
    instance = LatisInstance(baseUrl, latis3)
    dsObj = instance.getDataset(dataset, projections, selections, operations)

    returnType = returnType.upper()

    if returnType == 'NUMPY':
        return dsObj.asNumpy()
    elif returnType == 'PANDAS':
        return dsObj.asPandas()
    else:
        return None


def download(baseUrl: str, dataset: str, filename: str, fileFormat: str,
             projections: Optional[List[str]] = None,
             selections: Optional[List[str]] = None,
             operations: Optional[List[str]] = None,
             preferVersion2: bool = False) -> None:
    """Downloads a dataset from LaTiS instance to file.

    Args:
        baseUrl (str): The base URL of the LaTiS instance.
        dataset (str): The name of the dataset.
        filename (str): The name of the file to download.
        fileFormat (str): The format of the file to download.
        projections (list[str], optional): List of projections to use.
        selections (list[str], optional): List of selections to use.
        operations (list[str], optional): List of operations to apply.
        preferVersion2 (bool, optional): If True, prefer LaTiS version 2.
    """

    latis3 = _datasetWillUseVersion3(baseUrl, dataset, preferVersion2)
    instance = LatisInstance(baseUrl, latis3)
    dsObj = instance.getDataset(dataset, projections, selections, operations)
    dsObj.getFile(filename, fileFormat)


class LatisInstance:
    """Represents a LaTiS instance.

    This class represents a LaTiS instance with a specified base URL
    and version (indicated by latis3 attribute).

    Attributes:
        baseUrl (str): The base URL of the LaTiS instance,
            passed to the constructor.
        latis3 (bool): True if LaTiS version 3 is used, False otherwise,
            passed to the constructor.
        catalog (Catalog): Stores catalog object.

    Args:
        baseUrl (str): The base URL of the LaTiS instance.
        latis3 (bool): True if LaTiS version 3 is to be used,
            False otherwise.
    """

    def __init__(self, baseUrl: str, latis3: bool):

        self.baseUrl: str = baseUrl
        self.latis3: bool = latis3
        self._formatBaseUrl()

        self.catalog: Catalog = self._getCatalog()

    def getDataset(self, name: str,
                   projections: Optional[List[str]] = None,
                   selections: Optional[List[str]] = None,
                   operations: Optional[List[str]] = None) -> "Dataset":
        """
        Creates and returns a Dataset object.

        Args:
            name (str): LaTiS dataset name (ex: 'cls_radio_flux_f8').
            projections (list[str], optional): List of projections
                to use.
            selections (list[str], optional): List of selections to use.
            operations (list[str], optional): List of operations to apply.

        Returns:
            latis.Dataset: Dataset object
        """
        return Dataset(self, name, projections, selections, operations)

    def _formatBaseUrl(self) -> None:
        """
        Appends dap2 or dap3 depending on LaTiS version.
        """
        if not self.baseUrl[-1] == '/':
            self.baseUrl += '/'
        if self.latis3:
            self.baseUrl += 'dap2/'
        else:
            self.baseUrl += 'dap/'

    def _getCatalog(self) -> "Catalog":
        return Catalog(self)


class Catalog:
    """Catalog for a LaTiS instance.

    Attributes:
        datasets (dict of {str: str}): A dictionary mapping formatted
            dataset names to their LaTiS names.
        list (np.ndarray): List of all dataset LaTiS names in catalog.
    """

    def __init__(self, latisInstance: LatisInstance):
        """Initializes the Catalog Object.

        Populates a dictionary and list of avaiable datasets.

        Args:
            latisInstance (LatisInstance): The LaTiS instance to get
                a catalog from.
        """

        self.datasets: dict = {}
        self.list: np.ndarray[str, np.dtype[Any]]

        if latisInstance.latis3:
            if _checkQuery(latisInstance.baseUrl, expectTextError=False):
                js = requests.get(latisInstance.baseUrl).json()
                dataset = js['dataset']
                titles = np.array([k['title'] for k in dataset])
                self.list = np.array([k['identifier'] for k in dataset])
                for i in range(len(self.list)):
                    self.datasets[titles[i]] = self.list[i]
            else:
                logging.error("Cannot populate catalog. Query was None.")
                self.list = np.array([])
        else:
            q = latisInstance.baseUrl + 'catalog.csv'
            if _checkQuery(q):
                df = pd.read_csv(q)
                names = df['name']
                self.list = df['accessURL'].to_numpy()
                for i in range(len(self.list)):
                    self.datasets[names[i]] = self.list[i]
            else:
                logging.error("Cannot populate catalog. Query was None.")
                self.list = np.array([])

    def search(self, searchTerm: str) -> "np.ndarray":
        """
        Filters the catalog by a search term.

        If the search term is an empty string or None, returns all
        datasets in the catalog.

        Args:
            searchTerm (str): The term to filter the catalog by.

        Returns:
            list: Defines a filtered list of dataset LaTiS names.
        """

        if searchTerm:
            return np.array([k for k in self.list if searchTerm in k])
        else:
            return self.list


class Dataset:
    """A class that represents a dataset from a LaTiS instance.

    Attributes:
        latisInstance (LatisInstance): The LaTiS instance object.
        name (str): The name of the dataset.
        projections (list): The list of projections for the dataset.
        selections (list): The list of selections for the dataset.
        operations (list): The list of operations for the dataset.
        query (str): The built query for the dataset.
        metadata (Metadata): Metadata object.
    """

    def __init__(self, latisInstance: LatisInstance, name: str,
                 projections: Optional[List[str]] = None,
                 selections: Optional[List[str]] = None,
                 operations: Optional[List[str]] = None):
        """Initializes the Dataset object and Metadata object.

        Initilizes lists of projections, selections and operations.
        By default these will be empty lists.

        Args:
            latisInstance (LatisInstance): The LaTiS instance from which to
                access this dataset.
            name (str): The name of the dataset.
            projections (list[str], optional): List of projections
                to use.
            selections (list[str], optional): List of selections to use.
            operations (list[str], optional): List of operations to apply.
        """

        self.latisInstance: LatisInstance = latisInstance
        self.name: str = name
        self.projections: list[str] = [] if projections is None else projections
        self.selections: list[str] = [] if selections is None else selections
        self.operations: list[str] = [] if operations is None else operations
        self.query: str = ""

        self.metadata: Metadata = Metadata(latisInstance, self)
        self.buildQuery()

    def select(self, target: str = "time", start: str = "", end: str = "",
               inclusiveStart: bool = True, inclusiveEnd: bool = False) -> "Dataset":
        """
        Defines a selection parameters for the dataset query.

        Args:
            target (str, optional): Target parameter for selection.
                Defaults to 'time'.
            start (str, optional): Start bound for selection. Empty by default.
            end (str, optional): End bound for selection. Empty by default.
            inclusiveStart (bool, optional): If True, start bound is inclusive.
                Defaults to True.
            inclusiveEnd (bool, optional): If True, end bound is inclusive.
                Defaults to False.

        Returns:
            Dataset: The Dataset instance, allowing for method chaining.
        """

        if start:
            startBound = ">" if not inclusiveStart else ">="
            select = target + startBound + str(start)
            self.selections.append(select)

        if end:
            endBound = "<" if not inclusiveEnd else "<="
            select = target + endBound + str(end)
            self.selections.append(select)

        return self

    def project(self, projectionList: list[str]) -> "Dataset":
        """
        Appends a projection list for the dataset query.

        Args:
            projectionList (list[str]): List of projections.

        Returns:
            Dataset: The Dataset instance, allowing for method chaining.
        """

        for p in projectionList:
            self.projections.append(p)
        return self

    def operate(self, operation: str) -> "Dataset":
        """
        Append an operation for the dataset query.

        Args:
            operation (str): Define LaTiS operation.

        Returns:
            Dataset: The Dataset instance, allowing for method chaining.
        """

        self.operations.append(operation)
        return self

    def buildQuery(self) -> str:
        """
        Builds the query for the LaTiS API using the selections,
        projections and operations added.

        Returns:
            str: Query for the LaTiS API.
        """

        self.query = self.latisInstance.baseUrl + self.name + '.csv?'

        self.query += ','.join(urllib.parse.quote(p) for p in self.projections)

        for s in self.selections:
            self.query = self.query + '&' + urllib.parse.quote(s)

        for o in self.operations:
            self.query = self.query + '&' + urllib.parse.quote(o)

        if not _checkQuery(self.query):
            self.query = ""
        
        return self.query

    def asPandas(self) -> Union[pd.DataFrame, None]:
        """
        Returns data from LaTiS API as pandas dataframe.

        Returns:
            pandas.DataFrame: Data as pandas dataframe.
        """

        if self.buildQuery():
            return pd.read_csv(self.query)
        else:
            return None

    def asNumpy(self) -> Union[np.ndarray, None]:
        """
        Returns data from LaTiS API as numpy array.

        Returns:
            np.ndarray: Data as numpy array.
        """

        if self.buildQuery():
            return pd.read_csv(self.query).to_numpy()
        else:
            return None

    def getFile(self, filename: str, format: str = 'csv') -> None:
        """
        Writes the dataset data to a local file.

        A format such as 'csv' may be specified.

        Args:
            filename (str): Name of file.
            format (str): Format of file. Defaults to 'csv'.
        """

        
        validFormats = ['asc', 'bin', 'csv', 'das', 'dds', 'dods', 'html', 'json', 'jsona', 'jsond', 'nc', 'tab', 'txt', 'zip', 'zip3']

        if format in validFormats:
            if self.buildQuery():
                suffix = '.' + format
                if '.' not in filename:
                    filename += suffix

                if filename is not None:
                    csv = requests.get(self.query.replace('.csv', suffix)).text
                    f = open(filename, 'w')
                    f.write(csv)
            else:
                logging.error("Cannot create file. Query was none. Check that dataset is valid.")
        else:
            logging.error("Cannot create file. " + format + " is not a valid LaTiS format. Valid formats are: " + str(validFormats))
            

    def clearProjections(self) -> None:
        """Clears the list of projections for the dataset."""
        self.projections = []

    def clearSelections(self) -> None:
        """Clears the list of selections for the dataset."""
        self.selections = []

    def clearOperations(self) -> None:
        """Clears the list of operations for the dataset."""
        self.operations = []


class Metadata:
    """A class that represents metadata for a dataset.

    Attributes:
        properties (dict): A dictionary of metadata properties of the dataset,
            where keys are variable identifiers, and values are the respective
            variable metadata.
    """

    def __init__(self, latisInstance: LatisInstance, dataset: Dataset):
        """Initializes the Metadata object; retrieves the metadata properties.

        Retrieves metadata from the provided LaTiS instance and dataset. The
        retrieval method depends on the version of LaTiS being used.

        Args:
            latisInstance (LatisInstance): The LaTiS instance from which to
                retrieve metadata.
            dataset (Dataset): The dataset for which to retrieve metadata.
        """

        self.properties: dict = {}

        if latisInstance.latis3:
            q = latisInstance.baseUrl + dataset.name + '.meta'
            if _checkQuery(q):
                variables = pd.read_json(q)['variable']
                for i in range(len(variables)):
                    self.properties[variables[i]['id']] = variables[i]
            else:
                logging.error("Cannot populate metadata. Query was None.")
        else:
            q = latisInstance.baseUrl + dataset.name + '.jsond?first()'
            if _checkQuery(q):
                self.properties = pd.read_json(q).iloc[1][0]
            else:
                logging.error("Cannot populate metadata. Query was None.")
