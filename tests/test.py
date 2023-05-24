import os
import sys
import platform
import random

libPath = os.path.dirname(os.path.realpath(__file__))

if platform.system() == 'Windows':
    libPath = libPath.replace('\\tests',
                              '\\client')
else:
    libPath = libPath.replace('/tests',
                              '/client')

sys.path.insert(0, libPath)

import latis


def testRandomBaseUrl(baseUrl, latis3, seed, maxDatasets=None):
    random.seed(seed)

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
        except Exception:
            print("Failed to test or get a dataset.")
            pass


def testDataset(dsObj):
    metadata = dsObj.metadata.properties

    projections = []

    metadata_keys = list(metadata.keys())

    if metadata_keys:

        if metadata_keys[0] == 'time':

            projections.append(metadata_keys[0])
            if len(metadata_keys) == 2:
                projections.append(metadata_keys[1])
            else:
                projections.append(metadata_keys[random.randrange(1, len(metadata_keys) - 1)])

            # dsObj.operate('formatTime(yyyy.MM.dd)').project(projections).select(metadata_keys[0], start='0')

            dsObj.operate('formatTime(yyyy.MM.dd)').select(metadata_keys[0], start='0').project(projections)

            print(dsObj.name)
            print(dsObj.projections, dsObj.selections, dsObj.operations)
            print(dsObj.buildQuery())

            numpyData = dsObj.asNumpy()
            print(numpyData)


testRandomBaseUrl('https://lasp.colorado.edu/lisird/latis',
                  False, 23423, maxDatasets=4)


testRandomBaseUrl('https://lasp.colorado.edu/lisird/latis',
                  True, 23423, maxDatasets=4)
