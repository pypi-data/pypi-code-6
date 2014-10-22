from django.conf import settings

MPESA_PAYBILL_NUMBER = getattr(settings, "MPESA_PAYBILL_NUMBER", None)
MPESA_IPN_USER = getattr(settings, "MPESA_IPN_USER", None)
MPESA_IPN_PASS = getattr(settings, "MPESA_IPN_PASS", None)

assert MPESA_PAYBILL_NUMBER, "MISSING SETTING: Please set MPESA_PAYBILL_NUMBER in your settings file"
assert MPESA_IPN_USER, "MISSING SETTING: Please set MPESA_IPN_USER in your settings file"
assert MPESA_IPN_PASS, "MISSING SETTING: Please set MPESA_IPN_PASS in your settings file"