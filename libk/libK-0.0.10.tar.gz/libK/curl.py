import StringIO
from kernel import kernel
import pycurl
import random

__author__ = 'negash'


def curl(url, tor=False):
    b = StringIO.StringIO()
    a = pycurl.Curl()
    a.setopt(pycurl.WRITEFUNCTION, b.write)
    a.setopt(pycurl.URL, url)
    a.setopt(pycurl.USERAGENT, random.choice(kernel['user_agent']))
    if tor:
        a.setopt(pycurl.PROXY, 'localhost')
        a.setopt(pycurl.PROXYPORT, 9050)
    a.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5)
    a.perform()
    a.close()
    html = b.getvalue()
    return html