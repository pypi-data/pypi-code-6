from django.conf import settings
from django.conf.urls import patterns, url, include

from mpesa.dashboard.app import application as mpesa_dashboard_app
from mpesa import views
from mpesa.test_tools import views as test_views


urlpatterns = patterns('',
    url(r'^checkout/mpesa/', views.MpesaPaymentDetailsView.as_view(),
        name='mpesa-payment-details'),
    url(r'^dashboard/mpesa/', include(mpesa_dashboard_app.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
            url(r"^ipn-gen/$", test_views.IPNGeneratorView.as_view(), name="ipn-gen"),
        )