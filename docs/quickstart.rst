==========
Quickstart
==========

Installation
============

#. Install from PyPI with pip:

.. code-block:: bash

    pip install django-privates


#. Add the app to your ``INSTALLED_APPS`` for admin integration:

.. code-block:: python

    INSTALLED_APPS = [
        ...

        "privates",

        ...
    ]

Settings
--------

You need to set the following settings:

* ``PRIVATE_MEDIA_ROOT``: private equivalent of ``MEDIA_ROOT`` - the base location
  where private media files will be stored.

* ``PRIVATE_MEDIA_URL``: private equivalent of ``MEDIA_URL``. Note that your webserver
  must be configured appropriately for this, see the `sendfile`_ documentation. Your
  webserver may **not** directly serve these URLs, otherwise files can be downloaded
  without authentication.

* ``SENDFILE_BACKEND``: depends on your webserver, see the `sendfile`_
  documentation.

* ``SENDFILE_ROOT``: should be set to ``PRIVATE_MEDIA_ROOT``.

* ``SENDFILE_URL``: should be set to ``PRIVATE_MEDIA_URL``.

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
tests. There is a wrapper around ``django.test.override_settings`` available
to facilitate this:

.. code-block:: python

    from privates.test import temp_private_root


    @temp_private_root()
    class MyTests(TestCase):
        pass


The usage is the same as ``override_settings``, so you can use it as a class
decorator, test method decorator or context manager.


.. _sendfile: https://pypi.org/project/django-sendfile2/
