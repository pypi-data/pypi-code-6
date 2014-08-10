from __future__ import absolute_import

from django.conf.urls import patterns, url

from .views import HomeView

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
)
