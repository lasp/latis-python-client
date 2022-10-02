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

    pip3 intall -r requirements.txt

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
    
    instance.catalog.catalog
    
    instance3.catalog.catalog

Create datasets.

.. code:: python

    clsRadioFluxF8 = instance.createDataset('cls_radio_flux_f8')
    
    clsRadioFluxF15 = instance.createDataset('cls_radio_flux_f15')
    
    sorceMGIndex = instance3.createDataset('sorce_mg_index')
    
Create Queries.

.. code:: python

    clsRadioFluxF8.buildQuery()
     
    clsRadioFluxF15.buildQuery(selection=['time<0'])
     
    sorceMGIndex.buildQuery(selection=['time<2452705'])

Get Metadata.

.. code:: python

    clsRadioFluxF15.metadata.metadata
    
    clsRadioFluxF8.metadata.metadata
    
    sorceMGIndex.metadata.metadata

Get Data.

.. code:: python

    pandasDF = clsRadioFluxF15.getData()

    numpy = clsRadioFluxF15.getData('NUMPY')

    mgData = sorceMGIndex.getData('NUMPY')

Get File.

.. code:: python

    clsRadioFluxF15.getFile('cls_radio_flux_f15.data')

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

