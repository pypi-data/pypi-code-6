# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
from __future__ import print_function
import re
from six.moves.urllib.parse import quote

from ox import find_re, strip_tags, decode_html
from ox.cache import read_url

import lxml


def findISBN(title, author):
    q = '%s %s' % (title, author)
    url = "http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dstripbooks&field-keywords=" + "%s&x=0&y=0" % quote(q)
    data = read_url(url, unicode=True)
    links = re.compile('href="(http://www.amazon.com/.*?/dp/.*?)"').findall(data)
    id = find_re(re.compile('href="(http://www.amazon.com/.*?/dp/.*?)"').findall(data)[0], '/dp/(.*?)/')
    data = get_data(id)
    if author in data['authors']:
        return data
    return {}

def get_data(id):
    url = "http://www.amazon.com/title/dp/%s/" % id
    data = read_url(url, unicode=True)


    def find_data(key):
        return find_re(data, '<li><b>%s:</b>(.*?)</li>'% key).strip()

    r = {}
    r['amazon'] = url
    r['title'] = find_re(data, '<span id="productTitle" class="a-size-large">(.*?)</span>')
    r['authors'] = []
    doc = lxml.html.document_fromstring(data)
    for e in doc.xpath("//span[contains(@class, 'author')]"):
        print(e)
        for secondary in e.xpath(".//span[contains(@class, 'a-color-secondary')]"):
            if 'Author' in secondary.text:
                author = e.xpath(".//span[contains(@class, 'a-size-medium')]")
                if author:
                    r['authors'].append(author[0].text.strip())
                else:
                    r['authors'].append(e.xpath('.//a')[0].text.strip())
                break
            elif 'Translator' in secondary.text:
                r['translator'] = [e.xpath('.//a')[0].text]
                break
    r['publisher'] = find_data('Publisher')
    r['language'] = find_data('Language')
    r['isbn-10'] = find_data('ISBN-10')
    r['isbn-13'] = find_data('ISBN-13').replace('-', '')
    r['dimensions'] = find_re(data, '<li><b>.*?Product Dimensions:.*?</b>(.*?)</li>')

    r['pages'] = find_data('Paperback')
    if not r['pages']:
        r['pages'] = find_data('Hardcover')

    r['review'] = strip_tags(find_re(data, '<h3 class="productDescriptionSource">Review</h3>.*?<div class="productDescriptionWrapper">(.*?)</div>').replace('<br />', '\n')).strip()

    for e in doc.xpath('//noscript'):
        for c in e.getchildren():
            if c.tag == 'div':
                r['description'] = strip_tags(decode_html(lxml.html.tostring(c))).strip()
                break

    r['cover'] = re.findall('src="(.*?)" id="prodImage"', data)
    if r['cover']:
        r['cover'] = r['cover'][0].split('._BO2')[0]
        if not r['cover'].endswith('.jpg'):
            r['cover'] = r['cover'] + '.jpg'
        if 'no-image-avail-img' in r['cover']:
            del r['cover']
    else:
        del r['cover']
    return r

