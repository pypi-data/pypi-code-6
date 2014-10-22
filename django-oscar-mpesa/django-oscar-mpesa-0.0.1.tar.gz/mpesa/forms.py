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

    def clean_transaction_datetime(self):
        date_string = self.data["transaction_date"]
        time_string = self.data["transaction_time"]

        date = datetime.strptime(date_string, TRANSACTION_DATE_FORMAT).date()
        time = datetime.strptime(time_string, TRANSACTION_TIME_FORMAT).time()

        return datetime.combine(date, time)

class TransactionReferenceForm(forms.Form):

	reference_number = forms.CharField(label=_("Transaction Reference No."))
