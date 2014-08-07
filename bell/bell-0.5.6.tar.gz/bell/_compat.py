# coding=utf8

import sys

if sys.version_info[0] < 3:
    nativestr = lambda x: x.encode('utf8', 'replace') \
        if isinstance(x, unicode) else str(x)
else:
    nativestr = lambda x: x.decode('utf8', 'replace') \
        if isinstance(x, bytes) else str(x)
