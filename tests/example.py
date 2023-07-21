import os
import sys
import platform

libPath = os.path.dirname(os.path.realpath(__file__))

if platform.system() == 'Windows':
    libPath = libPath.replace('\\tests',
                              '\\src\\')
else:
    libPath = libPath.replace('/tests',
                              '/src/')

sys.path.insert(0, libPath)

import latis.client as latis


def testShortcuts():

    # latis.download(
    #     'https://lasp.colorado.edu/lisird/latis', False,
    #     'cls_radio_flux_f8', 'testing', 'csv', selections=['time<0'])

    print("Latis2 Numpy")
    testLatis2Np = latis.data(
        'https://lasp.colorado.edu/lisird/latis',
        'cls_radio_flux_f8', 'NUMPY', operations=['time<0'],
        preferVersion2=False)
    # Will auto switch to latis 2
    print(testLatis2Np)

    print("Latis2 Pandas")
    testLatis2Pd = latis.data(
        'https://lasp.colorado.edu/lisird/latis',
        'cls_radio_flux_f8', 'PANDAS', operations=['time<0'],
        preferVersion2=True)
    print(testLatis2Pd)

    print("Latis3 Numpy")
    testLatis3Np = latis.data(
        'https://lasp.colorado.edu/lisird/latis',
        'sorce_mg_index', 'NUMPY', operations=['time<2452705'])
    print(testLatis3Np)

    print("Latis3 Pandas")
    testLatis3Pd = latis.data(
        'https://lasp.colorado.edu/lisird/latis',
        'sorce_mg_index', 'PANDAS', operations=['time<2452705'],
        preferVersion2=True)
    # Dataset also exists on latis 2. Will not auto switch.
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

    print('\nGetting Datasets\n')
    # 3 - Get dataset objects
    clsRadioFluxF8 = instance.getDataset('cls_radio_flux_f8')
    clsRadioFluxF15 = instance.getDataset('cls_radio_flux_f15')
    sorceMGIndex = instance3.getDataset('sorce_mg_index')
    clsRadioFluxF107 = instance.getDataset('cls_radio_flux_absolute_f107')

    print('\nCreating Queries\n')
    # 4 - Create queries
    clsRadioFluxF15.select(start='0')
    sorceMGIndex.select(start='2452705')
    clsRadioFluxF107.project(['time', 'absolute_f107']).select(start='1953', end='1954').select(target='absolute_f107', end='70').operate('formatTime(yyyy.MM.dd)')
    # clsRadioFluxF107.project(['time','absolute_f107']).operate('formatTime(yyyy.MM.dd)').select(target='absolute_f107', end='70').select(start='1953', end='1954')

    print(clsRadioFluxF8.buildQuery())
    print(clsRadioFluxF15.buildQuery())
    print(clsRadioFluxF107.buildQuery())

    print('\nGet Metadata\n')
    # 5 - Get metadata
    print(clsRadioFluxF15.metadata.properties)
    print(clsRadioFluxF8.metadata.properties)
    print(sorceMGIndex.metadata.properties)

    print('\nGet data\n')
    # 6 - Get data

    print("clsRadioFluxF15:", clsRadioFluxF15.projections,
          clsRadioFluxF15.selections, clsRadioFluxF15.operations)
    print("clsRadioFluxF8:", clsRadioFluxF8.projections,
          clsRadioFluxF8.selections, clsRadioFluxF8.operations)
    print("clsRadioFluxF107:", clsRadioFluxF107.projections,
          clsRadioFluxF107.selections, clsRadioFluxF107.operations)
    print("sorceMGIndex:", sorceMGIndex.projections,
          sorceMGIndex.selections, sorceMGIndex.operations)

    pandasDF = clsRadioFluxF15.asPandas()
    print(pandasDF)
    numpy = clsRadioFluxF107.asNumpy()
    print(numpy)
    mgData = sorceMGIndex.asPandas()
    print(mgData)

    # 7 - Get file
    clsRadioFluxF15.getFile('cls_radio_flux_f15')
    clsRadioFluxF15.getFile('cls_radio_flux_f15', 'txt')
    clsRadioFluxF15.getFile('cls_radio_flux_f15.data')

def testErrors():
    # testLatis2Np = latis.data(
    #     'https://lasp.colorado.edu/lisird/latis',
    #     'cls_radio_flux_f83', 'NUMPY', operations=['time<0'],
    #     preferVersion2=False)
    
    instance = latis.LatisInstance(
        baseUrl='https://lasp.colorado.edu/lisird/latis',
        latis3=False)
    
    instance3 = latis.LatisInstance(
        baseUrl='https://lasp.colorado.edu/lisird/latis',
        latis3=True)   

    instancebad = latis.LatisInstance(
        baseUrl='https://lasp.colorado.edu/lis3rd/latis',
        latis3=True)

    instance.getDataset('cls_radio3_flux_f8')
    instance.getDataset('cls_radi3o_flux_f15')
    instance3.getDataset('sorce_mg3_index')
    instance.getDataset('cls_radio3_flux_absolute_f107')
    
    clsRadioFluxF8 = instance.getDataset('cls_radio_flux_f8')
    clsRadioFluxF15 = instance.getDataset('cls_radio_flux_f15')
    sorceMGIndex = instance3.getDataset('sorce_mg_index')
    clsRadioFluxF107 = instance.getDataset('cls_radio_flux_absolute_f107')

    clsRadioFluxF15.select(start='A')
    clsRadioFluxF107.project(['232', '23231']).select(start='A', end='QERWEEWD').select(target='absolute_f107', end='70').operate('formatTime(yyyy.MM.dd)')

    print(clsRadioFluxF15.asPandas())
    print(clsRadioFluxF107.asNumpy())

    clsRadioFluxF15.getFile('cls_radio_flux_f15')
    clsRadioFluxF15.getFile('cls_radio_flux_f15', '3txt')
    clsRadioFluxF15.getFile('cls_radio_flux_f15.data')

testErrors()
# testShortcuts()
# testCore()