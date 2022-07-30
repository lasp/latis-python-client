import numpy
import pandas as pd
import requests

class LatisInstance:

    def __init__(self, baseUrl='https://lasp.colorado.edu/lisird/latis/', latis3=False):
        if not baseUrl[-1] == '/':
            baseUrl += '/'
        if latis3:
            baseUrl += 'dap2/'
        else:
            baseUrl += 'dap/'
        self.baseUrl = baseUrl
        self.latis3 = latis3

    def getCatalog(self, searchTerm=None):
        if self.latis3:
            return None
        else:
            df = self.formatDataPd(dataset='catalog')

            urls = df['accessURL'].to_numpy()
            if searchTerm:
                return [k for k in urls if searchTerm in k]
            else:
                return urls

    def metadata(self, dataset=None, getStructureMetadata=False):
        if self.latis3:
            q = self.query(dataset, 'meta')
            return pd.read_json(q)
        else:
            suffix = 'das'
            if getStructureMetadata:
                suffix = 'dds'
            q = self.query(dataset, suffix)
            return requests.get(q).content

    def query(self, dataset=None, suffix='csv', projection=[], selection=None,
              startTime=None, endTime=None, filterOptions=None):

        if dataset is None:
            return None

        q = self.baseUrl + dataset + '.' + suffix + '?'
        if projection:
            q += ",".join(projection)
        if selection:
            q += "&" + selection
        else:
            if startTime:
                q += "&time>=" + startTime
            if endTime:
                q += "&time<=" + endTime
        if filterOptions:
            q += "&" + "&".join(filterOptions)
        return q


    def formatDataPd(self, dataset=None, projection=[], selection=None,
                     startTime=None, endTime=None, filterOptions=None):

        if self.latis3:
            return None
        else:
            q = self.query(dataset, 'csv', projection, selection, startTime,
                    endTime, filterOptions)

            if q is None:
                return None
            else:
                return pd.read_csv(q, parse_dates=[0], index_col=[0])

