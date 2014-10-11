# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
from __future__ import print_function
import re

from ox import strip_tags, find_re
from ox.cache import read_url


def get_id(url):
    return url.split("/")[-1]

def get_data(id):
    '''
    >>> get_data('129689')['cast'][1][1]
    u'Marianne'
    >>> get_data('129689')['credits'][0][0]
    u'Jean-Luc Godard'
    >>> get_data('129689')['posters'][0]
    u'http://image.allmusic.com/00/adg/cov200/dru800/u812/u81260bbffr.jpg'
    >>> get_data('129689')['rating']
    u'4.5'
    '''
    if id.startswith('http'):
        id = get_id(id)
    data = {
        "url": get_url(id)
    }
    html = read_url(data["url"], unicode=True)
    data['aka'] = parse_list(html, 'AKA')
    data['category'] = find_re(html, '<dt>category</dt>.*?<dd>(.*?)</dd>')
    data['countries'] = parse_list(html, 'countries')
    data['director'] = parse_entry(html, 'directed by')
    data['genres'] = parse_list(html, 'genres')
    data['keywords'] = parse_list(html, 'keywords')
    data['posters'] = [find_re(html, '<img src="(http://cps-.*?)"')]
    data['produced'] = parse_list(html, 'produced by')
    data['rating'] = find_re(html, 'Stars" title="(.*?) Stars"')
    data['released'] = parse_entry(html, 'released by')
    data['releasedate'] = parse_list(html, 'release date')
    data['runtime'] = parse_entry(html, 'run time').replace('min.', '').strip()
    data['set'] = parse_entry(html, 'set in')
    data['synopsis'] = strip_tags(find_re(html, '<div class="toggle-text" itemprop="description">(.*?)</div>')).strip()
    data['themes'] = parse_list(html, 'themes')
    data['types'] = parse_list(html, 'types')
    data['year'] = find_re(html, '<span class="year">.*?(\d+)')
    #data['stills'] = [re.sub('_derived.*?/', '', i) for i in re.compile('<a href="#" title="movie still".*?<img src="(.*?)"', re.DOTALL).findall(html)]
    data['stills'] = re.compile('<a href="#" title="movie still".*?<img src="(.*?)"', re.DOTALL).findall(html)
    #html = read_url("http://allmovie.com/work/%s/cast" % id, unicode=True)
    #data['cast'] = parse_table(html)
    #html = read_url("http://allmovie.com/work/%s/credits" % id, unicode=True)
    #data['credits'] = parse_table(html)
    html = read_url("http://allmovie.com/work/%s/review" % id, unicode=True)
    data['review'] = strip_tags(find_re(html, '<div class="toggle-text" itemprop="description">(.*?)</div>')).strip()
    return data

def get_url(id):
    return "http://allmovie.com/work/%s" % id

def parse_entry(html, title):
    html = find_re(html, '<dt>%s</dt>.*?<dd>(.*?)</dd>' % title)
    return strip_tags(html).strip()

def parse_list(html, title):
    html = find_re(html, '<dt>%s</dt>.*?<dd>(.*?)</dd>' % title.lower())
    r = map(strip_tags, re.compile('<li>(.*?)</li>', re.DOTALL).findall(html))
    if not r and html:
        r = [strip_tags(html)]
    return r

def parse_table(html):
    return [
        [
            strip_tags(r).strip().replace('&nbsp;', '')
            for r in x.split('<td width="305">-')
        ]
        for x in find_re(html, '<div id="results-table">(.*?)</table>').split('</tr>')[:-1]
    ]

def parse_text(html, title):
    return strip_tags(find_re(html, '%s</td>.*?<td colspan="2"><p>(.*?)</td>' % title)).strip()

if __name__ == '__main__':
    print(get_data('129689'))
    # print(get_data('177524'))

