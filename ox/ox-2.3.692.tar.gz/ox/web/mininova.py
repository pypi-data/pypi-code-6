# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
from datetime import datetime
import re
import socket
from six.moves.urllib.parse import quote

from ox.cache import read_url
from ox import find_re, cache, strip_tags, decode_html, get_torrent_info, int_value, normalize_newlines
from ox.normalize import normalize_imdbid
import ox

from torrent import Torrent


def _parse_results_page(data, max_results=10):
    results=[]
    regexp = '''<tr><td>(.*?)</td><td>(.*?)<a href="/tor/(.*?)">(.*?)</a>.*?</td>.*?</tr>'''
    for row in  re.compile(regexp, re.DOTALL).findall(data):
        torrentDate = row[0]
        torrentExtra = row[1]
        torrentId = row[2]
        torrentTitle = decode_html(row[3]).strip()
        torrentLink = "http://www.mininova.org/tor/" + torrentId
        privateTracker = 'priv.gif' in torrentExtra
        if not privateTracker:
            results.append((torrentTitle, torrentLink, ''))
    return results

def find_movie(query=None, imdb=None, max_results=10):
    '''search for torrents on mininova
    '''
    if imdb:
        url = "http://www.mininova.org/imdb/?imdb=%s" % normalize_imdbid(imdb)
    else:
        url = "http://www.mininova.org/search/%s/seeds" % quote(query)
    data = read_url(url, unicode=True)
    return _parse_results_page(data, max_results)

def get_id(mininovaId):
    mininovaId = unicode(mininovaId)
    d = find_re(mininovaId, "/(\d+)")
    if d:
        return d
    mininovaId = mininovaId.split('/')
    if len(mininovaId) == 1:
        return mininovaId[0]
    else:
        return mininovaId[-1]

def exists(mininovaId):
    mininovaId = get_id(mininovaId)
    data = ox.net.read_url("http://www.mininova.org/tor/%s" % mininovaId)
    if not data or 'Torrent not found...' in data:
        return False
    if 'tracker</a> of this torrent requires registration.' in data:
        return False
    return True

def get_data(mininovaId):
    _key_map = {
        'by': u'uploader',
    }
    mininovaId = get_id(mininovaId)
    torrent = dict()
    torrent[u'id'] = mininovaId
    torrent[u'domain'] = 'mininova.org'
    torrent[u'comment_link'] = "http://www.mininova.org/tor/%s" % mininovaId
    torrent[u'torrent_link'] = "http://www.mininova.org/get/%s" % mininovaId
    torrent[u'details_link'] = "http://www.mininova.org/det/%s" % mininovaId

    data = read_url(torrent['comment_link'], unicode=True) + read_url(torrent['details_link'], unicode=True)
    if '<h1>Torrent not found...</h1>' in data:
        return None

    for d in re.compile('<p>.<strong>(.*?):</strong>(.*?)</p>', re.DOTALL).findall(data):
        key = d[0].lower().strip()
        key = _key_map.get(key, key)
        value = decode_html(strip_tags(d[1].strip()))
        torrent[key] = value

    torrent[u'title'] = find_re(data, '<title>(.*?):.*?</title>')
    torrent[u'imdbId'] = find_re(data, 'title/tt(\d{7})')
    torrent[u'description'] = find_re(data, '<div id="description">(.*?)</div>')
    if torrent['description']:
        torrent['description'] = normalize_newlines(decode_html(strip_tags(torrent['description']))).strip()
    t = read_url(torrent[u'torrent_link'])
    torrent[u'torrent_info'] = get_torrent_info(t)
    return torrent

class Mininova(Torrent):
    '''
    >>> Mininova('123')
    {}
    >>> Mininova('1072195')['infohash']
    '72dfa59d2338e4a48c78cec9de25964cddb64104'
    '''
    def __init__(self, mininovaId):
        self.data = get_data(mininovaId)
        if not self.data:
            return
        Torrent.__init__(self)
        ratio = self.data['share ratio'].split(',')
        self['seeder'] = -1
        self['leecher'] = -1
        if len(ratio) == 2:
            val = int_value(ratio[0].replace(',','').strip())
            if val:
                self['seeder'] = int(val)
            val = int_value(ratio[1].replace(',','').strip())
            if val:
                self['leecher'] = int(val)
        val = int_value(self.data['downloads'].replace(',','').strip())
        if val:
            self['downloaded'] = int(val)
        else:
            self['downloaded'] = -1
        published =  self.data['added on']
        published = published.split(' +')[0]
        self['published'] =  datetime.strptime(published, "%a, %d %b %Y %H:%M:%S")

