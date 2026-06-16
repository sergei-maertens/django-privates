=========
Changelog
=========

4.0.3 (2026-06-16)
==================

Bugfix release.

* Fixed a crash in the admin when navigating to an object that doesn't exist.

4.0.2 (2026-05-15)
==================

Bugfix release.

* Fixed a regression in the migration serialization which would put absolute file
  system paths into migration files.

4.0.1 (2026-05-15)
==================

Small quality of life bugfix release.

* The ``temp_private_root`` test helper is now more versatile for different situations.

  - By default, it will reset the in-memory storage between tests when used as a class
    decorator, however you can opt out of this behaviour with the
    ``reset_storage=False`` parameter. This can be useful when setting up test data
    with private file fields in the ``setUpTestData`` class method.
  - By default, it injects a custom ``SENDFILE_BACKEND`` to serve files from the
    in-memory storage. You can opt-out of this if you have other/outer
    ``@override_settings`` decorators that override this setting.

* Fixed broken ReadTheDocs configuration.

4.0.0 (2026-05-14)
==================

Maintenance and refactor release.

We now use Django's built-in ``STORAGES`` setting, requiring breaking changes.

**Breaking changes 💥**

* Dropped support for Django 4.2.
* Dropped support for Python 3.11 and older.
* Reworked library to use ``settings.STORAGES``. Upgrading is mostly a boilerplate
  settings annoyance. For the least friction:

  .. code-block:: diff

        PRIVATE_MEDIA_ROOT = "/path/to/private-media/"
        PRIVATE_MEDIA_URL = "/private_media/"
        SENDFILE_ROOT = PRIVATE_MEDIA_ROOT
        SENDFILE_URL = PRIVATE_MEDIA_URL
      + STORAGES = {
      +     "default": {
      +         "BACKEND": "django.core.files.storage.FileSystemStorage",
      +     },
      +     "staticfiles": {
      +         "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
      +     },
      +     "privates": {
      +         "BACKEND": "django.core.files.storage.FileSystemStorage",
      +         "OPTIONS": {
      +             "location": PRIVATE_MEDIA_ROOT,
      +             "base_url": PRIVATE_MEDIA_URL,
      +         },
      +     },
      + }

  .. note:: The ``PRIVATE_MEDIA_*`` settings are all gone - you can restructure this
     code however you like.

**New features**

* Confirmed support for Django 6.0 and Python 3.14.
* Improved type annotations.
* [#18] Support configuration via the ``STORAGES`` setting.
* [#18] Added system checks that report broken configuration.

**Bugfixes**

* [#8] The ``privates.test.temp_private_root`` testing helper now sets up an in-memory
  storage that should no longer pollute the file system.

**Project maintenance**

* Hardened the CI workflows to reduce supply chain attack risks.
* CI now runs on a weekly basis to catch upstream changes early.

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
