# -*- coding: utf-8 -*-

import re

from datetime import datetime as datetime_

from validate_email import validate_email

import ipaddress

import pycountry

__all__ = ['numeric', 'alphanumeric', 'accepted_payment_type', 'email_address',
           'boolean', 'decimal', 'valid_country_code', 'valid_credit_card_number',
           'valid_ip_address', 'datetime']

ALPHANUMERIC_RE = re.compile(r'^(?:[\w ](?!_))+$')
NUMERIC_RE = re.compile(r'^[0-9]+$')
DECIMAL_RE = re.compile(r'^\d+\.\d{2}$')
CREDIT_CARD_RE = re.compile(r'''^(?:4[0-9]{12}(?:[0-9]{3})?
                                   |5[1-5][0-9]{14}
                                   |6(?:011|5[0-9][0-9])[0-9]{12}
                                   |3[47][0-9]{13}
                                   |3(?:0[0-5]|[68][0-9])[0-9]{11}
                                   |(?:2131|1800|35\\d{3})\d{11})$''',
                            re.X)


def email_address(length=None):
    """
    Verifies that a given value of a specified length is a valid RFC 2822 email address
    """
    def _email_address(email_address):
        if len(email_address) == length or length is None:
            return validate_email(email_address)
        else:
            return False
    return _email_address


def accepted_payment_type(credit_card_type):
    """
    Verifies that the given payment type is supported by Lime Light
    """
    return bool(credit_card_type in {'amex', 'visa', 'master', 'discover', 'checking', 'offline',
                                     'solo', 'maestro', 'switch', 'boleto', 'paypal', 'diners',
                                     'hipercard', 'aura', 'eft_germany', 'giro'})


def valid_credit_card_number(length=None):
    """
    Verifies that the given credit card number is valid.
    """
    def _valid_credit_card_number(number, credit_card_re=CREDIT_CARD_RE):
        if len(number) == length or length is None:
            return bool(re.match(credit_card_re, number))
        else:
            return False
    return _valid_credit_card_number


def valid_ip_address(length=None):
    """
    Verifies that the given IP address is valid.
    """
    def _valid_ip_address(ip_address):
        if len(ip_address) == length or length is None:
            return isinstance(ipaddress.ip_address(ip_address), (ipaddress.IPv4Address,
                                                                 ipaddress.IPv6Address))
        else:
            return False
    return _valid_ip_address


def decimal(number, decimal_re=DECIMAL_RE):
    """
    Verifies that the given number is a valid decimal
    :param number:
    :param decimal_re:
    :return:
    """
    return bool(re.match(decimal_re, number))


def valid_country_code(country_code):
    """
    Verifies that the given two-letter country code is valid.
    :param country_code:
    :return:
    """
    try:
        return bool(pycountry.countries.get(alpha2=country_code))
    except KeyError:
        return False


def datetime(obj):
    """
    Verifies that the given object represents a date.
    :param obj:
    :return:
    """
    return isinstance(obj, datetime_)