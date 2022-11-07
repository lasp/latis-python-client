import os
import sys
import platform

libPath = os.path.dirname(os.path.realpath(__file__))

if platform.system() == 'Windows':
    libPath = libPath.replace('\\tests',
                              '\\client')
else:
    libPath = libPath.replace('/tests',
                              '/client')

sys.path.insert(0, libPath)

import latis

def testShortcuts():

    print("Latis2 Numpy")
    testLatis2Np = latis.data(
        'https://lasp.colorado.edu/lisird/latis', False,
        'cls_radio_flux_f8', 'NUMPY', selection=['time<0'])
    print(testLatis2Np)

    print("Latis2 Pandas")
    testLatis2Pd = latis.data(
        'https://lasp.colorado.edu/lisird/latis', False,
        'cls_radio_flux_f8', 'PANDAS', selection=['time<0'])
    print(testLatis2Pd)

    print("Latis3 Numpy")
    testLatis3Np = latis.data(
        'https://lasp.colorado.edu/lisird/latis', True,
        'sorce_mg_index', 'NUMPY', selection=['time<2452705'])
    print(testLatis3Np)

    print("Latis3 Pandas")
    testLatis3Pd = latis.data(
        'https://lasp.colorado.edu/lisird/latis', True,
        'sorce_mg_index', 'PANDAS', selection=['time<2452705'])
    print(testLatis3Pd)

def testCore():
    print('Creating Latis Instance\n')
    # 1 - Create Instance
    instance = latis.LatisInstance(
        baseUrl='https://lasp.colorado.edu/lisird/latis',
        latis3=False)

    instance3 = latis.LatisInstance(
        baseUrl='https://lasp.colorado.edu/lisird/latis',
        latis3=True)

    print('\nSearch Catalog\n')
    # 2 - Search Catalog
    # print(instance.catalog.list) # (Full catalog)
    print(instance.catalog.search('cls'))
    print(instance3.catalog.search('sorce'))
    print(instance.catalog.datasets)
    print(instance3.catalog.datasets)

    print('\Getting Datasets\n')
    # 3 - Get dataset objects
    clsRadioFluxF8 = instance.getDataset('cls_radio_flux_f8')
    clsRadioFluxF15 = instance.getDataset('cls_radio_flux_f15')
    sorceMGIndex = instance3.getDataset('sorce_mg_index')

    print('\nCreating Queries\n')
    # 4 - Create queries
    queryReturn = clsRadioFluxF8.buildQuery()
    print(clsRadioFluxF15.select(['time<0']))
    print(queryReturn)
    print(sorceMGIndex.select(['time<2452705']))

    print('\nGet Metadata\n')
    # 5 - Get metadata
    print(clsRadioFluxF15.metadata.properties)
    print(clsRadioFluxF8.metadata.properties)
    print(sorceMGIndex.metadata.properties)

    print('\nGet data\n')
    # 6 - Get data
    pandasDF = clsRadioFluxF15.asNumpy()
    print(pandasDF)
    numpy = clsRadioFluxF15.asNumpy()
    print(numpy)
    mgData = sorceMGIndex.asPandas()
    print(mgData)

    # 7 - Get file
    # clsRadioFluxF15.getFile('cls_radio_flux_f15')
    # clsRadioFluxF15.getFile('cls_radio_flux_f15', 'txt')
    # clsRadioFluxF15.getFile('cls_radio_flux_f15.data')

testShortcuts()
#testCore()