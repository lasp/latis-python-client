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
    False, 'cls_radio_flux_f8', None)

dataset = latis.LatisDataset(config)

# baseUrl = dataset.getBaseUrl()
# print(baseUrl)

# catalog = dataset.getCatalog('timed')
# print(catalog)

# metadata = dataset.getMetadata()
# print(metadata)

select = dataset.toDataFrame('&time>=2022-08-11')
print(select)