# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
from __future__ import print_function
import json
import os
import re

from ox import find_re, strip_tags
from ox.cache import read_url

def get_data(id, language='en'):
    if language == 'de':
        url = 'http://films.arsenal-berlin.de/index.php/Detail/Object/Show/object_id/%d/lang/de_DE' % id
    else:
        url = 'http://films.arsenal-berlin.de/index.php/Detail/Object/Show/object_id/%d' % id
    html = read_url(url, unicode=True)
    if 'ID does not exist' in html:
        return None
    if 'Willkommen in der Datenbank des Arsenal' in html:
        return None
    data = {}
    data[u'id'] = id
    data[u'url'] = url
    m = re.compile('<h1>(.*?)</h1>').findall(html)
    if m:
        data[u'title'] = m[0]
    m = re.compile("<b>Director: </b><a href='.*?'>(.*?)</a>").findall(html)
    if m:
        data[u'director'] = m[0]

    m = re.compile("caUI.initImageScroller\(\[\{url:'(.*?)'").findall(html)
    if m:
        data[u'image'] = m[0]

    units = re.compile("<div class='unit'>(.*?)</div>", re.DOTALL).findall(html)
    for x in map(re.compile('<b>(.*?)</b>: (.*)', re.DOTALL).findall, units):
        if x:
            #data[x[0][0].lower()] = strip_tags(x[0][1])
            key = x[0][0].lower()
            data[key] = x[0][1]
            if key == "forum catalogue pdf":
                data[key] = find_re(data[key], '"(http:.*?)"')
            else:
                data[key] = strip_tags(data[key])
    if "running time (minutes)" in data:
        data[u'runtime'] = float(data.pop("running time (minutes)").replace(',', '.')) * 60
    for key in ('year', 'length in metres', 'forum participation year', 'number of reels'):
        if key in data and data[key].isdigit():
            data[key] = int(data[key])
    return data

def backup(filename):
    if os.path.exists(filename):
        with open(filename) as f:
            data = json.load(f)
    else:
        data = {}
    start = max(map(int, data)) or 1
    for i in range(start, 11872):
        info = get_data(i)
        if info:
            data[i] = info
            if len(data) % 10 == 0:
                print('save', filename, len(data))
                with open(filename, 'w') as f:
                    json.dump(data, f)
        else:
            print('ignore', i)
    with open(filename, 'w') as f:
        json.dump(data, f)
    return data

