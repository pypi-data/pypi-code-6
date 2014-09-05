# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('huron.pages.views',
    url(r'^(?P<page_slug>[-\w]+)/$', 'page', name="single"),
)
