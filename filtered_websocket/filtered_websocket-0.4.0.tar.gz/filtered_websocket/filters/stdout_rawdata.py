from __future__ import absolute_import

import sys
from .base import WebSocketDataFilter


class StdoutRawDataFilter(WebSocketDataFilter):

    @classmethod
    def filter(cls, web_socket_instance, data):
        sys.stdout.writelines("--RAWDATA--\n%s\n" % data)
        sys.stdout.flush()
