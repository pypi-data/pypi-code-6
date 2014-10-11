# -*- coding: UTF-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import re
from lxml.html import document_fromstring

from ox.cache import read_url
from ox import find_re, strip_tags
from ox.web.imdb import ImdbCombined


def get_data(id, timeout=-1):
    '''
    >>> get_data('the-matrix')['poster']
    'http://content7.flixster.com/movie/16/90/52/1690525_gal.jpg'

    >>> get_data('0133093')['poster']
    'http://content7.flixster.com/movie/16/90/52/1690525_gal.jpg'

    >>> get_data('2-or-3-things-i-know-about-her')['poster']
    'http://content6.flixster.com/movie/10/95/43/10954392_gal.jpg'

    >>> get_data('0078875')['rottentomatoes_id']
    'http://www.rottentomatoes.com/m/the-tin-drum/'
    '''
    if len(id) == 7:
        try:
            int(id)
            id = get_id(imdb=id)
        except:
            pass
    data = {
        "url": get_url(id),
    }
    html = read_url(data['url'], timeout=timeout, unicode=True)
    doc = document_fromstring(html)

    props = {
        'og:title': 'title',
        'og:image': 'poster',
        'og:url': 'rottentomatoes_id',
    }
    for meta in doc.head.findall('meta'):
        prop = meta.attrib.get('property', None)
        content = meta.attrib.get('content', '')
        if prop in props and content:
            data[props[prop]] = content

    for p in doc.body.find_class('synopsis'):
        data['synopsis'] = p.text.strip()

    if 'poster' in data and data['poster']:
        data['poster'] = data['poster'].replace('_pro.jpg', '_gal.jpg')
    if not 'title' in data:
        return None
    return data

def get_id(url=None, imdb=None):
    '''
    >>> get_id(imdb='0133093')
    u'the-matrix'

    #>>> get_id(imdb='0060304')
    #u'2-or-3-things-i-know-about-her'
    '''
    if imdb:
        i = ImdbCombined(imdb)
        title = i['title']
        return title.replace(' ', '-').lower().replace("'", '')
    return url.split('/')[-1]

def get_url(id):
    return "http://www.flixster.com/movie/%s"%id

