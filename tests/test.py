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

import random

def testBaseUrl(baseUrl, latis3, seed, maxDatasets=None):
    # random.seed(seed)

    instance = latis.LatisInstance(
        baseUrl=baseUrl,
        latis3=latis3)
    
    datasets = list(instance.catalog.datasets.values())

    if maxDatasets:
        index = 0
        picks = [0]
        dataset_picks = [datasets[0]]
        for i in range(maxDatasets):
            while index in picks:
                index = random.randrange(0, len(datasets) - 1)
            picks.append(index)
            dataset_picks.append(datasets[index])
        
        datasets = dataset_picks

    for d in datasets:
        try:
            dsObj = instance.getDataset(d)
            testDataset(dsObj)
        except:
            print("Failed to test or get a dataset.")
            pass

def testDataset(dsObj):
    metadata = dsObj.metadata.properties

    projections = []

    metadata_keys = list(metadata.keys())

    if metadata_keys:
        projections.append(metadata_keys[0])
        if len(metadata_keys) == 2:
            projections.append(metadata_keys[1])
        else:
            projections.append(metadata_keys[random.randrange(1, len(metadata_keys) - 1)])

        dsObj.project(projections).select(metadata_keys[0], start='0', end='1')

        print(dsObj.name, dsObj.projections, dsObj.selections, dsObj.operations, dsObj.buildQuery())

    # numpyData = dsObj.asNumpy()

    # if len(numpyData) > 1:
    #     print(numpyData[0], numpyData[1])

testBaseUrl('https://lasp.colorado.edu/lisird/latis', False, 324234)
# testBaseUrl('https://lasp.colorado.edu/lisird/latis', True, 324234, maxDatasets=10)