from django.views.generic import FormView
from django.http import HttpResponse
from django.db import IntegrityError

from django.conf import settings

from mpesa.forms import IPNReceiverForm
from mpesa.utils import parse_ipn_data
from mpesa import signals

# we have to make django process this file to register the signal handlers
from mpesa.processing import *


class IPNReceiverView(FormView):

    PAYMENT_ACCEPTED_MSG = 'OK|Payment accepted.'
    AUTHENTICATION_FAILURE_MSG = 'FAIL|Paybill authentication failure.'
    MISSING_DATA_ERROR_MSG = "FAIL|The following parameters are missing: %s"
    PAYBILL_ERROR = 'FAIL|Paybill error. Safaricom is experiencing issues.'
    TRANSACTION_ALREADY_EXISTS_MSG = 'FAIL|This notification has already been received'

    form_class = IPNReceiverForm

    def get_form_kwargs(self):
        kwargs = super(IPNReceiverView, self).get_form_kwargs()

        kwargs["data"] = parse_ipn_data(self.request.GET)

        return kwargs

    def authenticate_request(self, request):
        username = request.GET.get("user")
        password = request.GET.get("pass")

        try:
            assert username == settings.MPESA_IPN_USER
            assert password == settings.MPESA_IPN_PASS
        except AssertionError:
            return False

        return True

    def form_invalid(self, form):
        return HttpResponse(self.PAYBILL_ERROR, status=200)

    def form_valid(self, form):
        try:
            mpesa_payment = form.save()
        except IntegrityError:
            return HttpResponse(self.TRANSACTION_ALREADY_EXISTS_MSG, status=200)

        signals.ipn_received.send(sender=self, mpesa_payment=mpesa_payment)

        return HttpResponse(self.PAYMENT_ACCEPTED_MSG, status=200)

    def get(self, request, *args, **kwargs):
        if not self.authenticate_request(request):
            # TODO: Check how MPESA reacts to a 401
            return HttpResponse(self.AUTHENTICATION_FAILURE_MSG, status=401)

        # we treat this as a POST request in order to handle the form
        return super(IPNReceiverView, self).post(request, *args, **kwargs)
