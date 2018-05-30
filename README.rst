============================================
Django-privates - private media integrration
============================================

Django-privates makes it easy to work with login-protected ``FileField``s,
all the way through your application.

:Version: 0.1.0
:Source: https://github.com/sergei-maertens/django-privates
:Keywords: django, media, private, storage
:PythonVersion: 2.7, 3.4, 3.5, 3.6
:DjangoVersion: 1.11, 2.0

|build-status| |requirements|

.. contents::

.. section-numbering::

Features
========

* Default private media storage, configurable via settings
* Model field using the default storage
* Easy admin integration
* File serving through ``sendfile`` (supports nginx, apache, runserver,...)


* Django project inspection:

    * backs up configured databases using ``settings.DATABASES``
    * backs up file directories such as ``settings.MEDIA_ROOT``

* stdlib ``logging`` based reporting + e-mailing of backup/restore report
* YAML-based, minimal configuration
* Simple Python/CLI APIs for backup creation and restoration

Installation
============

Install
-------

.. code-block:: bash

    pip install django-privates

You do *not* need to add it to your ``INSTALLED_APPS``.


.. TODO

.. |build-status| image:: http://jenkins.maykin.nl/buildStatus/icon?job={{ project_name|lower }}
    :alt: Build status
    :target: http://jenkins.maykin.nl/job/{{ project_name|lower }}

.. |requirements| image:: https://requires.io/github/sergei-maertens/django-privates/requirements.svg?branch=master
     :target: https://requires.io/github/sergei-maertens/django-privates/requirements/?branch=master
     :alt: Requirements status
