# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
from .. import cache
from ..utils import json

def get_id(url):
    return url.split("/")[-1]

def get_url(id):
    return "http://www.archive.org/details/%s" % id

def get_data(id):
    data = {}
    url = get_url(id)
    details = cache.read_url('%s?output=json' % url)
    details = json.loads(details)
    for key in ('title', 'description', 'runtime'):
        data[key] = details['metadata'][key]
        if isinstance(data[key], list):
            data[key] = data[key][0]
    data['url'] = url
    data['image'] = 'http://archive.org/download/%s/format=thumbnail' % id
    data['ogg'] = 'http://archive.org/download/%s/format=Ogg+video' % id
    data['mp4'] = 'http://archive.org/download/%s/format=512Kb+MPEG4' % id
    return data

