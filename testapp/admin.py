from pickle import UnpicklingError

from django.contrib import admin

from privates.admin import PrivateMediaMixin

from .models import CacheModel, File, File2, File3, File4


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


@admin.register(CacheModel)
class CacheModelAdmin(PrivateMediaMixin, admin.ModelAdmin):
    private_media_fields = ("file",)
    readonly_fields = ("file",)

    # TODO: raise this at the correct moment/place?
    def __getstate__(self) -> dict:
        raise UnpicklingError
