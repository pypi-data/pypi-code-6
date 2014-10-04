from django.contrib import sitemaps
from .models import SitemappedModel


class Sitemap(sitemaps.Sitemap):

    def __init__(self):
        self.queryset.model.sitemap_entry = SitemappedModel.sitemap_entry

    def items(self):
        return self.queryset.filter()

    def changefreq(self, obj):
        try:
            setting = obj.sitemap_entry.get_changefreq_display()
        except:
            setting = self.default_changefreq
        return setting

    def priority(self, obj):
        try:
            setting = obj.sitemap_entry.priority
        except:
            setting = self.default_priority
        return setting
