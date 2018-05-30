from django.contrib.admin.widgets import AdminFileWidget
from django.urls import reverse


class PrivateFileWidgetMixin:

    def __init__(self, *args, **kwargs):
        self.url_name = kwargs.pop('url_name')
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        """
        Return value-related substitutions.
        """
        context = super().get_context(name, value, attrs)
        context['url'] = reverse(self.url_name, kwargs={'pk': value.instance.pk}) if value else ''
        return context


class PrivateFileWidget(PrivateFileWidgetMixin, AdminFileWidget):
    template_name = 'admin/widgets/clearable_private_file_input.html'
