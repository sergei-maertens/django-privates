import os
from pathlib import Path

from django.core.files.storage import InMemoryStorage, storages

from privates.storages import STORAGE_ALIAS
from privates.test import temp_private_root


def test_private_root_uses_in_memory_storage_and_updates_sendfile_root(
    settings,
    tmp_path: Path,
):
    storage_location = str(tmp_path / "privates")
    assert not os.path.exists(storage_location)
    settings.STORAGES = {
        **settings.STORAGES,
        STORAGE_ALIAS: {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
            "OPTIONS": {
                "location": storage_location,
                "base_url": "/protected/",
            },
        },
    }

    with temp_private_root():
        private_storage = storages[STORAGE_ALIAS]

        assert isinstance(private_storage, InMemoryStorage)
        assert private_storage.location == storage_location
        assert private_storage.base_url == "/protected/"
        assert settings.SENDFILE_CHECK_FILE_EXISTS is False
        assert not os.path.exists(private_storage.location)
