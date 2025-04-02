# ruff: noqa: DJ008
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
