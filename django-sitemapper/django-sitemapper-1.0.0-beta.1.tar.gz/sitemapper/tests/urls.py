from django.conf.urls import url
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from django.views.generic import base

from sitemapper.tests.test_sitemap import DummySitemap


class TestView(base.View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello Test World!')


sitemaps = {
    'tests': DummySitemap,
    }


urlpatterns = [

    url(r'^(?P<slug>[-_\w]+)/$',
        TestView.as_view(),
        name='sitemapper.tests.views.detail'
        ),

    url(r'^sitemap\.xml', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),

    ]
