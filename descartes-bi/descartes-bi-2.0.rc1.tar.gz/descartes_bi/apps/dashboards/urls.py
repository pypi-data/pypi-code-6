from __future__ import absolute_import

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import DashboardDetailView, DashboardListView

urlpatterns = patterns('',
    url(r'^$', login_required(DashboardListView.as_view()), name='dashboard_list'),
    url(r'^(?P<pk>\d+)/$', login_required(DashboardDetailView.as_view()), name='dashboard_view'),
)
