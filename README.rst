********
LaTiS Python Client
********

A client library for making LaTiS requests in Python.

Installation
============

We do not yet publish to PyPI so you need to install from Git:

.. code:: bash

    python3 -m pip install git+https://github.com/lasp/latis-python-client.git

Usage
=====

Use the ``read_data`` function to make a request to LaTiS and get the results as a Pandas ``DataFrame``.

The ``read_data`` function expects the following arguments:

* ``base_url``: The base URL of a LaTiS instance. The base URL includes the host and the path through ``/dap`` (for LaTiS 2) or ``/dap2`` (for LaTiS 3).
* ``dataset``: The identifier of a dataset.
* ``start_time``: The start time of the request, in ISO-8601 format.
* ``end_time``: The end time (exclusive) of the request, in ISO-8601 format.

.. code:: python

    from latis.client import read_data

    df = read_data(
        "https://lasp.colorado.edu/lisird/latis/dap2",
        "bremen_composite_mgii",
        "2026-01-01",
        "2026-01-02"
    )

You can optionally specify an API key for instances that require one.

.. code:: python

    df = read_data(
        "https://lasp.colorado.edu/lisird/latis/dap2",
        "bremen_composite_mgii",
        "2026-01-01",
        "2026-01-02",
        api_key="<api key>"
    )
