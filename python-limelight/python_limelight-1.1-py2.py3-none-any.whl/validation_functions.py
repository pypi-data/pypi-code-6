# -*- coding: utf-8 -*-
"""
A collection of Lime Light-specific validation functions.
"""

import re

from datetime import datetime

from six import u

from voluptuous import Invalid

from validate_email_address import validate_email

import ipaddress as ipaddr

import pycountry

__all__ = ['email_address', 'accepted_payment_type', 'credit_card_number', 'ip_address', 'decimal',
           'country_code', 'expiration_date', ]

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


def email_address(email):
    """
    Verifies that the given value is a valid email address

    :param email: An email address
    :type email: str
    :return: The given value
    :rtype: str
    :raises: voluptuous.Invalid
    """
    if validate_email(email):
        return email
    else:
        raise Invalid("Invalid email address")


def accepted_payment_type(credit_card_type):
    """
    Verifies that the given payment type is supported by Lime Light

    :param credit_card_type: The type of credit card
    :type credit_card_type: str
    :return: The given values
    :rtype: str
    :raises: voluptuous.Invalid
    """
    if credit_card_type.lower() in {'amex', 'visa', 'master', 'discover', 'checking', 'offline',
                                    'solo', 'maestro', 'switch', 'boleto', 'paypal', 'diners',
                                    'hipercard', 'aura', 'eft_germany', 'giro'}:
        return credit_card_type.lower()
    else:
        raise Invalid("Invalid payment type")


def credit_card_number(number, credit_card_re=CREDIT_CARD_RE):
    """
    Verifies that the given credit card number is valid.

    :param number: A credit card number
    :type number: str
    :param credit_card_re: CONSTANT
    :type credit_card_re: _sre.SRE_Pattern
    :raises: voluptuous.Invalid
    """
    if re.match(credit_card_re, str(number)):
        return number
    else:
        raise Invalid('Invalid credit card number')


def ip_address(ip):
    """
    Verifies that the given IP address is valid.

    :param ip: An IP address
    :type ip: str
    :return: The given value
    :rtype: str
    :raises: voluptuous.Invalid
    """
    if isinstance(ipaddr.ip_address(u(ip)), (ipaddr.IPv4Address,
                                             ipaddr.IPv6Address)):
        return ip
    else:
        raise Invalid('Invalid IP address')


def decimal(number, decimal_re=DECIMAL_RE):
    """
    Verifies that the given number is a valid decimal

    :param number: A number to check
    :type number: str or decimal.Decimal
    :param decimal_re: CONSTANT
    :type decimal_re: _sre.SRE_Pattern
    :return: The given value
    :rtype: str
    :raises: voluptuous.Invalid
    """
    if re.match(decimal_re, str(number)):
        return str(number)
    else:
        raise Invalid("Not a decimal number")


def country_code(code):
    """
    Verifies that the given two-letter country code is valid.

    :param code: A two-letter country code
    :type code: str
    :return: The passed value
    :rtype: str
    :raises: voluptuous.Invalid
    """
    try:
        pycountry.countries.get(alpha2=code)
    except KeyError:
        raise Invalid('Invalid country code')
    else:
        return code


def expiration_date(date):
    """
    Verifies that the given object represents a date and that the date has not passed

    :param date: A datetime object representing an expiration date
    :type date: datetime.datetime
    :return: Correctly formatted expiration date
    :rtype: str
    :raises: voluptuous.Invalid
    """
    if isinstance(date, datetime) and datetime.today() < date:
        return date.strftime("%m%y")
    else:
        raise Invalid('Invalid expiration date')


def bool_to_one_or_zero(value):
    """
    Converts a boolean value into an integer

    :param value: A boolean value
    :type value: bool
    :return: 1 or 0
    :rtype: int
    """
    return 1 if value else 0


def bool_to_yes_or_no(value):
    """
    Converts a boolean value into a string saying "YES" or "NO"

    :param value: A boolean value
    :type value: bool
    :return: "YES" or "NO"
    :rtype: str
    """
    return "YES" if value else "NO"