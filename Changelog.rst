=========
Changelog
=========

3.1.1 (2025-07-09)
==================

Bugfix release.

* [#15] Fixed 3.0.0 regression (because of #10) where it was no longer possible to
  pickle model instances that are exposed with the ``PrivateMediaMixin`` in the admin.

3.1.0 (2025-04-02)
==================

Small feature release to confirm support for Django 5.2

* Confirmed support for Django 5.2
* Confirmed support for Python 3.13
* Switched out black and isort for ruff
* Replaced legacy typing syntax with 3.10+ compatible syntax.

3.0.0 (2025-02-26)
==================

Maintenance and bugfix release

**Breaking changes 💥**

* Dropped support for Python 3.8 and 3.9
* Dropped support for Django 3.2 and 4.1

**Other changes**

* [#10] Fixed incorrect donwload link being shown for readonly private media fields in
  the admin.
* Confirmed support for Python 3.11 and 3.12.
* The package is now published via Github Trusted Publishers.

2.0.0.post1 (2024-03-01)
========================

* Added mypy type checking
* Updated type annotations to align with django-stubs for downstream
  projects/packages
* Confirmed Django 4.2 support

2.0.0 (2023-05-05)
==================

Periodic version compatibility release.

**Breaking changes 💥**

* Dropped support for Python 3.7
* Dropped support for Django 4.0

The library likely still works on those versions, but they are no longer tested.

**Other changes**

* Confirmed support for Python 3.11
* Confirmed support for Django 4.2

1.5.0 (2023-01-03)
==================

Feature release

* Added ``privates.admin.PrivateMediaMixin.private_media_no_download_fields`` so admin
  classes can mark fields for which no file download URL/view should be generated
* Specifying ``privates.admin.PrivateMediaMixin.private_media_fields`` is now optional,
  available private media fields are now automatically discovered.

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
