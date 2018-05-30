from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import DetailView

from sendfile import sendfile


class PrivateMediaView(PermissionRequiredMixin, DetailView):
    """
    Verify the permission required and send the filefield via sendfile.

    :param permission_required: the permission required to view the file
    :param model: the model class to look up the object
    :param file_field: the name of the ``Filefield``
    """
    file_field = None

    def get(self, request, *args, **kwargs):
        filename = getattr(self.get_object(), self.file_field).path
        return sendfile(request, filename)
