# -*- coding: UTF-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
from __future__ import print_function

import re

from ox.cache import read_url
from ox import find_re

def get_data(id):
    '''
    >>> get_data('0060304')['posters'][0]
    u'http://www.movieposterdb.com/posters/06_03/1967/0060304/l_99688_0060304_639fdd1e.jpg'
    >>> get_data('0123456')['posters']
    []
    '''
    data = {
        "url": get_url(id)
    }
    data["posters"] = get_posters(data["url"])
    return data

def get_id(url):
    return url.split("/")[-2]

def get_posters(url, group=True, timeout=-1):
    posters = []
    html = read_url(url, timeout=timeout, unicode=True)
    if url in html:
        if group:
            results = re.compile('<a href="(http://www.movieposterdb.com/group/.+?)\??">', re.DOTALL).findall(html)
            for result in results:
                posters += get_posters(result, False)
        results = re.compile('<a href="(http://www.movieposterdb.com/poster/.+?)">', re.DOTALL).findall(html)
        for result in results:
            html = read_url(result, timeout=timeout, unicode=True)
            posters.append(find_re(html, '"(http://www.movieposterdb.com/posters/.+?\.jpg)"'))
    return posters

def get_url(id):
    return "http://www.movieposterdb.com/movie/%s/" % id

if __name__ == '__main__':
    print(get_data('0060304'))
    print(get_data('0133093'))
