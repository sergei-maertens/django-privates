import copy

from django.conf import settings
from django.test import override_settings

from .storages import STORAGE_ALIAS


def temp_private_root():
    _original = copy.deepcopy(settings.STORAGES)
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
    )
