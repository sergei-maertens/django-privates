from typing import Optional, Sequence, Type

from django.contrib.auth import get_permission_codename
from django.db import models
from django.urls import re_path

from .fields import PrivateMediaFieldMixin
from .views import PrivateMediaView
from .widgets import PrivateFileWidget


class PrivateMediaMixin:
    private_media_fields: Optional[Sequence[str]] = None
    private_media_no_download_fields: Sequence[str] = ()
    private_media_permission_required: Optional[str] = None
    private_media_view_class = PrivateMediaView
    private_media_file_widget = PrivateFileWidget
    # options passed through to sendfile, as a dict
    private_media_view_options = None

    model: Type[models.Model]

    def get_private_media_fields(self):
        if self.private_media_fields is not None:
            return self.private_media_fields

        # introspect model fields to automatically figure out the field names
        field_names = [
            field.name
            for field in self.model._meta.get_fields()
            if isinstance(field, PrivateMediaFieldMixin)
        ]
        return field_names

    def get_private_media_permission_required(self, field: str) -> str:
        if self.private_media_permission_required:
            return self.private_media_permission_required

        opts = self.opts
        codename = get_permission_codename("change", opts)
        return "%s.%s" % (opts.app_label, codename)

    def get_private_media_view_options(self, field):
        return self.private_media_view_options or {}

    def get_private_media_view(self, field):
        View = self.private_media_view_class
        return View.as_view(
            model=self.model,
            file_field=field,
            permission_required=self.get_private_media_permission_required(field),
            sendfile_options=self.get_private_media_view_options(field),
        )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        private_media_fields = self.get_private_media_fields()
        if db_field.name in private_media_fields:
            # replace the widget
            view_name = self._get_private_media_view_name(db_field.name)
            # TODO: don't nuke potential other overrides?
            Widget = self.private_media_file_widget
            field.widget = Widget(
                url_name="admin:%s" % view_name,
                download_allowed=db_field.name
                not in self.private_media_no_download_fields,
            )
        return field

    def _get_private_media_view_name(self, field):
        name = "%(app_label)s_%(model_name)s_%(field)s" % {
            "app_label": self.opts.app_label,
            "model_name": self.opts.model_name,
            "field": field,
        }
        return name

    def get_urls(self):
        default = super().get_urls()

        extra = []
        for field in self.get_private_media_fields():
            if field in self.private_media_no_download_fields:
                continue
            view = self.get_private_media_view(field)
            extra.append(
                re_path(
                    r"^(?P<pk>\d+)/%s/$" % field,
                    self.admin_site.admin_view(view),
                    name=self._get_private_media_view_name(field),
                )
            )

        return extra + default
