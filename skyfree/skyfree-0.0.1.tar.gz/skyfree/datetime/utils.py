#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4 et
#
# Copyright @ 2014 OPS, Qunar Inc. (qunar.com)
#
# Author: tingfang.bao <tingfang.bao@qunar.com>
# DateTime: 14-7-23 下午2:34
"""
时间辅助类
"""

import calendar
import datetime
import time

import iso8601
import six


# ISO 8601 包括次秒
_ISO8601_TIME_FORMAT_SUBSECOND = '%Y-%m-%dT%H:%M:%S.%f'

# 标准的ISO 8601格式
_ISO8601_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S'

# 优先使用含有次秒的格式
PERFECT_TIME_FORMAT = _ISO8601_TIME_FORMAT_SUBSECOND


def isotime(at=None, subsecond=False):
    """
    返回ISO 8601格式的日期
    :param at: datetime实例，默认为None，自动调用utcnow() 2014-07-23T06:36:40Z
    :param subsecond: 是否显示次秒 2014-07-23T06:39:49.745012Z
    :return: 返回ISO 8601格式日期
    """
    if not at:
        at = utcnow()
    st = at.strftime(_ISO8601_TIME_FORMAT
                     if not subsecond
                     else _ISO8601_TIME_FORMAT_SUBSECOND)
    tz = at.tzinfo.tzname(None) if at.tzinfo else 'UTC'
    st += ('Z' if tz == 'UTC' else tz)
    return st


def parse_isotime(timestr):
    """
    返回ISO 8601 日期时间对象
    :param timestr: 事件字符串
    :return: 返回datetime.datetime对象
    :raise ValueError: 转换失败
    """
    try:
        return iso8601.parse_date(timestr)
    except iso8601.ParseError as e:
        raise ValueError(six.text_type(e))
    except TypeError as e:
        raise ValueError(six.text_type(e))


def strtime(at=None, fmt=PERFECT_TIME_FORMAT):
    """
    根据指定的日期格式，进行格式化操作
    :param at: 日期时间对象
    :param fmt: 格式化字符串
    :return:  返回格式化后的字符串
    """
    if not at:
        at = utcnow()
    return at.strftime(fmt)


def parse_strtime(timestr, fmt=PERFECT_TIME_FORMAT):
    """
    将一个字符串日期转化为fmt格式的日期时间对象
    注意：timestr的格式必须要符合fmt的格式要求
    :param timestr: 代表日期的字符串
    :param fmt: 时间日期格式
    :return: datetime.datetime对象
    """
    return datetime.datetime.strptime(timestr, fmt)


def normalize_time(timestamp):
    """
    标准化任意时区的信息到UTC naive对象
    :param timestamp: datetime对象
    """
    offset = timestamp.utcoffset()
    if offset is None:
        return timestamp
    return timestamp.replace(tzinfo=None) - offset


def is_older_than(before, seconds):
    """
    测试当前时间是否是在before时间点，之后seconds秒
    注意，两个datetime相减，获得到一个datetime.timedelta对象
    :param before: 之前的某一个测试时间点
    :param seconds: 时间间隔
    :return: 是否超过
    """
    if isinstance(before, six.string_types):
        before = parse_strtime(before).replace(tzinfo=None)
    else:
        before = before.replace(tzinfo=None)

    return utcnow() - before > datetime.timedelta(seconds=seconds)


def is_newer_than(after, seconds):
    """
    测试之后的某个时间是否是在当前时间点，之前seconds秒
    注意，两个datetime相减，获得到一个datetime.timedelta对象
    :param after: 当前时间之后的某个时间点
    :param seconds: 时间间隔
    :return: 是否超过
    """
    if isinstance(after, six.string_types):
        after = parse_strtime(after).replace(tzinfo=None)
    else:
        after = after.replace(tzinfo=None)

    return after - utcnow() > datetime.timedelta(seconds=seconds)


