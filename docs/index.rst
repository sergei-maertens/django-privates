.. Django Privates documentation master file, created by
   sphinx-quickstart on Tue Jun 19 15:36:59 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Django Privates's documentation!
===========================================

Simple private media integration for Django.

|build-status| |linting| |coverage| |ruff|

|python-versions| |django-versions| |pypi-version|

Django supports file uploads for user-generated content out of the box, which is
typically *public* - think of images, videos...

However, often you want to expose files only to correctly authenticated users because
they have a sensitive nature, for example invoice PDFs or tenant-specific documents.

django-privates achieves the latter while being as convenient as Django's core
``FileField`` and derivatives.

Features
========

* Provides a default private media storage, configurable via settings
* Private model field variants for ``FileField`` and ``ImageField``
* Easy admin integration
* Performant file serving through `sendfile`_ (supports nginx, apache, runserver,...)

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quickstart
   examples
   reference


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. |build-status| image:: https://github.com/sergei-maertens/django-privates/workflows/Run%20CI/badge.svg
    :target: https://github.com/sergei-maertens/django-privates/actions?query=workflow%3A%22Run+CI%22
    :alt: Run CI

.. |linting| image:: https://github.com/sergei-maertens/django-privates/workflows/Code%20quality%20checks/badge.svg
    :target: https://github.com/sergei-maertens/django-privates/actions?query=workflow%3A%22Code+quality+checks%22
    :alt: Code linting

.. |coverage| image:: https://codecov.io/gh/sergei-maertens/django-privates/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/sergei-maertens/django-privates
    :alt: Coverage status

.. |python-versions| image:: https://img.shields.io/pypi/pyversions/django-privates.svg

.. |django-versions| image:: https://img.shields.io/pypi/djversions/django-privates.svg

.. |pypi-version| image:: https://img.shields.io/pypi/v/django-privates.svg
    :target: https://pypi.org/project/django-privates/

.. |ruff| image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Ruff

.. _sendfile: https://pypi.org/project/django-sendfile2/

