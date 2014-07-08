from django.contrib import admin

from .models import Image


class ImageAdmin(admin.ModelAdmin):
    list_display = ("admin_thumbnail", "admin_url", "created", "height", "width")
    list_filter = ("created",)

admin.site.register(Image, ImageAdmin)
