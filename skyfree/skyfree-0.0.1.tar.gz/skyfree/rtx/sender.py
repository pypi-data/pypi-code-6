#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4 et
#
# Copyright @ 2014 OPS, Qunar Inc. (qunar.com)
#
# Author: tingfang.bao <tingfang.bao@qunar.com>
# DateTime: 14-7-22 下午5:09

import httplib2
import urllib

# 暂时还不好用，知道RTX可以有接口调用就好了


class RtxSender(object):
    def __init__(self, host, port, sender_user, sender_passwd):
        self.host = host
        self.port = port
        self.sender_user = sender_user
        self.sender_passwd = sender_passwd
        self.last_status = None
        self.last_response = None

    def get_session(self, receiver):
        url = "/GetSession.cgi"

        params = {"receiver": receiver}
        status_code, header, content = self._http_get(url, params)

        self.last_status = status_code
        self.last_response = content

        print status_code, header

    def send_message(self, receivers, msg, sessionid):
        url = "/SendIM.cgi"

        if isinstance(receivers, list):
            receivers = ";".join(receivers)

        params = {
            "sender": self.sender_user,
            "pwd": self.sender_passwd,
            "receivers": receivers,
            "msg": msg.encode("GBK"),
            "sessionid": "{%s}" % str(sessionid)
        }

        status_code, header, content = self._http_get(url, params)

        return status_code, content

    def _http_get(self, url_suffix, data):
        url = self._make_url(url_suffix, data)
        client = httplib2.Http()
        resp, content = client.request(url, "GET")
        print 'aaa'
        return resp["status"], resp, content

    def _make_url(self, url_suffix, data):
        params = []
        for key, value in data.items():
            params.append("%s=%s" % (key, urllib.quote(value)))

        url = "%s:%d%s?%s" % (
            self.host, self.port, url_suffix, "&".join(params))
        print url
        return url
