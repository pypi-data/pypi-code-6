from unittest import TestCase
import os
from webnews import webnews
from webnews import api

class TestWebnewsObject(TestCase):
    def test___init__(self):
        t = webnews.WebnewsObject('asdfasdf')
        self.assertTrue(type(t._api) == api.APINonSingle)
        apiobj = t._api
        a = webnews.WebnewsObject(apiobj)
        self.assertTrue(type(a._api) == api.APINonSingle)

    def test_populate(self):
        b = webnews.WebnewsObject('asdf')
        d = {'a': 5, 'b': 'a'}
        b.populate(d)
        self.assertTrue(hasattr(b, 'a'))
        self.assertTrue(hasattr(b, 'b'))
        self.assertTrue(b.a == 5)
        self.assertTrue(b.b == 'a')

    def setUp(self):
        if os.environ.get('WEBNEWS_API') == None:
            self.api = api.API(open("private/apikey").read())
        else:
            self.api = api.API(os.environ['WEBNEWS_API'])

class TestNewsgroupObject(TestCase):
    def test___init__(self):
        w = webnews.Newsgroup(self.api.api_key, 'control.cancel')
        self.assertTrue(type(w._api) == api.APINonSingle)

    def test_list(self):
        w = webnews.Newsgroup(self.api.api_key, 'control.cancel')
        for i in w.list():
            pass


    def test_list_paginate_nodup(self):
        w = webnews.Newsgroup(self.api.api_key, 'control.cancel')
        a,b,c,d = w.list(limit=4,callLimit=2)
        self.assertTrue(a['post']['date'] != c['post']['date'])
        self.assertTrue(b['post']['date'] != d['post']['date'])

    def test_list_limit(self):
        w = webnews.Newsgroup(self.api.api_key, 'control.cancel')
        count = 0
        LIM = 2
        for i in w.list(limit=LIM):
            count += 1
        self.assertTrue(LIM == count)

    def setUp(self):
        if os.environ.get('WEBNEWS_API') == None:
            self.api = api.API(open("private/apikey").read())
        else:
            self.api = api.API(os.environ['WEBNEWS_API'])
