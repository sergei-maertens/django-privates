==========
Quickstart
==========

Installation
============

#. Install from PyPI with pip:

.. code-block:: bash

    pip install django-privates


#. Add the app to your ``INSTALLED_APPS`` for admin integration and system checks:

.. code-block:: python

    INSTALLED_APPS = [
        ...

        "privates",

        ...
    ]

Settings
--------

We use the ``STORAGES`` setting introduced since Django 4.2, and expect a storage to
be configured with the ``"privates"`` key. Additionally, the ``SENDFILE_`` settings need
to be defined. For example:

.. code-block:: python
    :linenos:
    :emphasize-lines: 10-16

    STORAGES = {
        # default and staticfiles are the Django defaults
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
        # add privates
        "privates": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
            "OPTIONS": {
                "location": BASE_DIR / "private_media",
                "base_url": "/protected/",
            },
        },
    }

    SENDFILE_BACKEND = "django_sendfile.backends.nginx"
    SENDFILE_ROOT = BASE_DIR / "private_media"  # same as the storage location
    SENDFILE_URL = "/protected/"  # same as the storage base_url

The meaning of the backend options is:

``location``
    The private equivalent of ``MEDIA_ROOT`` - the base location where private media
    files will be stored.

``base_url``
    The private equivalent of ``MEDIA_URL``. Note that your webserver must be configured
    appropriately for this, see the `sendfile`_ documentation. Your webserver may
    **not** directly serve these URLs, otherwise files can be downloaded without
    authentication.

.. warning::
    It's important that you specify the ``location`` and ``base_url`` options, otherwise
    Django will fall back to ``settings.MEDIA_ROOT`` and ``settings.MEDIA_URL`` which will
    typically *publicly* expose your files.

The sendfile settings are important to actually serve the files correctly:

* ``SENDFILE_BACKEND``: depends on your webserver, see the `sendfile`_ documentation.

* ``SENDFILE_ROOT``: should be set to the storage location, as the library will resolve
  files from that path.

* ``SENDFILE_URL``: should be set to the storage base_url, so the webserver can match
  the location block to serve the file.

URLs
----

No URLs need to be configured. However, for development, you likely want to serve the
private media file uploads with Django. This can be achieved via settings:

.. code-block:: python

    SENDFILE_BACKEND = "django_sendfile.backends.development"

Defining model fields and admin integration
===========================================

Models
------

The simplest way is to use the model field, which is a drop-in replacement of Django's
``django.db.models.FileField``.

.. code-block:: python

    from django.db import models

    from privates.fields import PrivateMediaFileField, PrivateMediaImageField


    class IDDocument(models.Model):
        pdf = PrivateMediaFileField(blank=True)
        mugshot = PrivateMediaImageField(upload_to="mugshots/%Y/")

This uses the underlying :data:`privates.storages.private_media_storage`.

Admin
-----

There is built in admin integration via a mixin. This takes care of replacing
the default widget so you can open the private media files, and perform
permission checks.


.. code-block:: python

    from django.contrib import admin

    from privates.admin import PrivateMediaMixin

    from .models import Invoice


    @admin.register(Invoice)
    class InvoiceAdmin(PrivateMediaMixin, admin.ModelAdmin):
        pass


By default, this mixin requires you to have the ``<applabel>.can_change_<model>``
permission.

Attributes:

* :attr:`privates.admin.PrivateMediaMixin.private_media_permission_required`:
  (custom) permission to check instead of the default ``<applabel>.can_change_<model>``

* :attr:`privates.admin.PrivateMediaMixin.private_media_view_options`: optional
  arguments to forward to the ``sendfile.sendfile`` function.

Serving file contents
=====================

The private media files still need to be served to authorized users. The process for
this is roughly:

#. Define a view, which:

    #. Checks the user permissions
    #. Looks up the requested model instance
    #. Look up the relevant file field of the model
    #. Extract the path on-disk of the file
    #. Return a response which contains the file path information in a format the
       webserver understands
    #. Let the webserver (nginx, apache...) serve the file as efficiently as possible

#. Hook up the view to a URL in your ``urls.py``
#. Expose the download button with a simple anchor tag URL or button action in your
   template(s)

Generic view
------------

Django Privates ships with a built in permission-check view, used by the admin
integration. You are encouraged to re-use this.

It's built on top of ``django.contrib.auth.mixins.PermissionRequiredMixin``
and ``django.views.generic.DetailView``, so the methods/attributes of these
base classes are available.

.. code-block:: python

    from privates.views import PrivateMediaView


    class InvoicePDFView(PrivateMediaView):
        queryset = Invoice.objects.all()
        file_field = "pdf"
        permission_required = "applabel.can_change_invoice"

Custom views
------------

You can also easily serve file contents in regular views and/or djangorestframework
endpoints, for example:

.. code-block:: python

    from django_sendfile import sendfile
    from rest_framework import permissions
    from rest_framework.generics import GenericAPIView

    class DownloadFileView(GenericAPIView):
        queryset = IDDocument.objects.all()
        permission_classes = (permissions.IsAuthenticated,)

        def get(self, request, *args, **kwargs):
            instance = self.get_object()  # the get_object methods performs permission checks
            filepath = instance.pdf.path
            return sendfile(request, path)

Testing tools
=============

To isolate tests, you should clean up any uploaded files generated during
tests. :class:`privates.test.temp_private_root` is available to facilitate this:

.. code-block:: python

    from privates.test import temp_private_root


    @temp_private_root()
    class MyTests(TestCase):
        pass


The usage is the same as ``override_settings``, so you can use it as a class
decorator, test method decorator or context manager.


.. _sendfile: https://pypi.org/project/django-sendfile2/
