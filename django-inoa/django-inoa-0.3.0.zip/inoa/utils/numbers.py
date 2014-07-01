# -*- coding: utf-8 -*-
from decimal import Decimal, ROUND_HALF_UP
from locale import format_string


def to_precision(dec, places=None, min_places=None, max_places=None, rounding=None):
    """
    Returns the given Decimal object quantized to a number of decimal places within the given range.
    If the given value has less places than min_places, it will be zero-padded.
    If the given value has more places than max_places, it will be rounded.
    """
    dec = Decimal(dec)
    if places is None:
        if min_places is None and max_places is None:
            return dec
        places = max(-dec.normalize().as_tuple().exponent, 0)
        if max_places is not None:
            places = min(places, max_places)
        if min_places is not None:
            places = max(places, min_places)
    return dec.quantize(Decimal('%%.%df' % places % 0),
                        ROUND_HALF_UP if rounding is None else rounding)


def format_number(value, places=None, min_places=None, max_places=None, rounding=None,
                  multiplier=None, default=None, prefix=None, postfix=None, grouping=None):
    """
    Returns a number formatted to a string.
    eg.:
        value: '10000.3380'
        returns: 10.000,338
    """
    if value is None:
        return default
    if grouping is None:
        grouping = True
    value = Decimal(value) * (multiplier or 1)
    value = to_precision(value, places=places, min_places=min_places, max_places=max_places, rounding=rounding)
    places = max(-value.as_tuple().exponent, 0)
    return format_string((u"%%s%%.%df%%s" % places), (prefix or u"", value, postfix or u""), grouping=grouping)
