# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
    '',
    url('^$', 'debuggie.views.debug_status'),
    url('^toggle$', 'debuggie.views.debug_toggle'),
    url('^clear$', 'debuggie.views.debug_clear'),
)
