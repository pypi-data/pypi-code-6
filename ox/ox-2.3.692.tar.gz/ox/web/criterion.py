# -*- coding: UTF-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
from __future__ import print_function
import re

import ox.cache
from ox.cache import read_url
from ox.html import strip_tags
from ox.text import find_re

import imdb

def get_id(url):
    return url.split("/")[-1]

def get_url(id):
    return "http://www.criterion.com/films/%s" % id

def get_data(id, timeout=ox.cache.cache_timeout, get_imdb=False):
    '''
    >>> get_data('1333').get('imdbId')
    u'0060304'

    >>> get_data('236')['posters'][0]
    u'http://s3.amazonaws.com/criterion-production/release_images/1586/ThirdManReplace.jpg'

    >>> get_data('786')['posters'][0]
    u'http://s3.amazonaws.com/criterion-production/product_images/185/343_box_348x490.jpg'
    '''
    data = {
        "url": get_url(id)
    }
    try:
        html = read_url(data["url"], timeout=timeout, unicode=True)
    except:
        html = ox.cache.read_url(data["url"], timeout=timeout)
    data["number"] = find_re(html, "<li>Spine #(\d+)")

    data["title"] = find_re(html, "<h1 class=\"movietitle\">(.*?)</h1>")
    data["title"] = data["title"].split(u' \u2014 The Television Version')[0]
    data["director"] = strip_tags(find_re(html, "<h2 class=\"director\">(.*?)</h2>"))
    results = find_re(html, '<div class="left_column">(.*?)</div>')
    results = re.compile("<li>(.*?)</li>").findall(results)
    data["country"] = results[0]
    data["year"] = results[1]
    data["synopsis"] = strip_tags(find_re(html, "<div class=\"content_block last\">.*?<p>(.*?)</p>"))

    result = find_re(html, "<div class=\"purchase\">(.*?)</div>")
    if 'Blu-Ray' in result or 'Essential Art House DVD' in result:
        r = re.compile('<h3 class="section_title first">Other Editions</h3>(.*?)</div>', re.DOTALL).findall(html)
        if r:
            result = r[0]
    result = find_re(result, "<a href=\"(.*?)\"")
    if not "/boxsets/" in result:
        data["posters"] = [result]
    else:
        html_ = read_url(result, unicode=True)
        result = find_re(html_, '<a href="http://www.criterion.com/films/%s.*?">(.*?)</a>' % id)
        result = find_re(result, "src=\"(.*?)\"")
        if result:
            data["posters"] = [result.replace("_w100", "")]
        else:
            data["posters"] = []
    data['posters'] = [re.sub('(\?\d+)$', '', p) for p in data['posters']]
    result = find_re(html, "<img alt=\"Film Still\" height=\"252\" src=\"(.*?)\"")
    if result:
        data["stills"] = [result]
        data["trailers"] = []
    else:
        data["stills"] = filter(lambda x: x, [find_re(html, "\"thumbnailURL\", \"(.*?)\"")])
        data["trailers"] = filter(lambda x: x, [find_re(html, "\"videoURL\", \"(.*?)\"")])

    if timeout == ox.cache.cache_timeout:
        timeout = -1
    if get_imdb:
        # removed year, as "title (year)" may fail to match
        data['imdbId'] = imdb.get_movie_id(data['title'], data['director'], timeout=timeout)
    return data

def get_ids(page=None):
    ids = []
    if page:
        url = "http://www.criterion.com/library/expanded_view?m=dvd&p=%s&pp=50&s=spine" % page
        html = read_url(url)
        results = re.compile("films/(\d+)").findall(html)
        ids += results
        results = re.compile("boxsets/(.*?)\"").findall(html)
        for result in results:
            html = read_url("http://www.criterion.com/boxsets/" + result)
            results = re.compile("films/(\d+)").findall(html)
            ids += results
        return set(ids)
    html = read_url("http://www.criterion.com/library/expanded_view?m=dvd&p=1&pp=50&s=spine", unicode=True)
    results = re.compile("\&amp;p=(\d+)\&").findall(html)
    pages = max(map(int, results))
    for page in range(1, pages):
        ids += get_ids(page)
    return sorted(set(ids), key=int)

if __name__ == '__main__':
    print(get_ids())
