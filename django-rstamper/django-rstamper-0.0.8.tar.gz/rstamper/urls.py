# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from rstamper.views import (Stamps,
                            Refresh,
                            CustomersApi,
                            CustomersDelApi,
                            StampsApi)

urlpatterns = patterns('',
    url(r'^stamper/$',
        Stamps.as_view(),
        name='app_stamper-index'
    ),
    url(r'^stamper/ajax/refresh$',
        Refresh.as_view(),
        name='app_stamper-refresh'
    ),
    url(r'^stamper/api/customers/$',
        CustomersApi.as_view(),
        name='app_stamper-api-customers'
    ),
    url(r'^stamper/api/customers/delete$',
        CustomersDelApi.as_view(),
        name='app_stamper-api-stamps'
    ),
    url(r'^stamper/api/stamps/$',
        StampsApi.as_view(),
        name='app_stamper-api-stamps'
    ),

)
