from django.contrib.sitemaps import Sitemap
from .models import Question


class QuestionSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return Question.published.for_anonymous()

    def lastmod(self, obj):
        return obj.modified
