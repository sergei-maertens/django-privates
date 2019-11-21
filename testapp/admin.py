from django.contrib import admin

from privates.admin import PrivateMediaMixin

from .models import File


@admin.register(File)
class FileAdmin(PrivateMediaMixin, admin.ModelAdmin):
    private_media_fields = ('file', 'image')
    private_media_view_options = {
        'attachment': True
    }
