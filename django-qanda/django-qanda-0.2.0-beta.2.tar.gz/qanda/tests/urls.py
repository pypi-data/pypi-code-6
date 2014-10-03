from django.conf.urls import url, include
from django.contrib.sitemaps.views import sitemap
from qanda.sitemaps import QuestionSitemap

sitemaps = {
    'questions': QuestionSitemap,
    }

urlpatterns = [
    url(r'^faq/', include('qanda.urls')),
    url(r'^sitemap\.xml$',
        sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap',
        )
    ]
