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

print(libPath)
     
sys.path.insert(0, libPath)

import latis

config = latis.Config(
    'https://lasp.colorado.edu/lisird/latis',
    False, 'cls_radio_flux_f8')

dataset = latis.LatisDataset(config)

# baseUrl = dataset.getBaseUrl()
# print(baseUrl)

# catalog = dataset.getCatalog('timed')
# print(catalog)

metadata = dataset.getMetadata()
print(metadata)

config = latis.Config(
    'https://lasp.colorado.edu/lisird/latis',
    True, 'sorce_tsi_6hr_l3')

print("============================")
dataset = latis.LatisDataset(config)

metadata = dataset.getMetadata()
print(metadata)


# dataset.select(['time>=2022-08-11'])
# select = dataset.toDataFrame()
# print(select)