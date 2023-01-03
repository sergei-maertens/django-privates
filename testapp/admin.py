from django.contrib import admin

from privates.admin import PrivateMediaMixin

from .models import File, File2, File3


@admin.register(File)
class FileAdmin(PrivateMediaMixin, admin.ModelAdmin):
    private_media_fields = ("file", "image")
    private_media_view_options = {"attachment": True}


@admin.register(File2)
class FileAdmin2(FileAdmin):
    private_media_fields = ("file", "image")
    private_media_no_download_fields = ("image",)


@admin.register(File3)
class File3Admin(PrivateMediaMixin, admin.ModelAdmin):
    pass
