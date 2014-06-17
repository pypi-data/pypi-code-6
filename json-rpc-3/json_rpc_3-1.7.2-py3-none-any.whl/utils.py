""" Utility functions for package."""
from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta, tzinfo
import json


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


class JSONSerializable(metaclass=ABCMeta):
    """ Common functionality for json serializable objects."""

    serialize = staticmethod(json.dumps)
    deserialize = staticmethod(json.loads)

    @abstractmethod
    def json(self):
        raise NotImplemented

    @classmethod
    def from_json(cls, json_str):
        data = cls.deserialize(json_str)

        if not isinstance(data, dict):
            raise ValueError("data should be dict")

        return cls(**data)


class DatetimeEncoder(json.JSONEncoder):
    """ Encoder for datetime objects.
    Usage: json.dumps(object, cls=DatetimeEncoder)
    """

    @staticmethod
    def datetime_to_dict(dt):
        dt_dct = {"__datetime__": [
            dt.year,
            dt.month,
            dt.day,
            dt.hour,
            dt.minute,
            dt.second,
            dt.microsecond
        ]}
        if dt.tzinfo is not None:
            dt_dct["__tzshift__"] = dt.utcoffset().seconds
        return dt_dct

    def encode(self, o):
        if isinstance(o, datetime):
            return super(DatetimeEncoder, self).encode(self.datetime_to_dict(o))

        return super(DatetimeEncoder, self).encode(o)


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
