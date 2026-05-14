import copy

from django.conf import settings
from django.core.signals import setting_changed
from django.dispatch import receiver
from django.test import override_settings
from django.utils.functional import empty

from .storages import STORAGE_ALIAS, private_media_storage


@receiver(setting_changed)
def update_filefield_storage(setting, **kwargs):
    if setting == "STORAGES":
        private_media_storage._wrapped = empty  # type: ignore


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
