import datetime
from django.test import TestCase, Client
from django.utils import timezone
from django.core.urlresolvers import reverse
from sitemapper.tests.models import Demo
from sitemapper.sitemaps import Sitemap


class SitemapBasic(Sitemap):
    queryset = Demo.objects.all()

    def lastmod(self, obj):
        return obj.modified


class SitemapWithDefaults(SitemapBasic):
    default_changefreq = 'weekly'
    default_priority = 0.5


expected_dicts = {

    'http://testserver/default-sitemap/': {
        'priority': '0.5',  # This is a default_priority
        'lastmod': datetime.datetime(
            2014, 10, 5, 16, 32, 19, 228000, tzinfo=timezone.utc
            ),
        'changefreq': 'weekly',  # This is a default_changefreq
        },

    'http://testserver/frequent-sitemap/': {
        'priority': '0.9',
        'lastmod': datetime.datetime(
            2014, 10, 5, 16, 31, 36, 60000, tzinfo=timezone.utc
            ),
        'changefreq': u'hourly',
        },

    'http://testserver/infrequent-sitemap/': {
        'priority': '0.1',
        'lastmod': datetime.datetime(
            2014, 10, 5, 16, 32, 3, 763000, tzinfo=timezone.utc
            ),
        'changefreq': u'yearly',
        }

    }


class SitemapTestCase(TestCase):

    fixtures = ['test.json']

    def setUp(self):
        self.client = Client()

    def test_response_basic(self):
        response = self.client.get(reverse(
            'sitemap.basic'
            ))
        self.assertEqual(response.status_code, 200)
        context = response.context['urlset']
        for got in context:
            expected = expected_dicts[got['location']]

            if got['item'].slug == 'default-sitemap':
                self.assertFalse(got['changefreq'])
                self.assertFalse(got['priority'])
                self.assertEqual(got['lastmod'], expected['lastmod'])
            else:
                for field in ('changefreq', 'lastmod', 'priority'):
                    self.assertEqual(got[field], expected[field])

    def test_response_withdefaults(self):
        response = self.client.get(reverse(
            'sitemap.with.defaults'
            ))
        self.assertEqual(response.status_code, 200)
        context = response.context['urlset']
        for got in context:
            expected = expected_dicts[got['location']]

            for field in ('changefreq', 'lastmod', 'priority'):
                self.assertEqual(got[field], expected[field])
