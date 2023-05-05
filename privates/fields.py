from django.db.models import FileField, ImageField

from .storages import private_media_storage


class PrivateMediaFieldMixin:
    """
    Enable a private media storage for file-based model fields.

    Use the mixin in combination with django's ``FileField`` class or derivatives to
    set up the (default) private media storage.

    :arg storage: the (private) file storage to use. This defaults to django-privates'
      default private storage, but you can subclass these and provide your own. See the
      upstream storage documentation: https://docs.djangoproject.com/en/4.2/topics/files/#file-storage
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("storage", private_media_storage)
        super().__init__(*args, **kwargs)


class PrivateMediaFileField(PrivateMediaFieldMixin, FileField):
    """
    A generic private media file field.
    """


class PrivateMediaImageField(PrivateMediaFieldMixin, ImageField):
    """
    A private media image field.
    """
