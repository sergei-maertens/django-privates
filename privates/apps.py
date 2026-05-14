from django.apps import AppConfig


class PrivatesConfig(AppConfig):
    name = "privates"

    def ready(self):
        from . import checks  # noqa
