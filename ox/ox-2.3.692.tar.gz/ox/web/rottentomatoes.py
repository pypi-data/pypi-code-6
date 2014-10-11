# -*- coding: UTF-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import re

from ox.cache import read_url
from ox import find_re, strip_tags


def get_url(id=None, imdb=None):
    if imdb:
        url = "http://www.rottentomatoes.com/alias?type=imdbid&s=%s" % imdb
        data = read_url(url)
        if "movie_title" in data:
            movies = re.compile('(/m/.*?/)').findall(data)
            if movies:
                return "http://www.rottentomatoes.com" + movies[0]
    return None

def get_og(data, key):
    return find_re(data, '<meta property="og:%s".*?content="(.*?)"' % key)

def get_data(url):
    data = read_url(url)
    r = {}
    r['title'] = find_re(data, '<h1 class="movie_title">(.*?)</h1>')
    if '(' in r['title']:
        r['year'] = find_re(r['title'], '\((\d*?)\)')
        r['title'] = strip_tags(re.sub('\((\d*?)\)', '', r['title'])).strip()
    r['summary'] = strip_tags(find_re(data, '<p id="movieSynopsis" class="movie_synopsis" itemprop="description">(.*?)</p>')).strip()
    r['summary'] = r['summary'].replace('\t', ' ').replace('\n', ' ').replace('  ', ' ').replace('  ', ' ')
    if not r['summary']:
        r['summary'] = get_og(data, 'description')

    meter = re.compile('<span id="all-critics-meter" class="meter(.*?)">(.*?)</span>').findall(data)
    meter = filter(lambda m: m[1].isdigit(), meter)
    if meter:
        r['tomatometer'] = meter[0][1]
    r['rating'] = find_re(data, 'Average Rating: <span>([\d.]+)/10</span>')
    r['user_score'] = find_re(data, '<span class="meter popcorn numeric ">(\d+)</span>')
    r['user_rating'] = find_re(data, 'Average Rating: ([\d.]+)/5')
    poster = get_og(data, 'image')
    if poster and not 'poster_default.gif' in poster:
        r['posters'] = [poster]
    for key in r.keys():
        if not r[key]:
            del r[key]
    return r

