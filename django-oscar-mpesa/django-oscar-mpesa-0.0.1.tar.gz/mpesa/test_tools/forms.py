import decimal
import random
import datetime
import string

from django import forms
from django.conf import settings

NAMES = ["LINDA", "BARBARA", "KAREN", "SHARON", "MICHELLE", "ANGELA",
         "MARTHA", "DEBRA", "AMANDA", "STEPHANIE", "CAROLYN", "CHRISTINE",
         "MARIE", "JANET", "CATHERINE", "FRANCES", "ANN", "JOYCE", "DIANE",
         "ALICE", "JULIE"]

from mpesa.forms import TRANSACTION_DATE_FORMAT, TRANSACTION_TIME_FORMAT


class IPNForm(forms.Form):

    """
        Creates a dict that can be fed to the IPNReceiverForm to create an MpesaPayment
    """

    reference_number = forms.CharField(required=False)
    amount = forms.CharField(required=False)
    paybill_account = forms.CharField(required=False)

    def clean_reference_number(self):
        ref_number = self.cleaned_data["reference_number"]

        if not ref_number:
            ref_number = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

        return ref_number

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if not amount:
            amount = random.randint(0, 70000)

        try:
            amount = decimal.Decimal(amount)
        except decimal.DecimalException as e:
            raise forms.ValidationError("Please enter a valid amount")

        return str(amount)

    def clean_paybill_account(self):
        account = self.cleaned_data["paybill_account"]
        if not account:
            account = "%0.6d" % random.randint(0, 999999)

        return account

    def generate_phonenumber(self):
        return "+254770%0.6d" % random.randint(0, 999999)

    def generate_text(self, ref, amount, phone_number, account_name, tdate):
        return "{ref} Confirmed. on {date} Ksh{amount} received from {account_name} {phone_number}. Account Number New Utility balance is Ksh{balance}".format(
            ref=ref,
            date=tdate.strftime("%d/%m/%y at %I:%M %p"),
            amount=amount,
            phone_number=phone_number,
            account_name=account_name.upper(),
            balance=str(decimal.Decimal(amount) * 15)
        )

    def save(self):
        amount = self.cleaned_data["amount"]
        reference_number = self.cleaned_data["reference_number"]
        paybill_account = self.cleaned_data["paybill_account"]

        phone_number = self.generate_phonenumber()
        tdate = datetime.datetime.now()

        names_len = len(NAMES)
        account_name = "%s %s" % (NAMES[random.randint(0, names_len-1)], NAMES[random.randint(0, names_len-1)])

        return {
            "id": random.randint(0, 8**8),
            "orig": "MPESA",
            "dest": self.generate_phonenumber(),
            "tstamp": str(tdate),
            "text": self.generate_text(reference_number, amount, phone_number,
                    account_name, tdate
                ),
            "mpesa_code": reference_number,
            "mpesa_msisdn": phone_number,
            "mpesa_sender": account_name,
            "mpesa_amt": amount,
            "mpesa_acc": paybill_account,

            "business_number": 99999,
            "customer_id": 2040,

            "mpesa_trx_date": datetime.datetime.now().date().strftime(TRANSACTION_DATE_FORMAT),
            "mpesa_trx_time": datetime.datetime.now().time().strftime(TRANSACTION_TIME_FORMAT),

            "user": settings.MPESA_IPN_USER,
            "pass": settings.MPESA_IPN_PASS
        }