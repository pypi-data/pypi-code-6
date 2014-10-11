# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
from __future__ import print_function

import re

from six.moves import urllib

from ox.utils import json
from ox.cache import read_url
from ox import find_re


def get_id(url):
    return url.split("/")[-1]

def get_url(id=None, imdb=None, allmovie=None):
    if imdb:
        query = '"%s"'% imdb
        result = find(query)
        if result:
            url = result[0][1]
            data = get_movie_data(url)
            if 'imdb_id' in data:
                return url
        return ""
    if allmovie:
        query = '"amg_id = 1:%s"'% allmovie
        result = find(query)
        if result:
            url = result[0][1]
            return url
        return ''
    return "http://en.wikipedia.org/wiki/%s" % id

def get_movie_id(title, director='', year=''):
    query = '"%s" film %s %s' % (title, director, year)
    result = find(query, 1)
    if result:
        return result[0][1]
    return ''

def get_wiki_data(wikipedia_url):
    url = wikipedia_url.replace('wikipedia.org/wiki/', 'wikipedia.org/w/index.php?title=')
    url = "%s&action=raw" % url
    data = read_url(url).decode('utf-8')
    return data

def get_movie_data(wikipedia_url):
    if not wikipedia_url.startswith('http'):
        wikipedia_url = get_url(wikipedia_url)
    data = get_wiki_data(wikipedia_url)
    filmbox_data = find_re(data, '''\{\{[Ii]nfobox.[Ff]ilm(.*?)\n\}\}''')
    filmbox = {}
    _box = filmbox_data.strip().split('|')
    for row in _box:
        d = row.split('=')
        if len(d) == 2:
            _key = d[0].strip()
            if _key:
                key = _key
                if key[0] == '|':
                    key = key[1:]
                key = key.strip()
                value = d[1].strip()
                value = value.replace('<!-- see WP:ALT -->', '')
                if '<br>' in value:
                    value = value.split('<br>')
                if value:
                    if key in filmbox:
                        if isinstance(value, list) and isinstance(filmbox[key], basestring):
                            filmbox[key] = [filmbox[key]] + value
                        else:
                            filmbox[key] += value
                        if isinstance(filmbox[key], list):
                            filmbox[key] = [k for k in filmbox[key] if k]
                    else:
                        filmbox[key] = value
    if not filmbox_data:
        return filmbox
    if 'amg_id' in filmbox and not filmbox['amg_id'].isdigit():
        del filmbox['amg_id']
    if 'Allmovie movie' in data:
        filmbox['amg_id'] = find_re(data, 'Allmovie movie\|.*?(\d+)')
    elif 'Allmovie title' in data:
        filmbox['amg_id'] = find_re(data, 'Allmovie title\|.*?(\d+)')

    if 'Official website' in data:
        filmbox['website'] = find_re(data, 'Official website\|(.*?)}').strip()

    r = re.compile('{{IMDb title\|id=(\d{7})', re.IGNORECASE).findall(data)
    if r:
        filmbox['imdb_id'] = r[0]
    else:
        r = re.compile('{{IMDb title\|(\d{7})', re.IGNORECASE).findall(data)
        if r:
            filmbox['imdb_id'] = r[0]

    r = re.compile('{{Internet Archive.*?\|id=(.*?)[\|}]', re.IGNORECASE).findall(data)
    if r:
        filmbox['archiveorg_id'] = r[0]

    r = re.compile('{{mojo title\|(.*?)[\|}]', re.IGNORECASE).findall(data)
    if r:
        filmbox['mojo_id'] = r[0].replace('id=', '')

    r = re.compile('{{rotten-tomatoes\|(.*?)[\|}]', re.IGNORECASE).findall(data)
    if r:
        filmbox['rottentomatoes_id'] = r[0].replace('id=', '')
    if 'google video' in data:
        filmbox['google_video_id'] = find_re(data, 'google video\|.*?(\d*?)[\|}]')
    if 'DEFAULTSORT' in data:
        filmbox['title_sort'] = find_re(data, '''\{\{DEFAULTSORT:(.*?)\}\}''')
    return filmbox

def get_image_url(name):
    url = 'http://en.wikipedia.org/wiki/Image:' + name.replace(' ', '%20')
    data = read_url(url)
    url = find_re(data, 'href="(http://upload.wikimedia.org/.*?)"')
    if not url:
        url = find_re(data, 'href="(//upload.wikimedia.org/.*?)"')
        if url:
            url = 'http:' + url
    return url

def get_poster_url(wikipedia_url):
    if not wikipedia_url.startswith('http'): wikipedia_url = get_url(wikipedia_url)
    data = get_movie_data(wikipedia_url)
    if 'image' in data:
        return get_image_url(data['image'])
    return ''

def get_movie_poster(wikipedia_url):
    # deprecated, use get_poster_url()
    return get_poster_url(wikipedia_url)

def get_allmovie_id(wikipedia_url):
    data = get_movie_data(wikipedia_url)
    return data.get('amg_id', '')

def find(query, max_results=10):
    query = {'action': 'query', 'list':'search', 'format': 'json',
             'srlimit': max_results, 'srwhat': 'text', 'srsearch': query.encode('utf-8')}
    url = "http://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode(query)
    data = read_url(url)
    if not data:
        data  = read_url(url, timeout=0)
    result = json.loads(data.decode('utf-8'))
    results = []
    if result and 'query' in result:
        for r in result['query']['search']:
            title = r['title']
            url = "http://en.wikipedia.org/wiki/%s" % title.replace(' ', '_')
            results.append((title, url, ''))
    return results

