#!/usr/bin/env python
# -*- coding: utf-8 -*-

# django-simple-webservice
# Copyright (c) 2014, Liricus, All rights reserved.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3.0 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library.


#==============================================================================
# DOCS
#==============================================================================

"""Serializers

"""


#==============================================================================
# IMPORTS
#==============================================================================

import datetime
import decimal

from django.forms.models import model_to_dict as _model_to_dict


#==============================================================================
# CONSTANTS
#==============================================================================

TO_SIMPLE_TYPES = {
    datetime.datetime: lambda x: x.isoformat().replace("T", " "),
    datetime.time: lambda x: x.isoformat(),
    datetime.date: lambda x: x.isoformat(),
    bool: lambda x: x,
    int: lambda x: x,
    long: lambda x: x,
    float: lambda x: x,
    str: unicode,
    unicode: lambda x: x,
    decimal.Decimal: lambda x: unicode(x),
    type(None): lambda x: None,
    complex: lambda x: unicode(x)
}


DEFAULT_PARSER = lambda x: unicode(x)


#==============================================================================
# FUNCTIONS
#==============================================================================

def query_to_dict(query, *a, **kw):
    """Convert a django query ito a list of json-serialisable objects"""
    return [model_to_dict(obj) for obj in query]


def model_to_dict(obj, *a, **kw):
    """Convert a single model into json serialisable object"""
    as_dict = _model_to_dict(obj, *a, **kw)
    for k, v in as_dict.items():
        as_dict[k] = TO_SIMPLE_TYPES.get(type(v), DEFAULT_PARSER)(v)
    return as_dict


#==============================================================================
# MAIN
#==============================================================================

if __name__ == "__main__":
    print(__doc__)
