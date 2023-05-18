********
`latis-python-client`_
********

|Latest Version|

.. |Latest Version|
   :target: https://pypi.org/

latis-python-client streamlines latis operations in python.

Installation
============

.. code:: bash

    pip3 install -r requirements.txt

Usage
=====

Create new latis instance.

.. code:: python

    import latis

    instance = latis.LatisInstance(
         baseUrl='https://lasp.colorado.edu/lisird/latis',
         latis3=False)

    instance3 = latis.LatisInstance(
         baseUrl='https://lasp.colorado.edu/lisird/latis',
         latis3=True)

Get catalog.

.. code:: python

    instance.catalog.search('cls')
    
    instance3.catalog.search('sorce')
    
    instance.catalog.datasets
    
    instance3.catalog.datasets

Get datasets.

.. code:: python

    clsRadioFluxF8 = instance.getDataset('cls_radio_flux_f8')
    
    clsRadioFluxF15 = instance.getDataset('cls_radio_flux_f15')
    
    sorceMGIndex = instance3.getDataset('sorce_mg_index')
    
Add selections/projections/operations.

.. code:: python

    clsRadioFluxF15.select('time<0')
    
    sorceMGIndex.select('time<2452705')
    
    clsRadioFluxF107.project(['time', 'absolute_f107']).select(start='1953', end='1954').select(target='absolute_f107', end='70').operate('formatTime(yyyy.MM.dd)')

Order of additions does not matter:

.. code:: python

    clsRadioFluxF107.project(['time','absolute_f107']).operate('formatTime(yyyy.MM.dd)').select(target='absolute_f107', end='70').select(start='1953', end='1954')

Get Metadata.

.. code:: python

    clsRadioFluxF15.metadata.properties
    
    clsRadioFluxF8.metadata.properties
    
    sorceMGIndex.metadata.properties

Get Data.

.. code:: python

    pandasDF = clsRadioFluxF15.asNumpy()

    numpy = clsRadioFluxF15.asNumpy()

    mgData = sorceMGIndex.asPandas()

Get File.

.. code:: python

    clsRadioFluxF15.getFile('cls_radio_flux_f15') # Creates csv format file with .csv suffix
    
    clsRadioFluxF15.getFile('cls_radio_flux_f15', 'txt') # Creates txt format file with .txt suffix
    
    clsRadioFluxF15.getFile('cls_radio_flux_f15.data') # Creates csv format file with .data suffix

Testing
=======

(Currently temporary until test code is rewritten)

.. code:: bash

    python3 latis-python-client/tests/example.py

Development
===========

Use flake8 to lint python code.

.. code:: bash

    python3 -m flake8 .

