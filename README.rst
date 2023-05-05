============================================
Django-privates - private media integrration
============================================

Django-privates makes it easy to work with login-protected ``FileField``\ s,
all the way through your application.

:Version: 2.0.0
:Source: https://github.com/sergei-maertens/django-privates
:Keywords: django, media, private, storage

|build-status| |linting| |coverage| |docs| |python-versions| |django-versions| |pypi-version|

.. contents::

.. section-numbering::

Features
========

* Default private media storage, configurable via settings
* Model field using the default storage
* Easy admin integration
* File serving through `sendfile`_ (supports nginx, apache, runserver,...)


Installation
============

Install
-------

.. code-block:: bash

    pip install django-privates

And then add ``privates`` to your ``INSTALLED_APPS`` for admin integration (
template discovery):

.. code-block:: python

    INSTALLED_APPS = [
        ...,

        'privates',

        ...
    ]


.. |build-status| image:: https://github.com/sergei-maertens/django-privates/workflows/Run%20CI/badge.svg
    :target: https://github.com/sergei-maertens/django-privates/actions?query=workflow%3A%22Run+CI%22
    :alt: Run CI

.. |linting| image:: https://github.com/sergei-maertens/django-privates/workflows/Code%20quality%20checks/badge.svg
    :target: https://github.com/sergei-maertens/django-privates/actions?query=workflow%3A%22Code+quality+checks%22
    :alt: Code linting

.. |coverage| image:: https://codecov.io/gh/sergei-maertens/django-privates/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/sergei-maertens/django-privates
    :alt: Coverage status

.. |docs| image:: https://readthedocs.org/projects/django-privates/badge/?version=latest
    :target: https://django-privates.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. |python-versions| image:: https://img.shields.io/pypi/pyversions/django-privates.svg

.. |django-versions| image:: https://img.shields.io/pypi/djversions/django-privates.svg

.. |pypi-version| image:: https://img.shields.io/pypi/v/django-privates.svg
    :target: https://pypi.org/project/django-privates/

.. _sendfile: https://pypi.org/project/django-sendfile2/
