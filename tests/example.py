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

    # latis.download(
    #     'https://lasp.colorado.edu/lisird/latis', False,
    #     'cls_radio_flux_f8', 'testing', 'csv', selections=['time<0'])

    print("Latis2 Numpy")
    testLatis2Np = latis.data(
        'https://lasp.colorado.edu/lisird/latis', False,
        'cls_radio_flux_f8', 'NUMPY', selections=['time>0'])
    print(testLatis2Np)

    print("Latis2 Pandas")
    testLatis2Pd = latis.data(
        'https://lasp.colorado.edu/lisird/latis', False,
        'cls_radio_flux_f8', 'PANDAS', selections=['time<0'])
    print(testLatis2Pd)

    print("Latis3 Numpy")
    testLatis3Np = latis.data(
        'https://lasp.colorado.edu/lisird/latis', True,
        'sorce_mg_index', 'NUMPY', selections=['time<2452705'])
    print(testLatis3Np)

    print("Latis3 Pandas")
    testLatis3Pd = latis.data(
        'https://lasp.colorado.edu/lisird/latis', True,
        'sorce_mg_index', 'PANDAS', selections=['time<2452705'])
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
    clsRadioFluxF107 = instance.getDataset('cls_radio_flux_absolute_f107')

    print('\nCreating Queries\n')
    # 4 - Create queries
    clsRadioFluxF15.select('time<0')
    sorceMGIndex.select('time<2452705')
    clsRadioFluxF107.project(['time','absolute_f107']).select(start='1953', end='1954').select(target='absolute_f107', end='70').operate('formatTime(yyyy.MM.dd)')
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

    print("clsRadioFluxF15:", clsRadioFluxF15.projections, clsRadioFluxF15.selections, clsRadioFluxF15.operations)
    print("clsRadioFluxF8:", clsRadioFluxF8.projections, clsRadioFluxF8.selections, clsRadioFluxF8.operations)
    print("clsRadioFluxF107:", clsRadioFluxF107.projections, clsRadioFluxF107.selections, clsRadioFluxF107.operations)
    print("sorceMGIndex:", sorceMGIndex.projections, sorceMGIndex.selections, sorceMGIndex.operations)

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

# testShortcuts()
testCore()

#https://lasp.colorado.edu/lisird/latis/dap/cls_radio_flux_absolute_f107.asc?time,absolute_f107&time<1952&formatTime(yyyy.MM.dd)