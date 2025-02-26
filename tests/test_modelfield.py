from django.conf import settings

import pytest

from privates.storages import PrivateMediaStorage
from testapp.models import File


def test_private_media_file_field():
    file = File()
    assert isinstance(file.file.storage, PrivateMediaStorage)
    assert file.file.storage.base_location == settings.PRIVATE_MEDIA_ROOT


@pytest.mark.django_db
def test_url_property(private_file):
    # outside if the admin, the URL property must use django's default behaviour
    url = private_file.file.url

    assert url.startswith("/protected/")
    assert "dummy" in url
    assert url.endswith(".txt")
