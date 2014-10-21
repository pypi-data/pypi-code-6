#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4 et
#
# Copyright @ 2014 OPS, Qunar Inc. (qunar.com)
#
# Author: tingfang.bao <tingfang.bao@qunar.com>
# DateTime: 14-7-22 下午5:37


def valid_string(s, min_len=None, max_len=None,
                 allow_blank=False, auto_trim=True):
    """
    @param s str/unicode 要校验的字符串
    @param min_value None/int
    @param max_value None/int
    @param allow_blank boolean
    @param allow_trim boolean
    @return boolean is_ok
    @return string/int value 若是ok，返回int值，否则返回错误信息
    """
    if s is None:
        return False, "cannot is None"
    if not isinstance(s, basestring):
        return False, "must a string value"
    if auto_trim:
        s = s.strip()
    str_len = len(s)
    if not allow_blank and str_len < 1:
        return False, "not allow blank"
    if max_len is not None and str_len > max_len:
        return False, "length must less than %d" % max_len
    if min_len is not None and str_len < min_len:
        return False, "length must greater than %d" % min_len

    return True, s


def valid_int(s, min_value=None, max_value=None):
    """
    @param s str/unicode 要校验的字符串
    @param min_value None/int
    @param max_value None/int
    @return boolean is_ok
    @return string/int value 若是ok，返回int值，否则返回错误信息
    """
    if s is None:
        return False, "cannot is None"
    if not isinstance(s, basestring):
        return False, "must a string value"

    s = int(s)
    if max_value is not None and s > max_value:
        return False, "%d must less than %d" % (s, max_value)

    if min_value is not None and s < min_value:
        return False, "%d must greater than %d" % (s, min_value)
    return True, s