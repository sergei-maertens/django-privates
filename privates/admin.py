from typing import Optional, Sequence, Type

import django.db.models.options
from django.contrib.auth import get_permission_codename
from django.db import models
from django.urls import re_path

from .fields import PrivateMediaFieldMixin
from .views import PrivateMediaView
from .widgets import PrivateFileWidget


class PrivateMediaMixin:
    """
    Enable downloading private-media model fields in the admin.

    Use this mixin to automatically replace the Django admin file field widget so that
    private media fields can be downloaded. Django's default behaviour is to create URLs
    that are not actually served by the webserver (directly, and by design). Instead,
    a custom view is installed for each private media field of the model and registered
    in the admin URL configuration (automatically).
    """

    private_media_fields: Optional[Sequence[str]] = None
    private_media_no_download_fields: Sequence[str] = tuple()
    """
    A list of field names for which downloads are forbidden.

    By default, the contents for private media field are made downloadable through the
    custom widget. You can block this by specifying the name of the field(s) that should
    only be writable and not downloadable.
    """
    private_media_permission_required: Optional[str] = None
    private_media_view_class = PrivateMediaView
    """
    The Django view class to use for private media field content download views.
    """
    private_media_file_widget = PrivateFileWidget
    # options passed through to sendfile, as a dict
    private_media_view_options: Optional[dict] = None

    model: Type[models.Model]
    opts: django.db.models.options.Options

    def get_private_media_fields(self) -> Sequence[str]:
        """
        Return a sequence of model field names that are private media fields.

        By default, all private media fields are detected automatically. You can
        override this with the :attr:`private_media_fields` attribute or by overriding
        this method.
        """
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
        """
        Return the permission required to download private media field contents.

        The permission is specified in Django's typical format:
        ``{app_label}.change_{model_name}``. By default, users are allowed to download
        the model field contents if they have change permissions for the model.

        Override this method if you want to use permissions specific to a particular
        field or set of fields, or specify :attr:`private_media_permission_required`
        for an alternative static permission.

        :arg field: name of the private media field
        """
        if self.private_media_permission_required:
            return self.private_media_permission_required
        codename = get_permission_codename("change", self.opts)
        return f"{self.opts.app_label}.{codename}"

    def get_private_media_view_options(self, field: str) -> dict:
        """
        Specify any additional options to forward to :func:`django_sendfile.sendfile`.
        """
        return self.private_media_view_options or {}

    def get_private_media_view(self, field: str):
        """
        Construct a view for the given private media field on the model.
        """
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

    def _get_private_media_view_name(self, field: str) -> str:
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
