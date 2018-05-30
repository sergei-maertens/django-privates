from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.functional import LazyObject


class PrivateMediaFileSystemStorage(FileSystemStorage):

    """
    Storage that puts files in the private media folder that isn't
    globally available.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('location', settings.PRIVATE_MEDIA_ROOT)
        kwargs.setdefault('base_url', settings.PRIVATE_MEDIA_URL)
        super().__init__(*args, **kwargs)


class PrivateMediaStorage(LazyObject):

    def _setup(self):
        self._wrapped = PrivateMediaFileSystemStorage()


private_media_storage = PrivateMediaStorage()
