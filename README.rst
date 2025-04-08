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

.. image:: https://codecov.io/github/zytedata/zyte-test-websites/coverage.svg?branch=master
   :target: https://codecov.io/gh/zytedata/zyte-test-websites
   :alt: Coverage report

Overview
========

zyte-test-websites contains websites that can be used by spiders to test
scraping of websites of a specific kind. It currently contains an article
website, an e-commerce website and a job postings website.

Articles
--------

Features:

* A page with article categories.
* Pages with articles in a category with pagination.
* Pages with single article details.
* A search form with results pagination.
* An RSS feed.
* A page with a list of authors.
* Pages with author details.
* Some pages with static content like "Contact Us".

Run it with:

.. code-block:: console

    $ python -m zyte_test_websites.main articles 8888

You can access it at http://localhost:8888.


E-commerce
----------

Features:

* A page with top-level product categories with pagination.
* Pages with products and/or subcategories in a category with pagination.
* Pages with single product details.
* A search form with results pagination.

Run it with:

.. code-block:: console

    $ python -m zyte_test_websites.main ecommerce 8888

You can access it at http://localhost:8888.

Job postings
------------

Features:

* A page with job categories with pagination.
* Pages with jobs in a category with pagination.
* Pages with single job details.
* A search form with results pagination.

Run it with:

.. code-block:: console

    $ python -m zyte_test_websites.main jobs 8888

You can access it at http://localhost:8888.

Page objects
============

zyte-test-websites also includes page objects that can be used to extract
zyte-common-items_ objects from the provided websites.

Articles
--------

* ``zyte_test_websites.articles.extraction.TestArticlePage``
* ``zyte_test_websites.articles.extraction.TestArticleNavigationPage``

E-commerce
----------

* ``zyte_test_websites.ecommerce.extraction.TestProductPage``
* ``zyte_test_websites.ecommerce.extraction.TestProductListPage``
* ``zyte_test_websites.ecommerce.extraction.TestProductNavigationPage``

Job postings
------------

* ``zyte_test_websites.jobs.extraction.TestJobPostingPage``
* ``zyte_test_websites.jobs.extraction.TestJobPostingNavigationPage``

Requirements
============

* Python >= 3.9
* aiohttp


.. _zyte-common-items: https://zyte-common-items.readthedocs.io/en/latest/usage/items.html
