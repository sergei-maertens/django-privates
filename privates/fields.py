from __future__ import annotations

from django.db.models import FileField, ImageField, Model
from django.db.models.fields.files import FieldFile, ImageFieldFile
from django.urls import reverse

from .storages import private_media_storage


class PrivateMediaFieldFileMixin:
    instance: Model

    @property
    def url(self) -> str:
        from .admin import _get_private_media_view_name

        django_url = super().url  # type: ignore

        readonly_fields = getattr(self.instance, "_private_media_readonly_fields", None)
        if not readonly_fields:
            return django_url

        field_name = self.field.name  # type: ignore
        if field_name not in readonly_fields:
            return django_url

        url_name = (
            f"admin:{_get_private_media_view_name(self.instance._meta, field_name)}"
        )
        return reverse(url_name, kwargs={"pk": self.instance.pk})


class PrivateMediaFieldFile(PrivateMediaFieldFileMixin, FieldFile):
    pass


class PrivateMediaImageFieldFile(PrivateMediaFieldFileMixin, ImageFieldFile):
    pass


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

    attr_class = PrivateMediaFieldFile


class PrivateMediaImageField(PrivateMediaFieldMixin, ImageField):
    """
    A private media image field.
    """

    attr_class = PrivateMediaImageFieldFile
