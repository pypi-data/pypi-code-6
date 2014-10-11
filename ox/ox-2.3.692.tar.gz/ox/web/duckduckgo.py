# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import re

from six.moves import urllib
import ox
from ox import strip_tags, decode_html
from ox.cache import read_url


def find(query, timeout=ox.cache.cache_timeout):
    if not isinstance(query, bytes):
        query = query.encode('utf-8')
    params = urllib.parse.urlencode({'q': query})
    url = 'http://duckduckgo.com/html/?' + params
    data = read_url(url, timeout=timeout).decode('utf-8')
    results = []
    regex = '<a .*?class="large" href="(.+?)">(.*?)</a>.*?<div class="snippet">(.*?)</div>'
    for r in re.compile(regex, re.DOTALL).findall(data):
        results.append((strip_tags(decode_html(r[1])), r[0], strip_tags(decode_html(r[2]))))
    return results
    
