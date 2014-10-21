#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4 et
#
# Copyright @ 2014 OPS, Qunar Inc. (qunar.com)
#
# Author: tingfang.bao <tingfang.bao@qunar.com>
# DateTime: 14-7-22 下午4:29
import json
from datetime import datetime
from datetime import date
import decimal


def _jsonify(mix):
    result = None
    if isinstance(mix, list):
        result = []
        for i in mix:
            result.append(_jsonify(i))
    elif isinstance(mix, dict):
        result = {}
        for k, v in mix.items():
            k = _jsonify(k)
            v = _jsonify(v)
            result[k] = v
    elif isinstance(mix, datetime):
        result = mix.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(mix, date):
        result = mix.strftime('%Y-%m-%d')
    elif isinstance(mix, decimal.Decimal):
        result = float(mix)
    else:
        return mix
    return result


def json_dump(mix):
    mix = _jsonify(mix)
    return json.dumps(mix)


def json_loads(value):
    if value is not None and value.strip() != '':
        return json.loads(value)
    return None