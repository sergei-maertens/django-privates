from django.conf import settings

from privates.storages import PrivateMediaFileSystemStorage, private_media_storage
from privates.test import temp_private_root


def test_default_settings():
    assert private_media_storage.base_location == settings.PRIVATE_MEDIA_ROOT
    assert private_media_storage.base_url == "/protected/"


def test_override_settings():
    old_private_media_root = settings.PRIVATE_MEDIA_ROOT

    with temp_private_root():
        assert private_media_storage.base_location != old_private_media_root
        assert settings.SENDFILE_ROOT != old_private_media_root


def test_change_url(settings):
    assert private_media_storage.base_url == "/protected/"
    settings.PRIVATE_MEDIA_URL = "/overridden"
    assert private_media_storage.base_url == "/overridden"


def test_explicit_base_url():
    storage = PrivateMediaFileSystemStorage(base_url="/overridden")
    assert storage.base_url == "/overridden/"
