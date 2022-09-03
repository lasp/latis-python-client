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

config = latis.Config(
    'https://lasp.colorado.edu/lisird/latis',
    False, 'cls_radio_flux_f8')
dataset = latis.LatisDataset(config)

print("============================")

config = latis.Config(
    'https://lasp.colorado.edu/lisird/latis',
    True, 'sorce_tsi_6hr_l3')
dataset = latis.LatisDataset(config)
dataset.select(['time<2452697'])
# dataset.getFile('test_file', '.asc')
c = dataset.getCatalog()
print(c.search('number'))
m = dataset.getMetadata()
print(m.json)