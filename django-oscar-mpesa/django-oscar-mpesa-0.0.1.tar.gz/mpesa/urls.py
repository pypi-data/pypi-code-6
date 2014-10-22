from django.conf.urls import patterns, url, include

from mpesa.dashboard.app import application as mpesa_dashboard_app
from mpesa import views


urlpatterns = patterns('',
    url(r'^checkout/mpesa/', views.MpesaPaymentDetailsView.as_view(),
        name='mpesa-payment-details'),
    url(r'^dashboard/mpesa/', include(mpesa_dashboard_app.urls)),
)
