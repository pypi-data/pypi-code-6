#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4 et
#
# Copyright @ 2014 OPS, Qunar Inc. (qunar.com)
#
# Author: tingfang.bao <tingfang.bao@qunar.com>
# DateTime: 14-7-22 下午4:54
import json
import base64
import httplib2
import urllib

__all__ = ('post', 'get', 'postJson')


def post(url, params=None, header=None, basic_auth=None):
    return _do(url, "POST",
               body=params,
               headers=header,
               basic_auth=basic_auth,
               use_json_body=False)


def get(url, params=None, header=None, basic_auth=None):
    return _do(url, "GET",
               body=params,
               headers=header,
               basic_auth=basic_auth,
               use_json_body=False)


def post_json(url, params, header=None, basic_auth=None):
    header = {
        "Content-type": "application/json"
    }
    return _do(url, "POST",
               body=params,
               headers=header,
               basic_auth=basic_auth,
               use_json_body=True)


def _do(url, method, body=None, headers=None, basic_auth=None,
        use_json_body=False):
    """

    :param url: 请求的URL
    :param method: 请求的方法，get,post postJson
    :param body: 请求的内容，可以是字符串，也可以为dict
    :param headers: 请求header，类型为dict
    :param basic_auth: basic认证信息，为二元组，或则两个值的列表(username,password)
    :param use_json_body: 请求内容body是否为json格式
    :return: true, 200 content
    """
    _headers = {}
    _body = None

    if isinstance(headers, dict):
        _headers.update(headers)

    if basic_auth is not None and len(basic_auth) == 2:
        auth = base64.encodestring("%s:%s" % basic_auth)
        _headers['Authorization'] = "Basic " + auth

    if use_json_body and method == 'POST':
        _headers["Content-type"] = "application/json; charset=UTF-8"
        _body = json.dumps(body)
    elif isinstance(body, dict):
        _headers["Content-type"] = \
            "application/x-www-form-urlencoded; charset=UTF-8"
        _body = urllib.urlencode(body)
    elif isinstance(body, basestring):
        _headers["Content-type"] = \
            "application/x-www-form-urlencoded; charset=UTF-8"
        _body = str(body)

    client = httplib2.Http(None, disable_ssl_certificate_validation=True)
    resp, content = client.request(url, method, _body, _headers)
    status = int(resp["status"])

    is_ok = status in (200, 201, 202)

    return is_ok, status, content
