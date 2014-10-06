from sitemapper.mixins import Sitemap
from .models import Demo


class DemoSitemap(Sitemap):
    default_changefreq = 'weekly'
    default_priority = 0.5
    queryset = Demo.objects.all()

    def lastmod(self, obj):
        return obj.modified
