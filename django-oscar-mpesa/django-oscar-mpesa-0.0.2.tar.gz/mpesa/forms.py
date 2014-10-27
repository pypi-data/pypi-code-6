import decimal
from datetime import datetime

from django import forms
from django.utils.translation import ugettext_lazy as _

from mpesa.models import MpesaPayment

TRANSACTION_DATE_FORMAT = "%d/%m/%y"
TRANSACTION_TIME_FORMAT = "%I:%M %p"


class IPNReceiverForm(forms.ModelForm):

    class Meta:
        model = MpesaPayment
        fields = "__all__"

    def clean_amount(self):
        try:
            amount = decimal.Decimal(self.data["amount"])
        except decimal.DecimalException:
            raise forms.ValidationError(_("Invalid amount"), code='invalid')

        if amount < 0:
            # M-Pesa will send an IPN when the account holder withdraws
            # money. From the application's perspective, this is not a payment
            # and is therefore invalid
            raise forms.ValidationError(
                    _("Amount should be more than 0.00 for a valid payment."),
                    code='not-payment')

        return amount

    def clean_transaction_datetime(self):
        date_string = self.data["transaction_date"]
        time_string = self.data["transaction_time"]

        date = datetime.strptime(date_string, TRANSACTION_DATE_FORMAT).date()
        time = datetime.strptime(time_string, TRANSACTION_TIME_FORMAT).time()

        return datetime.combine(date, time)

class TransactionReferenceForm(forms.Form):

	reference_number = forms.CharField(label=_("Transaction Reference No."))
