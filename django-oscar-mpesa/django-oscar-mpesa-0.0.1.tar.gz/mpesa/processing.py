from django.dispatch import receiver
from django.db.models import get_model
from django.db import transaction

from oscar.apps.checkout.signals import post_checkout

from mpesa.models import MpesaPayment, PAYMENT_RECEIVED, PAYMENT_PENDING
from mpesa.signals import ipn_received, payment_accepted, unknown_payment_received

Transaction = get_model("payment", "Transaction")


@receiver(post_checkout)
@transaction.atomic()
def process_created_order(sender, **kwargs):
    """
    This receives the signal sent out after an order has been created successfully.
    For this order we iterate over the transactions in its payment sources and check
    if a payment for that transaction has been made via mpesa. If it has, then we mark the
    transaction as PAID. We send out a signal after this and how this signal is consumed is
    implementation dependent. Ideally the consumer should mark an order as fully paid or whatever
    status they find suitable.

    :kwargs: Contains the order that was created
    """

    order = kwargs['order']
    for source in order.sources.all():
        if source.source_type.name == "M-Pesa":
            for transaction in source.transactions.all():
                process_transaction(transaction)


@receiver(ipn_received)
@transaction.atomic()
def process_payment_notification(sender, **kwargs):
    mpesa_payment = kwargs['mpesa_payment']
    try:
        transaction = Transaction.objects.get(
                        reference=mpesa_payment.reference_number,
                        status=PAYMENT_PENDING)
        return process_transaction(transaction, mpesa_payment)
    except Transaction.DoesNotExist:
        # user hasn't sent the ref code yet
        unknown_payment_received.send(sender="payment_processor", mpesa_payment=mpesa_payment)
        return


def process_transaction(transaction, payment=None):
    ref_no = transaction.reference
    source = transaction.source

    if payment is None:
        try:
            payment = MpesaPayment.objects.get(reference_number=ref_no)
        except MpesaPayment.DoesNotExist:
            # if we reach here we have to return, we cannot debit a source
            # if the payment doesn't exist.
            return

    source.amount_debited = payment.amount
    source.save()

    transaction.amount = payment.amount
    transaction.status = PAYMENT_RECEIVED
    transaction.save()

    payment_accepted.send(sender="payment_processor", mpesa_payment=payment, transaction=transaction)
