import os
import sys

#NOT UP TO DATE WITH latis.py do not use

libPath = os.path.dirname(os.path.realpath(__file__))
libPath = libPath.replace('/latis-python-client/tests',
                          '/latis-python-client/client')
sys.path.insert(0, libPath)

import latis

class latisTester:

    def __init__(self, verbosity=0):
        self.errorReport = {
            'total': 0,
            'latis2': 0,
            'latis3': 0,
            'instance': 0,
            'catalog': 0,
            'query': 0,
            'format': 0,
            'metadata': 0,
            'exception': 0
        }

        self.latis2Instance = None
        self.latis3Instance = None

        self.verbosity = verbosity

    def runTests(self, testConfig=None):
        if not testConfig:
            self.error('Configure test list!', None, None, False)
            return

        self.createLatisInstances(testConfig)
        self.getCatalogs(testConfig)
        self.createQueries(testConfig)
        self.formatData(testConfig)
        self.getMetadata(testConfig)
        return self.errorReport

    def createLatisInstances(self, testConfig):
        print('--[Instance]---------')
        try:
            if testConfig.latis2:
                self.info('Creating Latis2 Instance')
                self.latis2Instance = latis.LatisInstance(
                    baseUrl=testConfig.baseUrl)
                if self.latis2Instance:
                    self.info('Initilized Latis2')
                else:
                    self.error('Latis2 Instance returned None!',
                               'instance', 'latis2', False)
        except Exception as ex:
            print(ex)
            self.error('Exception Thrown!', 'instance', 'latis2', True)

        try:
            if testConfig.latis3:
                self.info('Creating Latis3 Instance')
                self.latis3Instance = latis.LatisInstance(
                    baseUrl=testConfig.baseUrl, latis3=True)
                if self.latis3Instance:
                    self.info('Initilized Latis3')
                else:
                    self.error('Latis3 Instance returned None!',
                               'instance', 'latis3', False)
        except Exception as ex:
            print(ex)
            self.error('Exception Thrown!', 'instance', 'latis3', True)

    def getCatalogs(self, testConfig):
        print('--[Catalog]---------')
        if not testConfig.catalogSearch:
            return

        for element in testConfig.catalogSearch:
            formattedSearchInfo = 'No search terms'
            if element:
                formattedSearchInfo = 'Using search term: ' + element
            self.info(formattedSearchInfo)
            try:
                if testConfig.latis2:
                    self.info('Getting Latis2 Catalog')
                    catalog = self.latis2Instance.getCatalog(element)
                    if len(catalog):
                        self.info('Got Latis2 Catalog')
                        print(catalog)
                    else:
                        self.error('Latis2 Catalog returned zero length!',
                                   'catalog', 'latis2', False)
            except Exception as ex:
                print(ex)
                self.error('Exception Thrown!', 'catalog', 'latis2', True)

            try:
                if testConfig.latis3:
                    self.info('Getting Latis3 Catalog')
                    catalog3 = self.latis3Instance.getCatalog(element)
                    if len(catalog3):
                        self.info('Got Latis3 Catalog')
                        print(catalog3)
                    else:
                        self.error('Latis3 Catalog returned zero length!',
                                   'catalog', 'latis3', False)
            except Exception as ex:
                print(ex)
                self.error('Exception Thrown!', 'catalog', 'latis3', True)

    def createQueries(self, testConfig):
        print('--[Query]------------')
        if not testConfig.queries:
            return

        for element in testConfig.queries:
            try:
                if testConfig.latis2:
                    self.info('Creating Latis2 query')
                    query = self.latis2Instance.query(
                                dataset=element['dataset'],
                                selection=element['selection'])
                    if query:
                        self.info('Created Latis2 query')
                        print(query)
                    else:
                        self.error('Latis2 query returned None!',
                                   'query', 'latis2', False)
            except Exception as ex:
                print(ex)
                self.error('Exception Thrown!', 'query', 'latis2', True)

            try:
                if testConfig.latis3:
                    self.info('Creating Latis3 query')
                    query3 = self.latis3Instance.query(
                        dataset=element['dataset'])
                    if query3:
                        self.info('Created Latis3 query')
                        print(query3)
                    else:
                        self.error('Latis3 query returned None!',
                                   'query', 'latis3', False)
            except Exception as ex:
                print(ex)
                self.error('Exception Thrown!', 'query', 'latis3', True)

    def formatData(self, testConfig):
        print('--[Format]-----------')
        if not testConfig.formats:
            return
        for element in testConfig.formats:
            try:
                if testConfig.latis2:
                    self.info('Formatting Latis2 data')
                    data = self.latis2Instance.formatDataPd(
                        dataset=element['dataset'],
                        selection=element['selection'])
                    if len(data):
                        self.info('Formatted Latis2 data')
                        print(data)
                    else:
                        self.error(
                            'Formatting Latis2 data returned zero length!',
                            'format', 'latis2', False)
            except Exception as ex:
                print(ex)
                self.error('Exception Thrown!', 'format', 'latis2', True)

            try:
                if testConfig.latis3:
                    self.info('Formatting Latis3 data')
                    data3 = self.latis3Instance.formatDataPd(
                        dataset=element['dataset'])
                    if len(data3):
                        self.info('Formatted Latis3 data')
                        print(data3)
                    else:
                        self.error(
                            'Formatting Latis3 data returned zero length!',
                            'format', 'latis3', False)
            except Exception as ex:
                print(ex)
                self.error('Exception Thrown!', 'format', 'latis3', True)

    def getMetadata(self, testConfig):
        print('--[Metadata]---------')
        if not testConfig.metadatas:
            return

        for element in testConfig.metadatas:
            try:
                if testConfig.latis2:
                    self.info('Getting Latis2 metadata')
                    metadata = self.latis2Instance.metadata(
                        dataset=element['dataset'])
                    if metadata:
                        self.info('Got Latis2 metadata')
                        print(metadata)
                    else:
                        self.error(
                            'Latis2 metadata returned None!',
                            'metadata', 'latis2', False)
            except Exception as ex:
                print(ex)
                self.error('Exception Thrown!', 'metadata', 'latis2', True)

            try:
                if testConfig.latis3:
                    self.info('Getting Latis3 metadata')
                    metadata3 = self.latis3Instance.metadata(
                        dataset=element['dataset'])
                    if len(metadata3):
                        self.info('Got Latis3 metadata')
                        print(metadata3)
                    else:
                        self.error(
                            'Latis3 metadata returned None!',
                            'metadata', 'latis3', False)
            except Exception as ex:
                print(ex)
                self.error('Exception Thrown!', 'metadata', 'latis3', True)

    def info(self, msg):
        if self.verbosity == 0:
            print('[INFO]: ' + msg)

    def error(self, msg, errType, latisVersion, isException):
        print('[ERROR]: ' + msg)
        self.errorReport['total'] = self.errorReport['total'] + 1
        if isException:
            self.errorReport['exception'] = self.errorReport['exception'] + 1
        if not errType:
            return

        self.errorReport[errType] = self.errorReport[errType] + 1
        if latisVersion == 'latis3':
            self.errorReport['latis3'] = self.errorReport['latis3'] + 1
        else:
            self.errorReport['latis2'] = self.errorReport['latis2'] + 1
