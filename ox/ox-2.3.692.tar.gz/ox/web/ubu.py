# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
from __future__ import print_function
import re

from ox import find_re, strip_tags, decode_html
from ox.cache import read_url


def get_id(url):
    return url.replace('http://www.ubu.com/', '').split('.html')[0]

def get_url(id):
    return 'http://www.ubu.com/%s.html' % id

def get_data(url):
    if not url.startswith('http:'):
        url = get_url(url)
    data = read_url(url, unicode=True)
    m = {
        'id': get_id(url),
        'url': url,
        'type': re.compile('ubu.com/(.*?)/').findall(url)[0]
    }
    for videourl, title in re.compile('<a href="(http://ubumexico.centro.org.mx/.*?)">(.*?)</a>').findall(data):
        if videourl.endswith('.srt'):
            m['srt'] = videourl
        elif not 'video' in m:
            m['video'] = videourl
            m['video'] = m['video'].replace('/video/ ', '/video/').replace(' ', '%20')
            if m['video'] == 'http://ubumexico.centro.org.mx/video/':
                del m['video']
            m['title'] = strip_tags(decode_html(title)).strip()
    if not 'url' in m:
        print(url, 'missing')
    if 'title' in m:
        m['title'] = re.sub('(.*?) \(\d{4}\)$', '\\1', m['title'])

    match = re.compile("flashvars','file=(.*?.flv)'").findall(data)
    if match:
        m['flv'] = match[0]
        m['flv'] = m['flv'].replace('/video/ ', '/video/').replace(' ', '%20')

    y = re.compile('\((\d{4})\)').findall(data)
    if y:
        m['year'] = int(y[0])
    d = re.compile('Director: (.+)').findall(data)
    if d:
        m['director'] = strip_tags(decode_html(d[0])).strip()

    a = re.compile('<a href="(.*?)">Back to (.*?)</a>', re.DOTALL).findall(data)
    if a:
        m['artist'] = strip_tags(decode_html(a[0][1])).strip()
    else:
        a = re.compile('<a href="(.*?)">(.*?) in UbuWeb Film').findall(data)
        if a:
            m['artist'] = strip_tags(decode_html(a[0][1])).strip()
        else:
            a = re.compile('<b>(.*?)\(b\..*?\d{4}\)').findall(data)
            if a:
                m['artist'] = strip_tags(decode_html(a[0])).strip()
            elif m['id'] == 'film/lawder_color':
                m['artist'] = 'Standish Lawder'
    if 'artist' in m:
        m['artist'] = m['artist'].replace('in UbuWeb Film', '')
        m['artist'] = m['artist'].replace('on UbuWeb Film', '').strip()
    if m['id'] == 'film/coulibeuf':
        m['title'] = 'Balkan Baroque'
        m['year'] = 1999
    return m

def get_films():
    ids = get_ids()
    films = []
    for id in ids:
        info = get_data(id)
        if info['type'] == 'film' and ('flv' in info or 'video' in info):
            films.append(info)
    return films

def get_ids():
    data = read_url('http://www.ubu.com/film/')
    ids = []
    author_urls = []
    for url, author in re.compile('<a href="(\./.*?)">(.*?)</a>').findall(data):
        url = 'http://www.ubu.com/film' + url[1:]
        data = read_url(url)
        author_urls.append(url)
        for u, title in re.compile('<a href="(.*?)">(.*?)</a>').findall(data):
            if not u.startswith('http'):
                if u == '../../sound/burroughs.html':
                    u = 'http://www.ubu.com/sound/burroughs.html'
                elif u.startswith('../'):
                    u = 'http://www.ubu.com/' + u[3:]
                else:
                    u = 'http://www.ubu.com/film/' + u
                if u not in author_urls and u.endswith('.html'):
                    ids.append(u)
    ids = [get_id(url) for url in list(set(ids))]
    return ids
