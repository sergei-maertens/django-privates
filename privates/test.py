import copy

from django.conf import settings
from django.core.files import File
from django.core.signals import setting_changed
from django.dispatch import receiver
from django.http import HttpResponse
from django.test import override_settings
from django.utils.functional import empty

from django_sendfile.utils import _get_sendfile

from .storages import STORAGE_ALIAS, private_media_storage


@receiver(setting_changed)
def update_filefield_storage(setting, **kwargs):
    if setting == "STORAGES":
        private_media_storage._wrapped = empty  # type: ignore
    if setting == "SENDFILE_BACKEND":
        _get_sendfile.cache_clear()


def sendfile(request, filepath, **kwargs):
    """
    Companion sendfile backend for :func:`temp_private_root`.

    Serves the requested file from the in-memory storage backend.
    """
    with File(private_media_storage.open(filepath, "rb")) as f:
        response = HttpResponse(f.chunks())
    return response


def temp_private_root(setup_sendfile_backend: bool = True):
    _original = copy.deepcopy(settings.STORAGES)
    assert isinstance(_original, dict)
    assert isinstance(_original[STORAGE_ALIAS], dict)
    new_storages = {
        **_original,
        STORAGE_ALIAS: {
            "BACKEND": "django.core.files.storage.InMemoryStorage",
            "OPTIONS": _original[STORAGE_ALIAS].get("OPTIONS", {}),
        },
    }
    return override_settings(
        STORAGES=new_storages,
        # files don't exist on disk when using the the inmemorystorage
        SENDFILE_CHECK_FILE_EXISTS=False,
        SENDFILE_BACKEND=__name__,
    )
