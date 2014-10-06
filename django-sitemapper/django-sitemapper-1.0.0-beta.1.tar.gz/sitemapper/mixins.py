# Django
from django.contrib import sitemaps
from django.contrib.contenttypes.models import ContentType

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
        ctype = ContentType.objects.get_for_model(model)
        entries = SitemapEntry.objects.filter(content_type=ctype)
        return {entry.object_id: entry for entry in entries}

    def items(self):
        self._entries = self._get_entries_for_model(self.queryset.model)
        return self.queryset.filter()

    def changefreq(self, obj):
        try:
            return self._entries.get(obj.id).get_changefreq_display()
        except AttributeError:
            return getattr(self, 'default_changefreq', None)

    def priority(self, obj):
        try:
            return self._entries.get(obj.id).priority
        except AttributeError:
            return getattr(self, 'default_priority', None)
