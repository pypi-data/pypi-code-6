from __future__ import absolute_import

from django.conf.urls import patterns, url

urlpatterns = patterns('dynamic_search.views',
    url(r'^search/$', 'search', name='search'),
)


