# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from rstamper.views import Stamps, Refresh

urlpatterns = patterns('',
    url(r'^$', Stamps.as_view(), name='app_stamper-stamper'),
    url(r'^stamper/ajax/refresh$', Refresh.as_view(),
        name='app_stamper-refresh'),

)
