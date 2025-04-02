===============
Django-privates
===============

Simple private media integration for Django.

|build-status| |linting| |coverage| |docs| |ruff|

|python-versions| |django-versions| |pypi-version|

What does it do?
================

Django supports file uploads for user-generated content out of the box, which is
typically *public* - think of images, videos...

However, often you want to expose files only to correctly authenticated users because
they have a sensitive nature, for example invoice PDFs or tenant-specific documents.

django-privates achieves the latter while being as convenient as Django's core
``FileField`` and derivatives.

Usage
=====

The installation and usage `documentation`_ is hosted on ReadTheDocs.


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

.. |ruff| image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Ruff

.. _documentation: https://django-privates.readthedocs.io/
