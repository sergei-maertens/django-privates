from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import DetailView

from django_sendfile import sendfile


class PrivateMediaView(PermissionRequiredMixin, DetailView):
    """
    Verify the required permission and send the filefield content via sendfile.

    The permissions of the user are verified before sending back any data. If the user
    has the correct permissions, the path of the specified field name is looked up on
    the object and passed to sendfile, which transforms it into the appropriate response
    header so the web-server can serve the file contents.

    :param permission_required: the permission required to view the file
    :param model: the model class to look up the object
    """

    file_field: str = ""
    """
    Name of the file field on the model to look up.

    The path (on-disk) of the file is passed along to :func:`django_sendfile.sendfile`.
    """
    sendfile_options: dict | None = None
    """
    Additional options for :func:`django_sendfile.sendfile`.
    """

    def get_sendfile_opts(self) -> dict:
        return self.sendfile_options or {}

    def get(self, request, *args, **kwargs):
        filename = getattr(self.get_object(), self.file_field).path
        sendfile_options = self.get_sendfile_opts()
        return sendfile(request, filename, **sendfile_options)