def utcnow_ts():
    """
    返回当前事件的整数值
    :return:
    """
    if utcnow.override_time is None:
        # NOTE(kgriffs): This is several times faster
        # than going through calendar.timegm(...)
        # 与下面的calendar.timegm(utcnow().timetuple())返回结果一致
        return int(time.time())

    return calendar.timegm(utcnow().timetuple())


def utcnow():
    """
    返回当前日期时间的utc表示

    :return:
    """
    if utcnow.override_time:
        try:
            return utcnow.override_time.pop(0)
        except AttributeError:
            return utcnow.override_time
    return datetime.datetime.utcnow()


def iso8601_from_timestamp(timestamp):
    """
    时间戳转化为ISO8601格式的日期时间字符串
    :param timestamp:
    :return: 时间戳转化为ISO8601格式的日期时间字符串
    """
    return isotime(datetime.datetime.utcfromtimestamp(timestamp))


utcnow.override_time = None


def set_time_override(override_time=None):
    """Overrides utils.utcnow.

    Make it return a constant time or a list thereof, one at a time.

    :param override_time: datetime instance or list thereof. If not
                          given, defaults to the current UTC time.
    """
    utcnow.override_time = override_time or datetime.datetime.utcnow()


def advance_time_delta(timedelta):
    """
    计算某个时间点之后的事件，注意需要先调用set_time_override设置好时间
    :param timedelta:
    """
    assert (utcnow.override_time is not None)
    try:
        ret = []
        for dt in utcnow.override_time:
            dt += timedelta
            ret.append(dt)
        utcnow.override_time = ret
    except TypeError:
        utcnow.override_time += timedelta


def advance_time_seconds(seconds):
    """Advance overridden time by seconds."""
    advance_time_delta(datetime.timedelta(0, seconds))


def clear_time_override():
    """Remove the overridden time."""
    utcnow.override_time = None


def marshall_now(now=None):
    """
    可以方便获取年份，月份，小时，分钟，秒等信息
    """
    if not now:
        now = utcnow()
    return dict(day=now.day, month=now.month, year=now.year, hour=now.hour,
                minute=now.minute, second=now.second,
                microsecond=now.microsecond)


def unmarshall_time(tyme):
    """Unmarshall a datetime dict."""
    return datetime.datetime(day=tyme['day'],
                             month=tyme['month'],
                             year=tyme['year'],
                             hour=tyme['hour'],
                             minute=tyme['minute'],
                             second=tyme['second'],
                             microsecond=tyme['microsecond'])


def delta_seconds(before, after):
    """Return the difference between two timing objects.

    Compute the difference in seconds between two date, time, or
    datetime objects (as a float, to microsecond resolution).
    """
    delta = after - before
    return total_seconds(delta)


def total_seconds(delta):
    """Return the total seconds of datetime.timedelta object.

    Compute total seconds of datetime.timedelta, datetime.timedelta
    doesn't have method total_seconds in Python2.6, calculate it manually.
    """
    try:
        return delta.total_seconds()
    except AttributeError:
        return ((delta.days * 24 * 3600) + delta.seconds +
                float(delta.microseconds) / (10 ** 6))


def is_soon(dt, window):
    """Determines if time is going to happen in the next window seconds.

    :params dt: the time
    :params window: minimum seconds to remain to consider the time not soon

    :return: True if expiration is within the given duration
    """
    soon = (utcnow() + datetime.timedelta(seconds=window))
    return normalize_time(dt) <= soon


if __name__ == '__main__':
    print isotime(subsecond=False)
    print parse_isotime("2014-07-08 12:30:00")
    print strtime(fmt="%Y")
    print utcnow_ts()
    print utcnow()
    print iso8601_from_timestamp(utcnow_ts())

    print 'testing advance_time_second just a value'
    print type(utcnow())
    set_time_override(utcnow())
    print utcnow()
    advance_time_seconds(30)
    print utcnow()

    print 'testing advance_time_seconds'
    set_time_override([utcnow(), utcnow()])
    print utcnow.override_time
    advance_time_seconds(30)
    print utcnow.override_time

    clear_time_override()
    print marshall_now()

    print datetime.datetime.now()
