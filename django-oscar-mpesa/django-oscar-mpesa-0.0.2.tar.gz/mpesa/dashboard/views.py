from django.views.generic import ListView, DetailView
from django.db.models import get_model

MpesaPayment = get_model("mpesa", "MpesaPayment")


class PaymentsListView(ListView):
    model = MpesaPayment
    template_name = "mpesa/dashboard/payments-list.html"
    context_object_name = "payments"


class PaymentDetailView(DetailView):

    model = MpesaPayment
    template_name = "mpesa/dashboard/payment-detail.html"
    context_object_name = "payment"
