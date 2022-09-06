.. Django Privates documentation master file, created by
   sphinx-quickstart on Tue Jun 19 15:36:59 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Django Privates's documentation!
===========================================

|build-status| |linting| |coverage|

|python-versions| |django-versions| |pypi-version|

Django-privates makes it easy to work with login-protected FileFields,
all the way through your application.

Features
========

* Default private media storage, configurable via settings
* Model field using the default storage
* Easy admin integration
* File serving through `sendfile`_ (supports nginx, apache, runserver,...)

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quickstart



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

.. _sendfile: https://pypi.org/project/django-sendfile2/

