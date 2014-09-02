#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY in return.


# =============================================================================
# DOCS
# =============================================================================

"""Contains functions to convert various support types of Yatel to more easily
serializable types.

"""

# =============================================================================
# IMPORTS
# =============================================================================

import decimal
import datetime
import types

import numpy as np

from yatel import dom

# =============================================================================
# CONSTANTS
# =============================================================================

#: Constant to retrieve  value as is.
LITERAL_TYPE = "literal"

CONTAINER_TYPES = (tuple, set, list, frozenset, types.GeneratorType)

#: Dictionary of yatel domain object model.
HASHED_TYPES = tuple([dict] + dom.YatelDOM.__subclasses__())

#: This dictionary maps types to it's most simple representation.
TO_SIMPLE_TYPES = {
    datetime.datetime: lambda x: x.isoformat(),
    datetime.time: lambda x: x.isoformat(),
    datetime.date: lambda x: x.isoformat(),
    bool: lambda x: x,
    int: lambda x: x,
    long: lambda x: x,
    float: lambda x: x,
    str: unicode,
    unicode: lambda x: x,
    decimal.Decimal: lambda x: unicode(x),
    types.NoneType: lambda x: None,
    complex: lambda x: unicode(x)
}

#: This dictionary maps types to python types.
TO_PYTHON_TYPES = {
    datetime.datetime:
        lambda x: datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%f"),
    datetime.time:
        lambda x: datetime.datetime.strptime(x, "%H:%M:%S.%f").time(),
    datetime.date:
        lambda x: datetime.datetime.strptime(x, "%Y-%m-%d").date(),
    bool:
        lambda x: x.lower() == "true" if isinstance(x, basestring) else bool(x),
    long: long,
    int: int,
    float: float,
    str: unicode,
    unicode: unicode,
    decimal.Decimal: decimal.Decimal,
    type(None): lambda x: None,
    complex: complex
}

#: This dictionary maps data types to their name.
TYPES_TO_NAMES = dict(
    (k, k.__name__)
    for k in TO_SIMPLE_TYPES.keys() +
    list(CONTAINER_TYPES) +
    list(HASHED_TYPES) + [type]
)
TYPES_TO_NAMES[str] = unicode.__name__

#: This dictionary maps names to data type.
NAMES_TO_TYPES = dict((v, k) for k, v in TYPES_TO_NAMES.items())


# =============================================================================
# FUNCTIONS
# =============================================================================

def np2py(obj):
    """Converts a numpy number to it´s closest respresentation of Python
    traditional objects.

    """
    # http://stackoverflow.com/questions/9452775/converting-numpy-dtypes-to-native-python-types
    if isinstance(obj, np.ndarray):
        return [np2py(e) for e in obj]
    elif isinstance(obj, np.number):
        obj = np.asscalar(obj)
        if type(obj) in TO_SIMPLE_TYPES:
            return obj
        elif isinstance(obj, np.longdouble):
            return float(obj)
        elif "float" in pytype.__name__:
            return float(obj)
        elif "complex" in pytype.__name__:
            return complex(obj)
    elif isinstance(obj, np.bool_):
        return bool(obj)
    return str(obj)


def simplifier(obj):
    """Translates obj given to a Python dictionary.

    Returns
    -------
    dictionary: dict
        a dictionary representation of obj.

    """

    # numpy simplifier
    if isinstance(obj, (np.generic, np.ndarray)):
        obj = np2py(obj)

    typename = TYPES_TO_NAMES[type(obj)]
    value = ""
    if isinstance(obj, CONTAINER_TYPES):
        value = map(simplifier, obj)
    elif isinstance(obj, HASHED_TYPES):
        value = dict((k, simplifier(v)) for k, v in obj.items())
    elif type(obj) == type:
        value = TYPES_TO_NAMES[obj]
    else:
        value = TO_SIMPLE_TYPES[type(obj)](obj)
    return {"type": typename, "value": value}


def parse(obj):
    """Parses an objects type and value, according to the dictionary maps.

    """

    typename = obj["type"]
    value = obj["value"]
    if typename == LITERAL_TYPE:
        return value
    otype = NAMES_TO_TYPES[typename]
    if otype in CONTAINER_TYPES:
        value = map(parse, value)
    elif otype in HASHED_TYPES:
        data = dict((k, parse(v)) for k, v in value.items())
        value = otype(**data)
    elif otype == type:
        value = NAMES_TO_TYPES[value]
    else:
        value = TO_PYTHON_TYPES[otype](value)
    return value

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print(__doc__)
