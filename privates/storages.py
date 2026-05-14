from typing import Final

from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import InvalidStorageError, storages
from django.utils.functional import LazyObject

STORAGE_ALIAS: Final = "privates"


class PrivateMediaFileSystemStorage:
    pass  # only here for historical migrations support


class PrivateMediaStorage(LazyObject):
    """
    Look up the privates storage from the settings.
    """

    def _setup(self):
        try:
            self._wrapped = storages[STORAGE_ALIAS]
        except InvalidStorageError as exc:
            raise ImproperlyConfigured(
                f"Could not find the '{STORAGE_ALIAS}' storage. Did you configure it "
                "in the STORAGES setting?"
            ) from exc


private_media_storage = PrivateMediaStorage()
"""
The default (lazy) private media storage.
"""
