# -*- coding: utf-8 -*-
from .mxdateindex import MxDateIndex
from .mxdaterangeindex import MxDateRangeIndex
import MxDateTimeField  # register


def initialize(context):
    """initialize product (called by zope)"""
    MxDateIndex.initialize(context)
    MxDateRangeIndex.initialize(context)
