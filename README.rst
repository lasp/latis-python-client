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

You can specify an API key for instances that require one.

.. code:: python

    df = read_data(
        "https://lasp.colorado.edu/lisird/latis/dap2",
        "bremen_composite_mgii",
        "2026-01-01",
        "2026-01-02",
        api_key="<api key>"
    )

You can specify a username and password for instances that require basic auth.

.. code:: python

   df = read_data(
        "https://lasp.colorado.edu/lisird/latis/dap2",
        "bremen_composite_mgii",
        "2026-01-01",
        "2026-01-02",
        username="<username>",
        password="<password>"
    )

For queries more complicated than time selections, you can optionally specify an additional `DAP2 query fragment <https://lasp.colorado.edu/lisird/about/latis>`__ that will be appended to the query sent to LaTiS. It must be URL-encoded.

.. code:: python

    df = read_data(
        "https://lasp.colorado.edu/lisird/latis/dap",
        "nnl_hires_ssi_P1D",
        "2025-01-01",
        "2025-01-02",
        query="wavelength%3E=400&wavelength%3C500&convert(time,days%20since%201858-11-17)&replace_missing(-99)"
    )

Multiple datasets can be joined by passing a list or tuple of dataset identifiers to ``read_data``. This is only supported by LaTiS 3 instances (those with URLs ending in ``/dap2``).

.. code:: python

    df = read_data(
      "https://example.org/latis/dap2",
      ["dataset1", "dataset2"],
      "yyyy-mm-dd",
      "yyyy-mm-dd"
    )
