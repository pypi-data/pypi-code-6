from unittest import TestCase
from webnews import api
import os

class TestAPI(TestCase):

    def testSingleton(self):
        key = os.environ.get('WEBNEWS_API') if os.environ.get('WEBNEWS_API') != None else\
            open("private/apikey").read()
        a = api.API(key)
        b = api.API(key)
        self.assertTrue(a is b)

    def setUp(self):
        if os.environ.get('WEBNEWS_API') == None:
            self.api = api.API(open("private/apikey").read())
        else:
            self.api = api.API(os.environ['WEBNEWS_API'])

    def test_POST(self):
        #Tests handled by other methods
        pass

    def test_GET(self):
        #Tests handled by other methods
        pass

    def test_unread_counts(self):
        self.api.unread_counts()

    def test_newsgroups(self):
        self.api.newsgroups()

    def test_newsgroups_search(self):
        self.api.newsgroups_search('control.cancel')

    def test_search(self):
        self.api.search()

    def test_post_specifics(self):
        self.api.post_specifics("control.cancel", 3)

    def test_newsgroup_posts_noparam(self):
        self.api.newsgroup_posts('control.cancel', {})

    def test_newsgroup_posts_param(self):
        t = (self.api.newsgroup_posts('control.cancel', {'limit': 2}))
        self.assertTrue(len(t['posts_older']) == 2)
