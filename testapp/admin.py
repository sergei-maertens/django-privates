import uuid

from django.contrib import admin
from django.core.cache import cache

from privates.admin import PrivateMediaMixin

from .models import File, File2, File3, File4


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


@admin.register(File4)
class File4Admin(PrivateMediaMixin, admin.ModelAdmin):
    readonly_fields = ("file",)

    def save_model(self, request, obj, form, change) -> None:
        super().save_model(request, obj, form, change)
        # caching triggers pickle under the hood
        cache.set(str(uuid.uuid4()), obj)
