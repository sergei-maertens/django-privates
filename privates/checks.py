from collections.abc import Sequence
from pathlib import Path

from django.apps import AppConfig
from django.conf import settings
from django.core.checks import Error, Warning, register
from django.core.exceptions import ImproperlyConfigured

from .storages import STORAGE_ALIAS, private_media_storage


@register
def check_configuration(app_configs: Sequence[AppConfig] | None, **kwargs):
    run_check = app_configs is None or any(
        app_config.name == "privates" for app_config in app_configs
    )
    if not run_check:
        return []

    warnings_and_errors: list[Error | Warning] = []

    try:
        location: Path | str | None = getattr(private_media_storage, "location", None)
    except ImproperlyConfigured:
        if STORAGE_ALIAS not in settings.STORAGES:
            warnings_and_errors.append(
                Error(
                    "The 'privates' storage is not configured.",
                    hint=(
                        "Add the 'privates' key to the STORAGES setting - see the "
                        "quickstart documentation for details."
                    ),
                    id="privates.E001",
                )
            )
            return warnings_and_errors
        raise  # pragma: no cover

    # check if it doesn't accidentally is publicly exposed
    if location and Path(location) == Path(settings.MEDIA_ROOT).resolve():
        warnings_and_errors.append(
            Warning(
                "The storage location is probably public (equal to settings.MEDIA_ROOT).",
                hint=(
                    "Pass a (different) 'location' option to the storage options - see the "
                    "quickstart documentation for details."
                ),
                id="privates.W001",
            )
        )

    sf_root = getattr(settings, "SENDFILE_ROOT", None)
    if sf_root is None:
        warnings_and_errors.append(
            Error(
                "settings.SENDFILE_ROOT is not defined.",
                hint=(
                    "Define the setting with a value equal to the storage 'location' "
                    "option."
                ),
                id="privates.E002",
            )
        )
    elif location and Path(sf_root).resolve() != Path(location):
        warnings_and_errors.append(
            Warning(
                "settings.SENDFILE_ROOT is probably misconfigured.",
                hint="Typically this should match the storage 'location' option.",
                id="privates.W002",
            )
        )

    sf_url = getattr(settings, "SENDFILE_URL", None)
    if sf_url is None:
        warnings_and_errors.append(
            Error(
                "settings.SENDFILE_URL is not defined.",
                hint=(
                    "Define the setting with a value equal to the storage 'base_url' "
                    "option."
                ),
                id="privates.E003",
            )
        )
    elif (
        base_url := getattr(private_media_storage, "base_url", None)
    ) and sf_url != base_url:
        warnings_and_errors.append(
            Warning(
                "settings.SENDFILE_URL is probably misconfigured.",
                hint="Typically this should match the storage 'base_url' option.",
                id="privates.W003",
            )
        )

    return warnings_and_errors
