from django.db import models
from django.utils.translation import ugettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from mpesa.conf import *

PAYMENT_RECEIVED = "received"
PAYMENT_PENDING = "pending"


class MpesaPayment(models.Model):

    ipn_id = models.CharField(_("The IPN id."), max_length=256, unique=True)
    origin = models.CharField(_("This is the source of the notification."), max_length=128)
    destination = PhoneNumberField(_("Your business terminal MSISDN (phone number)"))

    recieved_at = models.DateTimeField(_("The date and time at which the IPN was received"))
    message = models.TextField(_("The text message received from M-Pesa"))

    reference_number = models.CharField(max_length=16, unique=True)
    account = models.CharField(_("The account entered by the subscriber on their Pay Bill transaction"),
                        null=True, blank=True, max_length=128)
    subscriber_phone_number = PhoneNumberField(_("The phone number from which this payment was made."))
    subscriber_name = models.CharField(_("The sender's name"), max_length=128)

    transaction_datetime = models.DateTimeField(blank=True)
    amount = models.DecimalField(decimal_places=2, max_digits=12)

    paybill_number = models.IntegerField(_("The Pay Bill number used for this transaction"))
    customer_id = models.CharField(max_length=128)

    def __unicode__(self):
        return "%s, KSh %s" % (self.reference_number, self.amount)
