from django.db.models import FileField

from .storages import private_media_storage


class PrivateMediaFileField(FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('storage', private_media_storage)
        super().__init__(*args, **kwargs)
