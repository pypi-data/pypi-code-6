#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4 et
#
# Copyright @ 2014 OPS, Qunar Inc. (qunar.com)
#
# Author: tingfang.bao <tingfang.bao@qunar.com>
# DateTime: 14-7-22 下午4:34


def sql_attack(s):
    s = s.replace("\\", "\\\\")
    s = s.replace("'", "\\'")
    return s


def quoted_sql_attack(s):
    return "'%s'" % sql_attack(s)
