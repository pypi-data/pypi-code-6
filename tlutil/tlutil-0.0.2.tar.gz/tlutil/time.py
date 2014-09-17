# -*- coding: utf-8 -*-
"""
    tlutil.time
"""

import time
import datetime


__all__ = [
    "ct_to_datetime", "datetime_to_stamp", "stamp_to_datetime",
    "pretty_date", "pretty_time"
]


def ct_to_datetime(s):
    return datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')


def datetime_to_stamp(d):
    return int(time.mktime(d.timetuple()))


def stamp_to_datetime(s):
    return datetime.datetime.fromtimestamp(s)


def _pretty_date(time=False):
    now = datetime.datetime.now()
    if type(time) is int:
        diff = now - stamp_to_datetime(time)
    elif isinstance(time, datetime.datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "刚刚"
        if second_diff < 60:
            return str(second_diff) + "秒前"
        if second_diff < 120:
            return "一分钟前"
        if second_diff < 3600:
            return str(second_diff / 60) + "分钟前"
        if second_diff < 7200:
            return "一小时前"
        if second_diff < 86400:
            return str(second_diff / 3600) + "小时前"
    if day_diff == 1:
        return "昨天"
    if day_diff < 7:
        return str(day_diff) + "天前"
    if day_diff < 31:
        return str(day_diff / 7) + "周前"
    if day_diff < 365:
        return str(day_diff / 30) + "月前"
    return str(day_diff / 365) + "年前"


def pretty_date(time=False):
    """格式化日期
    """
    return _pretty_date(time).decode('utf-8')


def _pretty_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    ret = ''
    if h:
        ret += '%d:' % h
    ret += '%02d:%02d' % (m, s)
    return ret


def pretty_time(seconds):
    """格式化时间
    """
    return _pretty_time(seconds).decode('utf-8')
