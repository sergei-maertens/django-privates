============================================
Django-privates - private media integrration
============================================

Django-privates makes it easy to work with login-protected ``FileField``s,
all the way through your application.

:Version: 1.0
:Source: https://github.com/sergei-maertens/django-privates
:Keywords: django, media, private, storage
:PythonVersion: 3.4, 3.5, 3.6
:DjangoVersion: 1.11, 2.0

|build-status| |requirements| |coverage|

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

.. code-block:: bash

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

.. _sendfile: https://pypi.org/project/django-sendfile2/
