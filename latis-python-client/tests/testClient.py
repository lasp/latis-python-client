from dataclasses import dataclass

import test

@dataclass
class testConfig:
    baseUrl: str
    latis2: bool
    latis3: bool
    catalogSearch: []
    queries: []
    formats: []
    metadatas: []

allConfigs = [
    testConfig('https://lasp.colorado.edu/lisird/latis',
            False,
            True,
            [None, 'satire'],
            [{'dataset': 'cls_radio_flux_f8', 'selection': 'time>=2022-07-27'}],
            [{'dataset': 'cls_radio_flux_f8', 'selection': 'time>=2022-07-27'}],
            [{'dataset': 'cls_radio_flux_f8'}]),

    testConfig('https://swp-dev.pdmz.lasp.colorado.edu/space-weather-portal/latis',
                False,
                True,
                [None],
                [{'dataset': 'kyoto_dst_index', 'selection': 'time>=2022-07-27'}],
                [{'dataset': 'kyoto_dst_index', 'selection': 'time>=2022-07-27'}],
                [{'dataset': 'kyoto_dst_index'}]),

    testConfig('https://lasp.colorado.edu/lisird/latis',
                True,
                False,
                [None, 'satire'],
                [{'dataset': 'cls_radio_flux_f8', 'selection': 'time>=2022-07-27'}],
                [{'dataset': 'cls_radio_flux_f8', 'selection': 'time>=2022-07-27'}],
                [{'dataset': 'cls_radio_flux_f8'}])
]

tc = test.latisTester()

errorReport = {
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

for config in allConfigs:
    print('\n=======================')
    errorReport = tc.runTests(config)

print('\n==[TEST SUMMARY]=======')
print('createLatisInstances() ERRORS: ', errorReport['instance'])
print('getCatalog() ERRORS: ', errorReport['catalog'])
print('query() ERRORS: ', errorReport['query'])
print('formatDataPd() ERRORS: ', errorReport['format'])
print('metadata() ERRORS: ', errorReport['metadata'])
print('=======================')
print('TOTAL EXCEPTIONS: ', errorReport['exception'])
print('LATIS 2 ERRORS: ', errorReport['latis2'])
print('LATIS 3 ERRORS: ', errorReport['latis3'])
print('=======================')
print('TOTAL ERRORS: ', errorReport['total'])
print('\n')