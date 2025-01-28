==================
zyte-test-websites
==================

.. image:: https://img.shields.io/pypi/v/zyte-test-websites.svg
   :target: https://pypi.org/pypi/zyte-test-websites
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/zyte-test-websites.svg
   :target: https://pypi.python.org/pypi/zyte-test-websites
   :alt: Supported Python Versions

.. image:: https://github.com/zytedata/zyte-test-websites/workflows/tox/badge.svg
   :target: https://github.com/zytedata/zyte-test-websites/actions
   :alt: Build Status

.. image:: https://codecov.io/github/zytedata/duplicate-url-discarder/coverage.svg?branch=master
   :target: https://codecov.io/gh/zytedata/zyte-test-websites
   :alt: Coverage report

Overview
========

zyte-test-websites contains websites that can be used by spiders to test
scraping of websites of a specific kind. It currently contains a job postings
website.

Job postings
------------

Features:

* A page with job categories with pagination.
* Pages with jobs in a category with pagination.
* Pages with single job details.

Run it with:

.. code-block:: console

    $ python -m zyte_test_websites.main jobs 8888

You can access it at http://localhost:8888.

Requirements
============

* Python >= 3.9
* aiohttp
