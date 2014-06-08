#!/usr/bin/env python
# -*- coding: utf-8 -*-

import calendar
from datetime import datetime
from datetime import timedelta
import random
import time

"""
Epoch represented as a struct_time (Thursday, January 1, 1970)
"""
EPOCH_AS_STRUCT_TIME = time.gmtime(0)

"""
Epoch represented as a datetime (Thursday, January 1, 1970)
"""
EPOCH_AS_DATETIME = datetime(*EPOCH_AS_STRUCT_TIME[:6])


def is_leap_year(year):
    """
    Returns true if the year is a leap year, false otherwise

    >>> is_leap_year(2008)
    True
    >>> is_leap_year(2012)
    True
    >>> is_leap_year(2013)
    False
    """
    return calendar.isleap(year)


def is_weekday(date):
    """
    Returns true if date is a weekday, false otherwise

    >>> date = datetime.now()
    >>> last_friday = date - timedelta(days=date.weekday()) \
    + timedelta(days=4, weeks=-1)
    >>> is_weekday(last_friday)
    True
    """
    return date.isoweekday() < 6


def is_weekend(date):
    """
    Returns true if date is a weekend, false otherwise

    >>> date = datetime.now()
    >>> last_friday = date - timedelta(days=date.weekday()) \
    + timedelta(days=4, weeks=-1)
    >>> is_weekend(last_friday)
    False
    """
    return date.isoweekday() > 5


def next_day(date, day):
    """
    Returns the next day (as a datetime) with respect to date.  Day parameter
    is in isoweekday format (Monday 1, Sunday 7).
    """
    days_ahead = day - date.isoweekday()
    if 0 > days_ahead:
        days_ahead += 7
    return date + timedelta(days=days_ahead)


def random_datetime(start_timestamp, end_timestamp, tz=None):
    """
    Returns a random datetime between two timestamps and converts to the tz if
    provided
    """
    assert end_timestamp > start_timestamp
    interval = end_timestamp - start_timestamp
    random_timestamp = start_timestamp + (random.random() * interval)
    return datetime.fromtimestamp(random_timestamp, tz)

# vim: filetype=python
