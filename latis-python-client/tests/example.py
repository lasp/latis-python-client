import os
import sys

libPath = os.path.dirname(os.path.realpath(__file__))
libPath = libPath.replace('/latis-python-client/tests',
                          '/latis-python-client/client')
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

select = dataset.select('&time>=2022-08-11')
print(select)