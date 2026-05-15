import os
from io import BytesIO
from pathlib import Path

from django.conf import settings as django_settings
from django.core.files import File
from django.core.files.storage import (
    FileSystemStorage,
    InMemoryStorage,
    default_storage,
    storages,
)
from django.http import Http404
from django.test import RequestFactory, SimpleTestCase, TestCase

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
        assert django_settings.SENDFILE_CHECK_FILE_EXISTS is False
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


def test_supports_not_overriding_the_sendfile_backend(settings):
    settings.SENDFILE_BACKEND = "django_sendfile.backends.nginx"
    with temp_private_root(update_sendfile_backend=False):
        assert django_settings.SENDFILE_BACKEND == "django_sendfile.backends.nginx"


@temp_private_root(reset_storage=False)
class NoResetStorageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        private_media_storage.save(
            "some-file.bin", File(BytesIO(b"contentisnotrelevant"))
        )

    def test_one_asserting_the_file_from_setup_testdata_still_exists(self):
        assert private_media_storage.exists("some-file.bin")

    def test_two_asserting_the_file_from_setup_testdata_still_exists(self):
        assert private_media_storage.exists("some-file.bin")


@temp_private_root(reset_storage=True)
class ResetStorageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        private_media_storage.save(
            "some-file.bin", File(BytesIO(b"contentisnotrelevant"))
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

        assert isinstance(private_media_storage, InMemoryStorage)
        assert not private_media_storage.exists("some-file.bin")

    def test_file_exists_inside_test(self):
        assert private_media_storage.exists("some-file.bin")


@temp_private_root(reset_storage=True)
class ResiliencyTests(SimpleTestCase):
    def test_doesnt_crash_for_other_storage_backends(self):
        assert isinstance(default_storage, FileSystemStorage)
        private_media_storage._wrapped = default_storage._wrapped  # type: ignore
