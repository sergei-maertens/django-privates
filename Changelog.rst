=========
Changelog
=========

1.4.0 (2022-09-06)
==================

Periodic maintenance release

* Confirmed support for Django 4.0 and 4.1
* Dropped support for Django 2.2
* Dropped support for Python 3.5 and 3.6
* Updated CI infrastructure
* Code base is now formatted with black
* Codebase now exposes type hints (incomplete!)

1.3.0 (2021-12-17)
==================

Align supported version with Django LTS. The CI-tested versions are now Django 2.2 and
3.2.

Django 3.0 and 3.1 probably also still work, but these are end of life and not
officially supported.

* Dropped Django 1.11 support
* Added Python 3.9 support
* Added Python 3.10 support
* Migrated from Travis CI to Github Action

1.2.2 (2021-07-23)
==================

Fixed deprecation message about django.conf.urls (thanks @GerjonM).

Supported Django versions are now 1.11, 2.2 and 3.2.

1.2.0 (2020-03-16)
==================

Maintenance update, some small features and cleanup

* Fixed packaging so that ``testapp/`` and ``tests/`` are no longer packaged
* Dropped support for Django 2.0 and 2.1, added support for Django 3.0
* Added support for Python 3.8
* Depends on django-sendfile2 > 0.5, which went through a package rename from
  ``sendfile`` to ``django_sendfile``.
* Improved hooks to customize representations

1.1.0 (2019-11-21)
==================

* Added ``privates.fields.PrivateMediaImageField`` - thanks to @GerjonM
* Support dropped for Django 2.0 (EOL)
* Support dropped for Python 3.4 (EOL)

Most likely this will still work on Python 3.4 and Django 2.0, however, it's
not explicitly listed in the CI build anymore, so use on your own risk.
