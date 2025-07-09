# ruff: noqa: DJ008
from django.core.cache import DEFAULT_CACHE_ALIAS, caches
from django.db import models

from privates.fields import PrivateMediaFileField, PrivateMediaImageField


class File(models.Model):
    file = PrivateMediaFileField()
    image = PrivateMediaImageField()


class File2(File):
    """Used for testing `admin.PrivateMediaMixin.no_download_fields`"""

    class Meta:
        proxy = True


class File3(File):
    class Meta:
        proxy = True


class File4(File):
    class Meta:
        proxy = True


class CacheModel(models.Model):
    file = PrivateMediaFileField()

    def save(self, **kwargs):
        super().save(**kwargs)

        cache = caches[DEFAULT_CACHE_ALIAS]
        cache.add("cache-model", self)
