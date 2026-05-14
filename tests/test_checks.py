from collections.abc import Collection

from django.apps import apps
from django.conf.global_settings import STORAGES as DEFAULT_STORAGES
from django.core.checks import Error, Warning
from django.core.exceptions import ImproperlyConfigured

import pytest

from privates.checks import check_configuration


def test_skip_check_if_app_config_not_requested(settings):
    settings.STORAGES = DEFAULT_STORAGES

    errors = check_configuration([])

    assert errors == []


def test_errors_when_storage_key_is_missing(settings):
    settings.STORAGES = DEFAULT_STORAGES

    errors = check_configuration([apps.get_app_config("privates")])

    assert len(errors) == 1
    assert errors[0] == Error(
        "The 'privates' storage is not configured.",
        hint=(
            "Add the 'privates' key to the STORAGES setting - see the quickstart "
            "documentation for details."
        ),
        id="privates.E001",
    )


def test_raises_improperlyconfigured_on_broken_configuration(settings):
    settings.STORAGES = {
        **DEFAULT_STORAGES,
        "privates": {
            "BACKEND": "i.do.not.exist.FooBackend",
        },
    }

    with pytest.raises(ImproperlyConfigured):
        check_configuration(None)


def test_warns_for_common_misconfigurations(settings):
    settings.STORAGES = {
        **DEFAULT_STORAGES,
        "privates": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
    }
    settings.SENDFILE_ROOT = "/other"
    settings.SENDFILE_URL = "/other/"

    warnings_by_id = {w.id: w for w in check_configuration(None)}

    assert warnings_by_id["privates.W001"] == Warning(
        "The storage location is probably public (equal to settings.MEDIA_ROOT).",
        hint=(
            "Pass a (different) 'location' option to the storage options - see the "
            "quickstart documentation for details."
        ),
        id="privates.W001",
    )
    assert warnings_by_id["privates.W002"] == Warning(
        "settings.SENDFILE_ROOT is probably misconfigured.",
        hint="Typically this should match the storage 'location' option.",
        id="privates.W002",
    )
    assert warnings_by_id["privates.W003"] == Warning(
        "settings.SENDFILE_URL is probably misconfigured.",
        hint="Typically this should match the storage 'base_url' option.",
        id="privates.W003",
    )


def test_warns_for_missing_sendfile_settings(settings):
    del settings.SENDFILE_ROOT
    del settings.SENDFILE_URL

    errors_by_id = {e.id: e for e in check_configuration(None)}

    assert errors_by_id["privates.E002"] == Error(
        "settings.SENDFILE_ROOT is not defined.",
        hint=(
            "Define the setting with a value equal to the storage 'location' option."
        ),
        id="privates.E002",
    )
    assert errors_by_id["privates.E003"] == Error(
        "settings.SENDFILE_URL is not defined.",
        hint=(
            "Define the setting with a value equal to the storage 'base_url' option."
        ),
        id="privates.E003",
    )


def test_doesnt_crash_for_weird_storages(settings):
    settings.STORAGES = {
        **DEFAULT_STORAGES,
        "privates": {
            "BACKEND": "django.core.files.storage.base.Storage",
        },
    }

    result = check_configuration(None)

    assert isinstance(result, Collection)
