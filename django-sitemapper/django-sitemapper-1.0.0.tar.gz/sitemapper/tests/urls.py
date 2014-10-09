from django.conf.urls import url
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from django.views.generic import base

from sitemapper.tests.test_sitemap import SitemapBasic, SitemapWithDefaults


class TestView(base.View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello Test World!')


basic_dict = {
    'tests': SitemapBasic,
    }

withdefaults_dict = {
    'tests': SitemapWithDefaults,
    }


urlpatterns = [

    url(r'^(?P<slug>[-_\w]+)/$',
        TestView.as_view(),
        name='sitemapper.tests.views.detail'
        ),

    url(r'^sitemap-basic\.xml',
        sitemap,
        {'sitemaps': basic_dict},
        name='sitemap.basic'
        ),

    url(r'^sitemap-withdefaults\.xml',
        sitemap,
        {'sitemaps': withdefaults_dict},
        name='sitemap.with.defaults'
        ),

    ]
