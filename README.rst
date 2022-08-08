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

Create new latis instance. Arguments ``baseUrl='https://lasp.colorado.edu/lisird/latis/', latis3=False``

.. code:: python

    import latis

    latis2Instance = latis.LatisInstance()

Get catalog of datasets. Arguments ``searchTerm=None``

.. code:: python

    catalog = latis2Instance.getCatalog()
    filtered_catalog = latis2Instance.getCatalog(searchTerm='satire')

Get metadata. Arguments ``dataset=None, getStructureMetadata=False``

.. code:: python

    metadata = latis2Instance.metadata(dataset='cls_radio_flux_f8')
    structure_metadata = latis2Instance.metadata(dataset='cls_radio_flux_f8', getStructureMetadata=True)

Get query. Arguments ``dataset=None, suffix='csv', projection=[], selection=None, startTime=None, endTime=None, filterOptions=None``

.. code:: python

    query = latis2Instance.query(dataset='cls_radio_flux_f8', selection='time>=2022-07-27')

Format data to pandas. Arguments ``dataset=None, projection=[], selection=None, startTime=None, endTime=None, filterOptions=None``
    
.. code:: python
    
    data = latis2Instance.formatDataPd(dataset='cls_radio_flux_f8', selection='time>=2022-07-27')

Testing
=======

.. code:: bash

    python3 latis-python-client/tests/testClient.py

Development
===========

Use flake8 to lint python code.

.. code:: bash

    python3 -m flake8 .

