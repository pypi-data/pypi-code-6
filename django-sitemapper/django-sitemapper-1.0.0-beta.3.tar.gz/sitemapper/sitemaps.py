# Django
from django.contrib import sitemaps

# Local
from .models import SitemapEntry


class Sitemap(sitemaps.Sitemap):

    def __init__(self, *args, **kwargs):

        priority = kwargs.get('priority')
        if priority:
            self.default_priority = priority

        changefreq = kwargs.get('changefreq')
        if changefreq:
            self.default_changefreq = changefreq

    def _get_entries_for_model(self, model):
        """
        Look up any SitemapEntries for given model and return them in a
        dictionary keyed to the related object's ID.
        """
        entries = SitemapEntry.objects.get_for_model(model)
        return {entry.object_id: entry for entry in entries}

    def items(self):
        self._entries = self._get_entries_for_model(self.queryset.model)
        return self.queryset.filter()

    def changefreq(self, obj):
        default = getattr(self, 'default_changefreq', None)
        try:
            changefreq = self._entries.get(obj.id).get_changefreq_display()
        except AttributeError:
            changefreq = None
        return changefreq or default

    def priority(self, obj):
        default = getattr(self, 'default_priority', None)
        try:
            priority = self._entries.get(obj.id).get_priority_display()
        except AttributeError:
            priority = None
        return priority or default
