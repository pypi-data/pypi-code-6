# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import json

from ox.cache import read_url
from ox import find_re

class Freebase(dict):
    def __init__(self, id, timeout=-1):
        url = "http://ids.freebaseapps.com/get_ids?id=/authority/imdb/title/tt%s" % id
        '''
            "http://graph.freebase.com/imdb.title.tt%s" % id
            might also be of interest at some point, right now not much info
        '''
        data = read_url(url, unicode=True)
        try:
            data = json.loads(data)
        except ValueError:
            return
        '''
        for key in data:
            self[key] = data[key]
        '''
        for key in ('id', 'guid', 'name'):
            self[key] = data[key]
        keys = {
            'wikipedia': '/wikipedia/en',
            'netflix': '/authority/netflix/movie',
            'nytimes': '/source/nytimes/movie',
            'metacritic': '/source/metacritic/movie',
        }
        for key in keys:
            links = filter(lambda x: x['namespace'] == keys[key],data['ids'])
            if links:
                self[key] = links[0]['uri']

        if 'nytimes' in self:
            self['nytimes'] = self['nytimes'].replace('_/overview', '%s/overview' % self['name'].replace(' ', '-'))
            self['amgId'] = find_re(self['nytimes'], 'movie/(\d+)/')



