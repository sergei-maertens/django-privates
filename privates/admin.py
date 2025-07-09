from collections.abc import Sequence
from typing import Generic, TypeVar

import django.db.models.options
from django.contrib.admin import AdminSite
from django.contrib.auth import get_permission_codename
from django.db import models
from django.db.models.options import Options
from django.urls import path

from .fields import PrivateMediaFieldMixin
from .views import PrivateMediaView
from .widgets import PrivateFileWidget

__all__ = ["PrivateMediaMixin"]

_ModelT = TypeVar("_ModelT", bound=models.Model)


def _get_private_media_view_name(opts: Options, field: str) -> str:
    return f"{opts.app_label}_{opts.model_name}_{field}"


class PrivateMediaMixin(Generic[_ModelT]):
    """
    Enable downloading private-media model fields in the admin.

    Use this mixin to automatically replace the Django admin file field widget so that
    private media fields can be downloaded. Django's default behaviour is to create URLs
    that are not actually served by the webserver (directly, and by design). Instead,
    a custom view is installed for each private media field of the model and registered
    in the admin URL configuration (automatically).
    """

    private_media_fields: Sequence[str] | None = None
    private_media_no_download_fields: Sequence[str] = tuple()
    """
    A list of field names for which downloads are forbidden.

    By default, the contents for private media field are made downloadable through the
    custom widget. You can block this by specifying the name of the field(s) that should
    only be writable and not downloadable.
    """
    private_media_permission_required: str | None = None
    private_media_view_class = PrivateMediaView
    """
    The Django view class to use for private media field content download views.
    """
    private_media_file_widget = PrivateFileWidget
    # options passed through to sendfile, as a dict
    private_media_view_options: dict | None = None

    admin_site: AdminSite
    model: type[_ModelT]
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
        field = super().formfield_for_dbfield(db_field, request, **kwargs)  # type: ignore
        private_media_fields = self.get_private_media_fields()
        if db_field.name in private_media_fields:
            # replace the widget
            view_name = _get_private_media_view_name(self.opts, db_field.name)
            # TODO: don't nuke potential other overrides?
            Widget = self.private_media_file_widget
            field.widget = Widget(
                url_name=f"admin:{view_name}",
                download_allowed=db_field.name
                not in self.private_media_no_download_fields,
            )
        return field

    def get_urls(self):
        default = super().get_urls()  # type: ignore

        extra = []
        for field in self.get_private_media_fields():
            if field in self.private_media_no_download_fields:
                continue
            view = self.get_private_media_view(field)
            extra.append(
                path(
                    f"<int:pk>/{field}/",
                    self.admin_site.admin_view(view),
                    name=_get_private_media_view_name(self.opts, field),
                )
            )

        return extra + default

    def get_object(self, request, object_id, from_field=None):
        """
        Override to replace the readonly private media file field accessors.

        See issue #10 - injecting the private media (admin specific) URLs for readonly
        fields is not possible since all the form field machinery gets bypassed, and
        a bunch of helpers/utilities that are private Django API are used to render a
        form, fieldsets, field lines and ultimately the field. This call chain ends up
        in ``django.db.models.fields.file.FieldFile.url``. We cannot blindly always
        return the admin URL at the model level, since these URLs should not be exposed
        to non-admin users.

        So, in the admin context we instead taint the model instance so that our custom
        ``FieldFile`` class/attr_class can introspect this and conditionally build up
        the correct URL.
        """
        obj = super().get_object(request, object_id, from_field=from_field)  # type: ignore

        readonly_fields = self.get_readonly_fields(request, obj=obj)  # type: ignore
        obj._private_media_readonly_fields = [
            field
            for field in self.get_private_media_fields()
            if field in readonly_fields
        ]

        return obj
