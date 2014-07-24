# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
TrustPay helpers.
"""

import sys
import hmac
import hashlib
import collections

try:
    unicode
    from urllib import urlencode
except NameError:
    unicode = lambda s: s
    from urllib.parse import urlencode

#: Default test api url.
TEST_API_URL = "https://test.trustpay.eu/mapi/paymentservice.aspx"

#: TrustPay service url.
API_URL = "https://ib.trustpay.eu/mapi/paymentservice.aspx"

#: TrustCard service url.
TRUSTCARD_API_URL = "https://ib.trustpay.eu/mapi/cardpayments.aspx"

__currencies = (
    "CZK", "EUR", "GBP", "HUF", "PLN",
    "USD", "RON", "BGN", "HRK", "LTL", "TRY",
)

#: Supported currencies.
CURRENCIES = collections.namedtuple(
    "TrustPayCurrencies",
    __currencies,
)(*__currencies)

__languages = (
    "bg", "bs", "cs", "de", "en", "es",
    "et", "hr", "hu", "it", "lt", "lv",
    "pl", "ro", "ru", "sk", "sl", "sr",
    "uk",
)

#: Suported languages.
LANGUAGES = collections.namedtuple(
    "TrustPayLanguages",
    __languages,
)(*__languages)

__countries = (
    "CZ", "HU", "PL", "SK", "EE", "BG",
    "RO", "HR", "LV", "LT", "SI", "TR",
    "FI",
)

__countries_verbose = (
    "Czech Republic", "Hungary", "Poland",
    "Slovak Republic", "Estonia", "Bulgaria",
    "Romania", "Croatia", "Latvia", "Lithuania",
    "Slovenia", "Turkey", "Finland",
)

#: Supported countries
COUNTRIES = collections.namedtuple(
    "TrustPayCountries",
    __countries,
)(*__countries)

#: Supported countries verbose version.
COUNTRIES_VERBOSE = collections.namedtuple(
    "TrustPayCountriesVerbose",
    __countries,
)(*__countries_verbose)


__ResultCodes = collections.namedtuple(
    "TrustPayResultCodes",
    [
        "SUCCESS", "PENDING", "ANNOUNCED", "AUTHORIZED",
        "PROCESSING", "AUTHORIZED_ONLY", "INVALID_REQUEST",
        "UNKNOWN_ACCOUNT", "MERCHANT_ACCOUNT_DISABLED",
        "INVALID_SIGN", "USER_CANCEL", "INVALID_AUTHENTICATION",
        "DISPOSABLE_BALANCE", "SERVICE_NOT_ALLOWED", "PAYSAFECARD_TIMEOUT",
        "GENERAL_ERROR", "UNSUPPORTED_CURRENCY_CONVERSION",
    ]
)

#: Result codes of redirects and notifications.
RESULT_CODES = __ResultCodes(
    "0", "1", "2", "3", "4", "5", "1001", "1002", "1003", "1004",
    "1005", "1006", "1007", "1008", "1009", "1100", "1101",
)

__rc_desc = collections.namedtuple(
    "TrustPayResultCodesDesc",
    ["short", "long"],
)

#: Result codes of redirects and notifications.
#: In verbose form with short and long description of result code.
RESLUT_CODES_DESC = {
    RESULT_CODES.SUCCESS: __rc_desc(
        "Success",
        "Payment was successfully processed.",
    ),
    RESULT_CODES.PENDING: __rc_desc(
        "Pending",
        "Payment is pending (offline payment)",
    ),
    RESULT_CODES.ANNOUNCED: __rc_desc(
        "Announced",
        (
            "TrustPay has been notified that the client"
            "placed a payment order or has made payment,"
            " but further confirmation from 3rd party is needed."
        ),
    ),
    RESULT_CODES.AUTHORIZED: __rc_desc(
        "Authorized",
        (
            "Payment was successfully authorized. Another"
            " notification (with result code 0 - success)"
            " will be sent when TrustPay receives and processes"
            " payment from 3rd party."
        ),
    ),
    RESULT_CODES.PROCESSING: __rc_desc(
        "Processing",
        (
            "TrustPay has received the payment, but it"
            " must be internally processed before it is"
            " settled on the merchant‘s account."
        ),
    ),
    RESULT_CODES.AUTHORIZED_ONLY: __rc_desc(
        "Authorized only",
        (
            "Card payment was successfully authorized,"
            " but not captured. Subsequent MAPI call(s)"
            " is (are) required to capture payment."
        ),
    ),
    RESULT_CODES.INVALID_REQUEST: __rc_desc(
        "Invalid request",
        "Data sent is not properly formatted.",
    ),
    RESULT_CODES.UNKNOWN_ACCOUNT: __rc_desc(
        "Unknown account",
        "Account with specified ID was not found.",
    ),
    RESULT_CODES.MERCHANT_ACCOUNT_DISABLED: __rc_desc(
        "Merchant's account disabled",
        "Merchant's account has been disabled.",
    ),
    RESULT_CODES.INVALID_SIGN: __rc_desc(
        "Invalid sign",
        "The message is not signed correctly.",
    ),
    RESULT_CODES.USER_CANCEL: __rc_desc(
        "User cancel",
        "Customer has cancelled the payment.",
    ),
    RESULT_CODES.INVALID_AUTHENTICATION: __rc_desc(
        "Invalid authentication",
        "Request was not properly authenticated",
    ),
    RESULT_CODES.DISPOSABLE_BALANCE: __rc_desc(
        "Disposable balance",
        "Requested transaction amount is greater than disposable balance.",
    ),
    RESULT_CODES.SERVICE_NOT_ALLOWED: __rc_desc(
        "Service not allowed",
        (
            "Service cannot be used or permission to"
            " use given service has not been granted."
        ),
    ),
    RESULT_CODES.PAYSAFECARD_TIMEOUT: __rc_desc(
        "PaySafeCard timeout",
        "Cards allocation will be cancelled.",
    ),
    RESULT_CODES.GENERAL_ERROR: __rc_desc(
        "General Error",
        "Internal error has occurred.",
    ),
    RESULT_CODES.UNSUPPORTED_CURRENCY_CONVERSION: __rc_desc(
        "Unsupported currency conversion",
        "Currency conversion for requested currencies is not supported.",
    ),
}


#: TrustPay environment class
#: Just attributes holder for TrustPay's variables.
TrustPayEnvironment = collections.namedtuple(
    "TrustPayEnvironment",
    [
        "api_url",
        "redirect_url",
        "success_url",
        "error_url",
        "cancel_url",
        "notification_url",
        "aid",
        "secret_key",
        "currency",
        "language",
        "country",
    ],
)


TrustPayRequest = collections.namedtuple(
    "TrustPayRequest",
    [
        "AID", "AMT", "CUR", "REF", "URL", "RURL",
        "CURL", "EURL", "NURL", "SIG", "LNG",
        "CNT", "DSC", "EMA",
    ],
)


TrustPayNotification = collections.namedtuple(
    "TrustPayNotification",
    [
        "AID", "TYP", "AMT", "CUR", "REF",
        "RES", "TID", "OID", "TSS", "SIG",
    ],
)

TrustPayRedirect = collections.namedtuple(
    "TrustPayRedirect",
    ["REF", "RES", "PID"],
)


def _build_nt_cls(
    cls,
    kw,
    fnc=lambda v: v if v is None else unicode(v),
):
    _kw = kw.copy()
    inst = cls(*[fnc(_kw.pop(attr, None)) for attr in cls._fields])
    if _kw:
        raise ValueError("Got unexpected field names: %r" % _kw.keys())
    return inst


def build_redirect(**kw):
    return _build_nt_cls(TrustPayRedirect, kw)


def build_notification(**kw):
    return _build_nt_cls(TrustPayNotification, kw)


def build_pay_request(**kw):
    return _build_nt_cls(TrustPayRequest, kw)


def build_test_environment(**kw):
    kw["api_url"] = kw.get("api_url", TEST_API_URL)
    return _build_nt_cls(TrustPayEnvironment, kw, fnc=lambda v: v)


def build_environment(**kw):
    kw["api_url"] = kw.get("api_url", API_URL)
    return _build_nt_cls(TrustPayEnvironment, kw, fnc=lambda v: v)


def sign_message(key, msg):
    if sys.version_info[0] == 3:
        msg, key = str.encode(msg), str.encode(key)
    return hmac.new(key, msg, hashlib.sha256).hexdigest().upper()


def extract_attrs(obj, attrs):
    return [getattr(obj, attr) for attr in attrs]


def merge_env_with_request(
    env,
    request,
    fnc=lambda v1, v2: v1 if v2 is None else v2,
):
    kw = {}
    kw['AID'] = fnc(env.aid, request.AID)
    kw['URL'] = fnc(env.redirect_url, request.URL)
    kw['RURL'] = fnc(env.success_url, request.RURL)
    kw['CURL'] = fnc(env.cancel_url, request.CURL)
    kw['EURL'] = fnc(env.error_url, request.EURL)
    kw['NURL'] = fnc(env.notification_url, request.NURL)
    kw['CUR'] = fnc(env.currency, request.CUR)
    kw['LNG'] = fnc(env.language, request.LNG)
    kw['CNT'] = fnc(env.country, request.CNT)
    return request._replace(**kw)


def _build_link(url, query_dict, fmt="{url}?{params}"):
    return fmt.format(url=url, params=urlencode(query_dict))


def _filter_dict_nones(d):
    res = {}
    for key, value in d.items():
        if value is not None:
            res[key] = value
    return res


def _initial_data(pay_request):
    return _filter_dict_nones(pay_request._asdict())


def build_link_for_request(url, request):
    return _build_link(url, _initial_data(request))


class TrustPay(object):

    SIGNATURE_ATTRS = ("AID", "AMT", "CUR", "REF")

    NOTIFICATION_SIGNATURE_ATTRS = (
        "AID", "TYP", "AMT", "CUR", "REF",
        "RES", "TID", "OID", "TSS"
    )

    REQUEST_REQUIRED_ATTRS = ("AID", "CUR")

    SIGNED_REQUEST_REQUIRED_ATTRS = REQUEST_REQUIRED_ATTRS + (
        "AMT", "REF", "SIG")

    CURRENCIES = CURRENCIES
    LANGUAGES = LANGUAGES
    COUNTRIES = COUNTRIES
    RESULT_CODES = RESULT_CODES
    RESLUT_CODES_DESC = RESLUT_CODES_DESC

    def __init__(self, environment):
        self.environment = environment

    def sign_request(self, pay_request):
        return pay_request._replace(
            SIG=self.pay_request_signature(pay_request))

    def pay_request_signature(self, pay_request):
        return sign_message(
            self.environment.secret_key,
            self.create_signature_msg(pay_request),
        )

    def merge_env_with_request(self, pay_request):
        return merge_env_with_request(
            self.environment,
            pay_request,
        )

    def finalize_request(
        self,
        pay_request,
        sign=True,
        validate=True,
        merge_env=True
    ):
        pr = pay_request
        if merge_env:
            pr = self.merge_env_with_request(pay_request)
        if sign:
            pr = self.sign_request(pr)
        if validate:
            pr = self.validate_request(pr)
        return pr

    def build_link(
        self,
        pay_request,
        sign=True,
        validate=True,
        merge_env=True
    ):
        return _build_link(
            self.environment.api_url,
            self.initial_data(
                self.finalize_request(
                    pay_request,
                    sign=sign,
                    validate=validate,
                    merge_env=merge_env,
                )
            ),
        )

    def check_notification_signature(self, notification):
        msg = unicode("").join(
            [self.environment.aid, ] +
            extract_attrs(notification, self.NOTIFICATION_SIGNATURE_ATTRS[1:])
        )
        return sign_message(
            self.environment.secret_key, msg) == notification.SIG

    @classmethod
    def create_signature_msg(cls, pay_request):
        return unicode("").join(
            [
                attr for attr in cls.extract_signature_attrs(pay_request)
                if attr is not None
            ]
        )

    @classmethod
    def get_result_desc(cls, rc):
        return cls.RESLUT_CODES_DESC[str(rc)]

    @classmethod
    def get_result_desc_from_notification(cls, notif):
        return cls.get_result_desc(notif.RES)

    @classmethod
    def get_result_desc_from_redirect(cls, redirect):
        return cls.get_result_desc(redirect.RES)

    @classmethod
    def validate_currency(cls, pay_request):
        if (
            pay_request.CUR is not None
            and pay_request.CUR not in cls.CURRENCIES
        ):
            raise ValueError(
                "Currency [%r] not in supported currencies [%r]" % (
                    pay_request.CUR, cls.CURRENCIES,
                )
            )

    @classmethod
    def validate_language(cls, pay_request):
        if (
            pay_request.LNG is not None
            and pay_request.LNG not in cls.LANGUAGES
        ):
            raise ValueError(
                "Language [%r] not int supported languages [%r]" % (
                    pay_request.LNG, cls.LANGUAGES,
                )
            )

    @classmethod
    def validate_country(cls, pay_request):
        if (
            pay_request.CNT is not None
            and pay_request.CNT not in cls.COUNTRIES
        ):
            raise ValueError(
                "Country [%r] not int supported countries [%r]" % (
                    pay_request.CNT, cls.COUNTRIES,
                )
            )

    @classmethod
    def validate_request(cls, pay_request):
        missing = []
        required_attrs = (
            cls.REQUEST_REQUIRED_ATTRS
            if pay_request.SIG is None else
            cls.SIGNED_REQUEST_REQUIRED_ATTRS
        )
        for attr in required_attrs:
            if attr not in cls.initial_data(pay_request):
                missing.append(attr)
        if pay_request.AMT is not None and '.' in pay_request.AMT:
            if len(pay_request.AMT.split('.')[1]) > 2:
                raise ValueError(
                    "Amount can have at max"
                    " 2 decimal places. [%s]" % pay_request.AMT)
        if missing:
            raise ValueError("Required attributes missing: %r" % missing)
        cls.validate_currency(pay_request)
        cls.validate_language(pay_request)
        cls.validate_country(pay_request)
        return pay_request

    @classmethod
    def extract_signature_attrs(cls, pay_request):
        return extract_attrs(pay_request, cls.SIGNATURE_ATTRS)

    @staticmethod
    def initial_data(pay_request):
        return _initial_data(pay_request)
