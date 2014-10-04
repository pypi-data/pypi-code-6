# Django
from django.contrib import admin
try:
    from django.contrib.contenttypes.admin import GenericStackedInline
except ImportError:
    from django.contrib.contenttypes.generic import GenericStackedInline

# Local
from .models import SitemapEntry


class SitemapEntryInline(GenericStackedInline):
    model = SitemapEntry
    max_num = 1


class SitemapEntryAdmin(admin.ModelAdmin):
    list_display = (
        'content_object',
        'content_type',
        'object_id',
        'changefreq',
        'priority',
        )

admin.site.register(SitemapEntry, SitemapEntryAdmin)
