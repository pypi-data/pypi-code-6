from __future__ import absolute_import

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import WidgetRenderView

urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/$', login_required(WidgetRenderView.as_view()), name='widget_render'),
)
