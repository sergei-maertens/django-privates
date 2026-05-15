import copy

from django.conf import settings
from django.core.files import File
from django.core.files.storage import InMemoryStorage
from django.core.files.storage.memory import InMemoryDirNode  # type: ignore
from django.core.signals import setting_changed
from django.dispatch import receiver
from django.http import HttpResponse
from django.test import override_settings
from django.test.testcases import SimpleTestCase
from django.utils.functional import empty

from django_sendfile.utils import _get_sendfile

from .storages import STORAGE_ALIAS, private_media_storage

__all__ = ["temp_private_root"]


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


class temp_private_root(override_settings):
    """
    Set up an isolated private media storage.

    You can use this as a test class or test decorator. When enabled, the private media
    storage will be replaced with an in-memory storage, and the sendfile backend is
    updated to serve files from the in-memory storage.

    :param reset_storage: If enabled (by default it is), the storage contents are reset
      in the test cleanup function when used as a class decorator.
    :param update_sendfile_backend: If enabled (by default it is), the sendfile backend
      is updated with a custom backend to serve files from the in-memory storage.
    """

    def __init__(
        self,
        reset_storage: bool = True,
        update_sendfile_backend: bool = True,
    ):
        self._reset_storage = reset_storage

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

        options = {
            "STORAGES": new_storages,
            # files don't exist on disk when using the the inmemorystorage
            "SENDFILE_CHECK_FILE_EXISTS": False,
        }
        if update_sendfile_backend:
            options["SENDFILE_BACKEND"] = __name__

        super().__init__(**options)

    def decorate_class(self, cls):
        cls = super().decorate_class(cls)

        assert issubclass(cls, SimpleTestCase), (
            "Can only decorate subclasses of SimpleTestCase"
        )

        decorated_setUp = cls.setUp

        def setUp(inner_self: SimpleTestCase):
            decorated_setUp(inner_self)
            inner_self.addCleanup(clear_storage)

        def clear_storage():
            if not isinstance(private_media_storage, InMemoryStorage):
                return
            if not self._reset_storage:
                return
            # reset the root node
            private_media_storage._root = InMemoryDirNode()

        cls.setUp = setUp
        return cls
