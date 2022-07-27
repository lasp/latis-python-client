import pandas as pd


def query(baseUrl='https://lasp.colorado.edu/space-weather-portal/latis/dap/',
          dataset=None, suffix='csv', projection=[], selection=None,
          startTime=None, endTime=None, filterOptions=None):

    if dataset is None:
        return None

    q = baseUrl + dataset + '.' + suffix + '?'
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


def formatDataPd(
    baseUrl='https://lasp.colorado.edu/space-weather-portal/latis/dap/',
    dataset=None, projection=[], selection=None, startTime=None,
        endTime=None, filterOptions=None):

    q = query(baseUrl, dataset, 'csv', projection, selection, startTime,
              endTime, filterOptions)

    if q is None:
        return None
    else:
        return pd.read_csv(q, parse_dates=[0], index_col=[0])
