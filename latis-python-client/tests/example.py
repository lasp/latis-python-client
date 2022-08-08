import os
import sys

libPath = os.path.dirname(os.path.realpath(__file__))
libPath = libPath.replace('/latis-python-client/tests',
                          '/latis-python-client/client')
sys.path.insert(0, libPath)

import latis

latis2Instance = latis.LatisInstance()

catalog = latis2Instance.getCatalog()
filtered_catalog = latis2Instance.getCatalog(searchTerm='satire')

metadata = latis2Instance.metadata(dataset='cls_radio_flux_f8')
structure_metadata = latis2Instance.metadata(
    dataset='cls_radio_flux_f8', getStructureMetadata=True)

query = latis2Instance.query(dataset='cls_radio_flux_f8',
                             selection='time>=2022-07-27')
data = latis2Instance.formatDataPd(dataset='cls_radio_flux_f8',
                                   selection='time>=2022-07-27')

print(catalog)
print(filtered_catalog)

print(metadata)
print(structure_metadata)

print(query)
print(data)
