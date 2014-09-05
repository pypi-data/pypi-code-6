from django.contrib.sitemaps import Sitemap
from huron.blog.models import Post


class BlogSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.6

    def items(self):
        return Post.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.last_mod
