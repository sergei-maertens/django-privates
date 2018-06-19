from django.db import models

from privates.fields import PrivateMediaFileField


class File(models.Model):
    file = PrivateMediaFileField()
