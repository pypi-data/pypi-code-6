# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import re
from datetime import datetime
from six.moves.urllib.parse import quote

import lxml.html
import ox
from ox.cache import read_url

def find(query=None, user=None, timeout=60):
    if user:
        url = 'https://twitter.com/' + quote(user)
    else:
        url = 'https://twitter.com/search/' + quote(query)
    data = ox.cache.read_url(url, timeout=timeout).decode('utf-8')
    doc = lxml.html.document_fromstring(data)
    tweets = []
    for e in doc.xpath("//div[contains(@class, 'original-tweet')]"):
        t = lxml.html.tostring(e)
        text = e.xpath(".//p[contains(@class, 'js-tweet-text')]")[0]
        html = lxml.html.tostring(text, encoding='unicode').strip()
        text = ox.decode_html(ox.strip_tags(html)).strip()
        user = re.compile('data-name="(.*?)"').findall(t)[0]
        user = ox.decode_html(ox.strip_tags(user)).strip()
        tweets.append({
            'id': re.compile('data-tweet-id="(\d+)"').findall(t)[0],
            'user-id': re.compile('data-user-id="(\d+)"').findall(t)[0],
            'name': re.compile('data-screen-name="(.*?)"').findall(t)[0],
            'time': datetime.fromtimestamp(int(re.compile('data-time="(\d+)"').findall(t)[0])),
            'user': user,
            'text': text,
            'html': html,
        })
    return tweets
