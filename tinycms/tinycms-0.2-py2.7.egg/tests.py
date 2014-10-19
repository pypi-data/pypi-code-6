from django.test import TestCase
from django.test.client import Client

from models import *

import datetime

class ModellTest(TestCase):
    def setUp(self):
        self.c512 =""
        for i in range(0,511):
            self.c512 += "a"


    def test_model_normal(self):
        testDispatch={}

        page = Page(slug="test",template="tinycms/shelltest.html",is_active=True)
        page.save()
        page2 = Page(slug="test2",template="tinycms/shelltest.html",parent=page,is_active=True)
        page2.save()

        testDispatch[u'test/']=page
        testDispatch[u'test/test2/']=page2

        with self.assertRaises(Exception):
            page = Page(slug="test",template="tinycms/shelltest.html",is_active=True)
            page.save()

        page = Page(slug=self.c512,template="tinycms/shelltest.html",is_active=True)
        page.save()
        testDispatch[unicode(self.c512+"/")]=page

        cont = Content(page=page,value_name="main",language="ja",content="test")
        cont.save()

        Dispatcher.register()
        self.assertEqual(Dispatcher.dispatchURLs,testDispatch)#,"Invalid dispatch url\n"+str(Dispatcher.dispatchURLs))


class DummyRequest:
    def __init__(self,user=None,GET={}):
        self.user=user
        self.GET=GET
        self.POST={}
        self.method="GET"

class ViewTest(TestCase):
    def setUp(self):
        pass

    def test_content(self):
        Dispatcher.clear()
        page = Page(slug="test",template="tinycms/shelltest.html",is_active=True)
        page.save()
        page2 = Page(slug="test2",template="tinycms/shelltest.html",parent=page,is_active=True)
        page2.save()
        cont = Content(page=page,value_name="main",language="ja",content="test")
        cont.save()
        cont = Content(page=page,value_name="main",language="en-us",content="test")
        cont.save()

        req = DummyRequest()
        from views import *
        result = show_page(req,"test/")
        candResult = '<html><body><p>test</p></body></html>'
        self.assertEqual(result.content,candResult)

        with self.assertRaises(Exception):
            result = show_page(req,"test2/")

    def test_menu(self):
        Dispatcher.clear()
        page = Page(slug="test",template="tinycms/menutest.html",is_active=True)
        page.save()
        page2 = Page(slug="test2",template="tinycms/menutest.html",parent=page,is_active=True)
        page2.save()
        cont = Content(page=page,value_name="main",language="ja",content="test")
        cont.save()
        cont = Content(page=page,value_name="main",language="en-us",content="test")
        cont.save()
        cont = Content(page=page,value_name="menu_title",language="en-us",content="test")
        cont.save()
        cont = Content(page=page2,value_name="menu_title",language="en-us",content="test2")
        cont.save()

        req = DummyRequest()
        from views import *
        result = show_page(req,"test/")
        candResult = "<html><body><ul><li><a href='/en-us/test/'>test</a><ul><li><a href='/en-us/test/test2/'>test2</a></li></ul></li></ul><p>test</p></body></html>"
        self.assertEqual(result.content,candResult)


