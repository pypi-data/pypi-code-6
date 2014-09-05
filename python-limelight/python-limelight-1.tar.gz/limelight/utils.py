# -*- coding: utf-8 -*-

import re
import six

__all__ = ['not_implemented', 'to_python', 'to_camel_case', 'to_underscore']


CAMEL_RE = re.compile(r'([A-Z])')
UNDER_RE = re.compile(r'_([a-z])')
NUM_RE = re.compile(r'^[0-9]+$')
FLOAT_RE = re.compile(r'^[0-9]*?\.[0-9]+$')


def capitalize(name):
    return name[0].upper() + name[1:]


# noinspection PyUnusedLocal
@property
def not_implemented(self):
    raise NotImplementedError


def to_underscore(name, initial_cap=False):
    """Convert identifiers from camelCase to underscore_style"""
    underscore_name = CAMEL_RE.sub(lambda s: "_" + s.group(1).lower(), name)
    if initial_cap:
        underscore_name = capitalize(underscore_name)
    return underscore_name


def to_camel_case(name, initial_cap=False):
    """Convert identifiers from underscore_style to camelCase"""
    camel_case_name = UNDER_RE.sub(lambda s: s.group(1).upper(), name)
    if initial_cap:
        camel_case_name = capitalize(camel_case_name)
    return camel_case_name


def to_python(var):
    """
    Converts strings that are really numbers to ints or floats

    May be more generic in the future
    :param var:
    """
    var = var[0] if isinstance(var, list) and len(var) == 1 else var
    if not isinstance(var, six.string_types):
        return var
    elif NUM_RE.match(var):
        if int(var) == 1:
            return True
        elif int(var) == 0:
            return False
        else:
            return int(var)
    elif FLOAT_RE.match(var):
        return float(var)  # Maybe this should be decimal.Decimal?
    else:
        return var

