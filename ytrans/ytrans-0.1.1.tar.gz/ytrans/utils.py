# coding: utf-8
import os
import sys

try:
    # Py3
    from urllib.parse import urlencode, urljoin
    from urllib.request import urlopen

    def to_unicode(s):
        return s

    def to_str(s):
        return s

    def encoded_dict(in_dict):
        return in_dict


except ImportError:
    # Py2
    from urlparse import urljoin
    from urllib2 import urlopen
    from urllib import urlencode

    def to_unicode(s):
        if not isinstance(s, unicode):
            return unicode(s, encoding='utf-8')
        return s

    def to_str(s):
        if isinstance(s, unicode):
            s = s.encode('utf8')
        elif isinstance(s, str):
            # Must be encoded in UTF-8
            s.decode('utf8')
        return s

    def encoded_dict(in_dict):
        out_dict = {}
        for k, v in in_dict.iteritems():
            out_dict[k] = to_str(v)
        return out_dict

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
            "{0} must be regular file!".format(to_unicode(path_to_check)))

    elif not os.access(path_to_check, permissions):
        raise IOError("Access denied! {0}!".format(to_unicode(path_to_check)))


def request(method, data=None):
    from ytrans.settings import URL
    return urlopen(urljoin(URL, method), data=data)


