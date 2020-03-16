============================================
Django-privates - private media integrration
============================================

Django-privates makes it easy to work with login-protected ``FileField``\ s,
all the way through your application.

:Version: 1.2.0
:Source: https://github.com/sergei-maertens/django-privates
:Keywords: django, media, private, storage

|build-status| |requirements| |coverage| |docs| |python-versions| |django-versions| |pypi-version|

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


.. |build-status| image:: https://travis-ci.org/sergei-maertens/django-privates.svg?branch=develop
    :target: https://travis-ci.org/sergei-maertens/django-privates

.. |requirements| image:: https://requires.io/github/sergei-maertens/django-privates/requirements.svg?branch=develop
    :target: https://requires.io/github/sergei-maertens/django-privates/requirements/?branch=develop
    :alt: Requirements status

.. |coverage| image:: https://codecov.io/gh/sergei-maertens/django-privates/branch/develop/graph/badge.svg
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
