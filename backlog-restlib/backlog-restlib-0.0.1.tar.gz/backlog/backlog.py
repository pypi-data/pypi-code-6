# -*- coding: utf-8 -*-

from urlparse import urljoin

import requests

BACKLOG_API_V2_BASE_URL = 'https://{}.backlog.jp/api/v2/'


class Backlog(object):

    @classmethod
    def _create_session(cls, api_key):
        s = requests.Session()
        s.params.update({'apiKey': api_key})
        return s

    def __init__(self, space, api_key):
        self.session = self._create_session(api_key)
        self.base_url = BACKLOG_API_V2_BASE_URL.format(space)

    def __getattr__(self, name):
        return RestPathBuilder(self.base_url, name, self.session)


class RestPathBuilder(object):

    def fetch(self, name, **kwargs):
        url = urljoin(self.base_url, name)
        r = self.session.get(url, params=kwargs)
        r.raise_for_status()
        return r.json()

    def __init__(self, base_url, name, session):
        self.base_url = base_url
        self.path = name
        self.session = session

    def __call__(self, **kwargs):
        return self.fetch(self.path, params=kwargs)

    def __getitem__(self, item_name):
        return RestPathBuilder(self.base_url,
                         self.path + '/' + str(item_name), 
                         self.session)

    def __getattr__(self, name):
        return RestPathBuilder(self.base_url,
                         self.path + '/' + name,
                         self.session)
