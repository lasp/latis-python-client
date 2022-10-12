import os
import sys
import platform

libPath = os.path.dirname(os.path.realpath(__file__))
if platform.system() == 'Windows':
    libPath = libPath.replace('\\latis-python-client\\tests',
                              '\\latis-python-client\\client')
else:
    libPath = libPath.replace('/latis-python-client/tests',
                              '/latis-python-client/client')

sys.path.insert(0, libPath)

import latis

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

print('\nCreating Datasets\n')
# 3 - Create a dataset objects
clsRadioFluxF8 = instance.createDataset('cls_radio_flux_f8')
clsRadioFluxF15 = instance.createDataset('cls_radio_flux_f15')
sorceMGIndex = instance3.createDataset('sorce_mg_index')

print('\nCreating Queries\n')
# 4 - Create queries
queryReturn = clsRadioFluxF8.buildQuery()
print(clsRadioFluxF15.buildQuery(selection=['time<0']))
print(queryReturn)
print(sorceMGIndex.buildQuery(selection=['time<2452705']))

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
# clsRadioFluxF15.getFile('cls_radio_flux_f15.data')
