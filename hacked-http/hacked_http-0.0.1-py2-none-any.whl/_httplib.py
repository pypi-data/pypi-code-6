'''
Created on 2014. 6. 7.

@author: a141890
'''
from httplib import *
from httplib import HTTPConnection as _HTTPConnection, _CS_REQ_STARTED


class HTTPConnection(_HTTPConnection):
    
    def _output(self, s):
        if (self._HTTPConnection__state == _CS_REQ_STARTED and
            s.endswith(self._http_vsn_str) and not self._buffer):
            self._buffer.append('\r\n')  # will insert extra \r\n
        _HTTPConnection._output(self, s)
        