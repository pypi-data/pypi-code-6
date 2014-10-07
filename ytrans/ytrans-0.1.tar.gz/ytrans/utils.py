# coding: utf-8
import os
import sys

try:
    # Py3
    from urllib.parse import urlencode, urljoin
    from urllib.request import urlopen

    def to_string(s):
        return s
except ImportError:
    # Py2
    from urlparse import urljoin
    from urllib2 import urlopen
    from urllib import urlencode

    def to_string(s):
        return unicode(s).encode('utf-8')

if sys.version_info.major >= 3:
    bytefy_kwargs = {'encoding': 'utf-8'}
else:
    bytefy_kwargs = {}


_bytes = bytes


def bytes(value):
    return _bytes(value, **bytefy_kwargs)


def check_existance_and_permissions(path_to_check, permissions=os.R_OK):
    if not (path_to_check and os.path.isfile(path_to_check)):
        raise IOError(
            u"{0} must be regular file!".format(path_to_check))

    elif not os.access(path_to_check, permissions):
        raise IOError(u"Access denied! {0}!".format(path_to_check))


def request(method, data=None):
    from ytrans.settings import URL
    return urlopen(urljoin(URL, method), data=data)
