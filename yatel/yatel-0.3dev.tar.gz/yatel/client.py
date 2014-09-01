#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY us return.


#==============================================================================
# DOCS
#==============================================================================

"""Client library for yatel

"""


#==============================================================================
# IMPORTS
#==============================================================================

import json
import requests
import collections

from yatel import typeconv


#==============================================================================
# CLASS
#==============================================================================

QBJResponse = collections.namedtuple(
    "QBJResponse",
    ["id", "response", "json", "yatel", "error", "error_msg", "stack_trace"]
)


class QBJClientError(Exception):

    def __init__(self, qbjresponse):
        super(QBJClientError, self).__init__(self, qbjresponse.error_msg)
        self._response = qbjresponse

    @property
    def response(self):
        return self.response


class QBJClient(object):

    def __init__(self, url, nwname):
        while url.endswith("/"):
            url = url[1:]
        self.url = url
        self.nwname = nwname
        self.full_url = "/".join([self.url, "qbj", nwname])

    def parse_response(self, response):
        as_json = response.json()
        yatel = None if as_json["error"] else typeconv.parse(as_json["result"])
        return QBJResponse(
            id=as_json["id"], response=response, json=as_json, yatel=yatel,
            error=as_json["error"], error_msg=as_json["error_msg"],
            stack_trace=as_json["stack_trace"]
        )

    def execute(self, query):
        serialized = json.dumps(query)
        response = requests.post(
            self.full_url, data=serialized,
            headers={'content-type':"application/json"}
        )
        qbjresponse = self.parse_response(response)
        if qbjresponse.error:
            raise QBJClientError(qbjresponse)
        return qbjresponse


#==============================================================================
# MAIN
#==============================================================================

if __name__ == "__main__":
    print(__doc__)



