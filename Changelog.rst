=========
Changelog
=========

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
