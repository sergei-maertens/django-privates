from django.conf import settings

from privates.storages import PrivateMediaStorage
from testapp.models import File


def test_private_media_file_field():
    file = File()
    assert isinstance(file.file.storage, PrivateMediaStorage)
    assert file.file.storage.base_location == settings.PRIVATE_MEDIA_ROOT
