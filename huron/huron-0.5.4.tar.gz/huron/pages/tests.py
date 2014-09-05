from django.test import TestCase
from django.test.client import Client
from django.utils.safestring import SafeText
from huron.pages.models import Page
from huron.pages import get_page_by_slug

import datetime


class PageTestCase(TestCase):
    def setUp(self):
        today = datetime.datetime.now()
        next_week = today + datetime.timedelta(days=7)
        last_week = today - datetime.timedelta(days=7)
        Page.objects.create(title='Home', slug='home', content="<p>yes.</p>",
                            status='published')
        Page.objects.create(title='Draft', slug='draft',
                            content="<p>Draft.</p>")
        Page.objects.create(title='Futur', slug='futur',
                            content="<p>To the futur.</p>", status='published',
                            date_pub=next_week)
        Page.objects.create(title='Past', slug='past',
                            content="<p>Depreciate page.</p>",
                            status='published', date_unpub=last_week)

    def test_basic_manip(self):
        page = get_page_by_slug('home')
        draft = Page.objects.get(slug='draft')
        futur = Page.objects.get(slug='futur')
        past = Page.objects.get(slug='past')
        self.assertEqual(page.title, 'Home')
        self.assertEqual(page.is_published(), True)
        self.assertEqual(draft.is_published(), False)
        self.assertEqual(futur.is_published(), False)
        self.assertEqual(past.is_published(), False)
        self.assertEqual(type(page.see_online()), SafeText)

    def test_unpublished_page(self):
        c = Client()
        response = c.get('/pages/draft/')
        self.assertEqual(response.status_code, 404)

    def test_future_page(self):
        c = Client()
        response = c.get('/pages/futur/')
        self.assertEqual(response.status_code, 404)

    def test_published_page(self):
        c = Client()
        response = c.get('/pages/home/')
        self.assertEqual(response.status_code, 200)

    def test_str_settings(self):
        page = Page.objects.get(pk=1)
        self.assertEqual(str(page), 'Home')
