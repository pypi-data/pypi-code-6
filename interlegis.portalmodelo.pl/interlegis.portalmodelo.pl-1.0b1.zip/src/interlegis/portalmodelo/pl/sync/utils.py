# -*- coding: utf-8 -*-
from datetime import date
from interlegis.portalmodelo.pl.config import PROJECTNAME
from plone.namedfile.file import NamedBlobImage
from urllib2 import Request
from urllib2 import URLError
from urllib2 import urlopen

import logging

HDR = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) (KHTML, like Gecko) Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'
}

log = logging.getLogger(PROJECTNAME)


def date_from_json(value):
    """ Convert iso 8601 format to python date object
    """
    if not value:
        return None
    # Date should be formated as 2013-10-17
    value = [int(p) for p in value.split('-')]
    return date(*value)


def get_remote_data(url):
    data = None
    req = Request(url, headers=HDR)
    try:
        fh = urlopen(req)
    except (URLError, ValueError):
        log.info('Unable to acces %s' % (url))
        return (data, None)
    data = fh.read()
    content_type = fh.headers['content-type']
    return (data, content_type)


def get_image(url):
    """ Get an image at the given url and return a NamedBlobImage
        or None
    """
    value = None
    if url:
        data, content_type = get_remote_data(url)
        if data:
            filename = u'image.%s' % (content_type.split('/')[1])
            value = NamedBlobImage(data, content_type, filename)
    return value


def adjust_types(item):
    """ Adjust an item data types
    """
    dates = ['start_date', 'end_date', 'birthday', 'date_affiliation', 'date_disaffiliation']
    images = ['image', ]
    for field in item.keys():
        if field in dates:
            item[field] = date_from_json(item[field])
        if field in images:
            item[field] = get_image(item[field])

    return item
