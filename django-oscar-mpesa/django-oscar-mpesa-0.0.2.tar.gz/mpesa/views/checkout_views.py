from django.conf import settings

from oscar.apps.checkout.views import PaymentDetailsView as BasePaymentDetailsView
from oscar.apps.payment.models import SourceType, Source, Transaction

from mpesa import forms
from mpesa.models import PAYMENT_PENDING


class MpesaPaymentDetailsView(BasePaymentDetailsView):

    """
        This view has a different
        chronilogical order for the preview and payment_details views.
        In mpesa, the only payment detail collected (at least for now) is
        the reference number for the payment that a buyer has made.
        This number is entered in the last step of checkout.
    """

    template_name = "mpesa/checkout/payment_details.html"

    def get_context_data(self, **kwargs):

        ctx = super(MpesaPaymentDetailsView, self).get_context_data(**kwargs)

        ctx["transaction_reference_form"] = kwargs.get("transaction_reference_form",
                                                        forms.TransactionReferenceForm())
        ctx["paybill_number"] = settings.MPESA_PAYBILL_NUMBER

        return ctx

    def post(self, request, *args, **kwargs):
        return self.handle_place_order_submission(request)

    def handle_place_order_submission(self, request):

        transaction_reference_form = forms.TransactionReferenceForm(request.POST)
        if transaction_reference_form.is_valid():
            submission = self.build_submission(
                payment_kwargs={
                    "transaction_reference_form": transaction_reference_form
                }
            )
            return self.submit(**submission)

        # form wasn't valid
        return self.render_payment_details(request,
                    transaction_reference_form=transaction_reference_form)


    def handle_payment(self, order_number, order_total, transaction_reference_form, **kwargs):

        """
            Here we create a payment source and allocate to it the total amount of the order.
            Once the IPN for this order's payment is received, we create a Transaction for this source.
            NB: This transaction is different from MpesaTransaction.

            A source can have multiple transactions. Both Source and Transaction have a reference field
            Source.reference will store a reference unique to every order.
            Transaction.reference will store the reference number from mpesa.

            Orders should have one mpesa source. The source will have a transaction everytime
            money is sent or refunded.
        """

        ref_no = transaction_reference_form.cleaned_data['reference_number']

        source_type, __ = SourceType.objects.get_or_create(name='M-Pesa')
        source = Source(
                        source_type=source_type,
                        amount_allocated=order_total.incl_tax,
                        currency="KES")

        # in this example, we expect only one transaction to be used for the order.
        # We create a transaction with 0 amount. This transaction is only meant to store
        # the reference number. Once the IPN is received, we update this transaction with
        # the amount in the IPN, we also update the source amounts and send out the relevant
        # signal depending on the state of the payment.
        source.create_deferred_transaction(Transaction.DEBIT, 0,
                        reference=ref_no, status=PAYMENT_PENDING)

        self.add_payment_source(source)

    def get_initial_order_status(self, basket):
        return getattr(settings, "OSCAR_INITIAL_ORDER_STATUS", None)