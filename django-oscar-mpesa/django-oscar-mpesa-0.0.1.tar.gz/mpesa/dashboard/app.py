from django.conf.urls import patterns, url
from django.contrib.admin.views.decorators import staff_member_required

from oscar.core.application import Application

from . import views


class MpesaDashboard(Application):

    name = None
    payments_list_view = views.PaymentsListView
    payment_detail_view = views.PaymentDetailView

    def get_urls(self):
        urls = [
            url(r"^payments/$", self.payments_list_view.as_view(),
                name="mpesa-payments-list"),
            url(r"^payment/(?P<pk>\d+)/$", self.payment_detail_view.as_view(),
                name="mpesa-payment-detail")
        ]

        return self.post_process_urls(patterns("", *urls))

    def get_url_decorator(self, url_name):
        return staff_member_required


application = MpesaDashboard()
