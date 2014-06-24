""" Utility functions for package."""
from datetime import datetime, timedelta, tzinfo


class FixedOffset(tzinfo):
    """Fixed offset in minutes east from UTC."""

    def __init__(self, offset):
        self.__offset = timedelta(seconds=offset)

    def utcoffset(self, dt):
        return self.__offset

    def tzname(self, dt):
        return 'TZ offset: {secs} hours'.format(secs=self.__offset)

    def dst(self, dt):
        return timedelta(0)


def json_datetime_default(d):
    """ Encoder for datetime objects.
    Usage: json.dumps(object, cls=DatetimeEncoder)
    """
    if isinstance(d, datetime):
        dt_dct = {"__datetime__": [d.year, d.month, d.day, d.hour, d.minute, d.second, d.microsecond]}
        if d.tzinfo is not None:
            dt_dct["__tzshift__"] = d.utcoffset().seconds
        return dt_dct
    raise TypeError


def json_datetime_hook(dictionary):
    """
    JSON object_hook function for decoding datetime objects.
    Used in pair with
    :return: Datetime object
    :rtype: datetime
    """
    if "__datetime__" not in dictionary:
        return dictionary

    dt = datetime(*dictionary["__datetime__"])

    if "__tzshift__" in dictionary:
        dt = dt.replace(tzinfo=FixedOffset(dictionary["__tzshift__"]))

    return dt
