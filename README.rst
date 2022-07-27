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

    $ pip3 intall -r requirements.txt

Usage
=====

Generate a latis query

.. code:: python

    import latis
    query = latis.query(dataset='kyoto_dst_index', selection='time>=2022-07-20')

Create a pandas data structure

.. code:: python

    ...
    data = latis.formatDataPd(dataset='kyoto_dst_index',
                          selection='time>=2022-07-20')

Development
===========

Use flake8 to lint python code.

.. code:: bash

    $ python3 -m flake8 .

