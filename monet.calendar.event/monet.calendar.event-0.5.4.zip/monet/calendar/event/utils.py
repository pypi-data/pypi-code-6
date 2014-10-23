# -*- coding: utf-8 -*-

from DateTime import DateTime

def toDateTime(time):
    try:
        returntime = DateTime(time.year,time.month,time.day,time.hour,time.minute,time.second)
    except AttributeError:
        returntime = DateTime(time.year,time.month,time.day)
    return returntime

def dstartformat(time):
    return toDateTime(time).strftime("%Y%m%d")
