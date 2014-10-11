# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
from datetime import datetime
import re

from six.moves.urllib.parse import quote

from ox import find_re, cache, strip_tags, decode_html, get_torrent_info, normalize_newlines
from ox.normalize import normalize_imdbid
import ox

from torrent import Torrent

cache_timeout = 24*60*60 # cache search only for 24 hours

season_episode = re.compile("S..E..", re.IGNORECASE)


def read_url(url, data=None, headers=cache.DEFAULT_HEADERS, timeout=cache.cache_timeout, valid=None, unicode=False):
    headers = headers.copy()
    headers['Cookie'] = 'language=en_EN'
    return cache.read_url(url, data, headers, timeout, unicode=unicode)

def find_movies(query=None, imdb=None, max_results=10):
    if imdb:
        query = "tt" + normalize_imdbid(imdb)
    results = []
    next = ["http://thepiratebay.org/search/%s/0/3/200" % quote(query), ]
    page_count = 1
    while next and page_count < 4:
        page_count += 1
        url = next[0]
        if not url.startswith('http'):
            if not url.startswith('/'):
                url = "/" + url
            url = "http://thepiratebay.org" + url
        data = read_url(url, timeout=cache_timeout, unicode=True)
        regexp = '''<tr.*?<td class="vertTh"><a href="/browse/(.*?)".*?<td><a href="(/torrent/.*?)" class="detLink".*?>(.*?)</a>.*?</tr>'''
        for row in  re.compile(regexp, re.DOTALL).findall(data):
            torrentType = row[0]
            torrentLink = "http://thepiratebay.org" + row[1]
            torrentTitle = decode_html(row[2])
            # 201 = Movies , 202 = Movie DVDR, 205 TV Shows
            if torrentType in ['201']:
                results.append((torrentTitle, torrentLink, ''))
            if len(results) >= max_results:
                return results
        next = re.compile('<a.*?href="(.*?)".*?>.*?next.gif.*?</a>').findall(data)
    return results

def get_id(piratebayId):
    if piratebayId.startswith('http://torrents.thepiratebay.org/'):
        piratebayId = piratebayId.split('org/')[1]
    d = find_re(piratebayId, "tor/(\d+)")
    if d:
        piratebayId = d
    d = find_re(piratebayId, "torrent/(\d+)")
    if d:
        piratebayId = d
    return piratebayId

def exists(piratebayId):
    piratebayId = get_id(piratebayId)
    return ox.net.exists("http://thepiratebay.org/torrent/%s" % piratebayId)

def get_data(piratebayId):
    _key_map = {
      'spoken language(s)': u'language',
      'texted language(s)': u'subtitle language',
      'by': u'uploader',
      'leechers': 'leecher',
      'seeders': 'seeder',
    }
    piratebayId = get_id(piratebayId)
    torrent = dict()
    torrent[u'id'] = piratebayId
    torrent[u'domain'] = 'thepiratebay.org'
    torrent[u'comment_link'] = 'http://thepiratebay.org/torrent/%s' % piratebayId

    data = read_url(torrent['comment_link'], unicode=True)
    torrent[u'title'] = find_re(data, '<title>(.*?) \(download torrent\) - TPB</title>')
    if not torrent[u'title']:
        return None
    torrent[u'title'] = decode_html(torrent[u'title']).strip()
    torrent[u'imdbId'] = find_re(data, 'title/tt(\d{7})')
    title = quote(torrent['title'].encode('utf-8'))
    torrent[u'torrent_link']="http://torrents.thepiratebay.org/%s/%s.torrent" % (piratebayId, title)
    for d in re.compile('dt>(.*?):</dt>.*?<dd.*?>(.*?)</dd>', re.DOTALL).findall(data):
        key = d[0].lower().strip()
        key = _key_map.get(key, key)
        value = decode_html(strip_tags(d[1].strip()))
        torrent[key] = value
    torrent[u'description'] = find_re(data, '<div class="nfo">(.*?)</div>')
    if torrent[u'description']:
        torrent['description'] = normalize_newlines(decode_html(strip_tags(torrent['description']))).strip()
    t = read_url(torrent[u'torrent_link'])
    torrent[u'torrent_info'] = get_torrent_info(t)
    return torrent

class Thepiratebay(Torrent):
    '''
    >>> Thepiratebay('123')
    {}

    >>> Thepiratebay('3951349')['infohash']
    '4e84415d36ed7b54066160c05a0b0f061898d12b'
    '''
    def __init__(self, piratebayId):
        self.data = get_data(piratebayId)
        if not self.data:
            return
        Torrent.__init__(self)
        published =  self.data['uploaded']
        published = published.replace(' GMT', '').split(' +')[0]
        self['published'] =  datetime.strptime(published, "%Y-%m-%d %H:%M:%S")

