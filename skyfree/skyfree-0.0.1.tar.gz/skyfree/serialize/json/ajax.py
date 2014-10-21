#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4 et
#
# Copyright @ 2014 OPS, Qunar Inc. (qunar.com)
#
# Author: tingfang.bao <tingfang.bao@qunar.com>
# DateTime: 14-7-22 下午4:50
from flask import Response
from serialize.json.parser import json_dump


def _ajax_success(msg=u'success', data=u'', **kwargs):
    result = {}
    result.update(kwargs)
    result["success"] = True
    result["msg"] = msg
    result["data"] = data
    return json_dump(result)


def _ajax_error(msg, **kwargs):
    result = {}
    result.update(kwargs)
    result["success"] = False
    result["msg"] = msg
    return json_dump(result)


def api_success(msg=u'success', data=u'', **kwargs):
    return Response(_ajax_success(msg, data, **kwargs),
                    status=200, mimetype='application/json')


def api_error(error_msg, **kwargs):
    return Response(_ajax_error(error_msg, **kwargs),
                    status=200, mimetype='application/json')