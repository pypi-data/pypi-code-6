# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import ox.cache

def get_poster_url(id):
    url = "http://0xdb.org/%s/poster.0xdb.jpg" % id
    if ox.cache.exists(url):
        return url
    return ''

