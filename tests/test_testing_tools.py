import os
from io import BytesIO
from pathlib import Path

from django.core.files import File
from django.core.files.storage import InMemoryStorage, storages
from django.http import Http404
from django.test import RequestFactory

import pytest
from django_sendfile import sendfile

from privates.storages import STORAGE_ALIAS, private_media_storage
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


def test_in_memory_storage_can_still_serve_files(rf: RequestFactory):
    request = rf.get("/dummy")

    with temp_private_root():
        with pytest.raises(Http404):
            sendfile(request, "non-existent-file.bin")

        private_media_storage.save(
            "some-file.bin", File(BytesIO(b"contentisnotrelevant"))
        )

        success_response = sendfile(request, "some-file.bin")

        assert success_response.status_code == 200
