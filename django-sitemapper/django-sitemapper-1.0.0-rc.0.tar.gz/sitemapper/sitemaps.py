# Django
from django.contrib import sitemaps

# Local
from .models import SitemapEntry


class SitemapBase(sitemaps.Sitemap):
    """The root class for sitemapper.Sitemaps.

    Inherits from django.contrib.sitemaps.Sitemap and overrides the
    Sitemap.items() method.

    In this class calling items() does two things:

    1. It creates a private attribute ``_entries`` containing a dictionary of
       sitemapper.SitemapEntry objects having the same ContentType as the
       supplied queryset's model. This dictionary is keyed to the object_id of
       each SitemapEntry instance.

    2. It then returns the queryset.

    Attributes:

      queryset (queryset): A queryset containing the objects to appear in
        the sitemap.

      _entries (dict): A private variable populated by the items() method and
        containing SitemapEntries matching the ContentType and object_id of the
        queryset above.
    """

    def _get_entries_for_model(self, model):
        """
        Return a dictionary of sitemapper.SitemapEntry objects whose
        ContentType matches ``model``. The dictionary is keyed to the
        SitemapEntry's object_id.

        Args:

          model (class): This is the model class or instance to be filtered on.
        """
        entries = SitemapEntry.objects.get_for_model(model)
        return {entry.object_id: entry for entry in entries}

    def items(self):
        """
        Assign the result of _get_entries_for_model(model) to the private
        attribute _entries, and return the queryset attribute.
        """
        self._entries = self._get_entries_for_model(self.queryset.model)
        return self.queryset.filter()


class Sitemap(SitemapBase):

    def changefreq(self, item):
        """
        Return one of three values:

        1. the SitemapEntry.changefreq related to ``item``, if set;
        2. or, the default_changefreq, if set;
        3. or, None

        Args:
          item (model instance): An member instance of self.queryset.
        """
        default = getattr(self, 'default_changefreq', None)
        try:
            changefreq = self._entries.get(item.id).get_changefreq_display()
        except AttributeError:
            changefreq = None
        return changefreq or default

    def priority(self, item):
        """
        Return one of three values:

        1. the SitemapEntry.priority related to ``item``, if set;
        2. or, the default_priority, if set;
        3. or, None

        Args:
          item (model instance): An member instance of self.queryset.
        """
        default = getattr(self, 'default_priority', None)
        try:
            priority = self._entries.get(item.id).get_priority_display()
        except AttributeError:
            priority = None
        return priority or default


class GenericSitemap(Sitemap):
    """
    A sub-class of Sitemapper which emulates
    django.contrib.sitemaps.GenericSitemap, except that any supplied
    ``priority`` or ``changefreq`` args set the corresponding default_*
    attributes.

    Args:

      info_dict (dictionary): Optional dictionary which may contain
        ``date_field`` and, or, ``queryset``.

      priority (string or float): Optional value assigned internally to
        ``default_priority`` and used **only** if not overridden by a
        SitemapEntry.

      changefreq (string): Optional value assigned internally to
        ``default_changefreq`` and used **only** if not overridden by a
        SitemapEntry. Must be one of: 'always' 'hourly', 'daily', 'weekly',
        'monthly', 'yearly' or 'never'.
    """

    def __init__(self, info_dict={}, priority=None, changefreq=None):

        queryset = info_dict.get('queryset', None)
        if queryset:
            self.queryset = queryset

        date_field = info_dict.get('date_field', None)
        if date_field:
            self.date_field = date_field

        if priority:
            self.default_priority = priority

        if changefreq:
            self.default_changefreq = changefreq

    def lastmod(self, item):
        if self.date_field is not None:
            return getattr(item, self.date_field)
        return None
