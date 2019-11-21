from django.db import models

from privates.fields import PrivateMediaFileField, PrivateMediaImageField


class File(models.Model):
    file = PrivateMediaFileField()
    image = PrivateMediaImageField()
