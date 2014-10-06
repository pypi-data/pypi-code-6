import datetime
from django.test import TestCase, Client
from django.utils import timezone
from django.core.urlresolvers import reverse
from sitemapper.tests.models import Demo
from sitemapper.mixins import Sitemap


class DummySitemap(Sitemap):
    default_changefreq = 'weekly'
    default_priority = 0.5
    queryset = Demo.objects.all()

    def lastmod(self, obj):
        return obj.modified


expected_dicts = {

    'http://testserver/default-sitemap/': {
        'priority': '0.5',
        'lastmod': datetime.datetime(
            2014, 10, 5, 16, 32, 19, 228000, tzinfo=timezone.utc
            ),
        'changefreq': 'weekly',
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

    def test_sitemap_response(self):
        response = self.client.get(reverse(
            'django.contrib.sitemaps.views.sitemap'
            ))
        self.assertEqual(response.status_code, 200)
        context = response.context['urlset']

        for got in context:
            expected = expected_dicts[got['location']]

            for field in ('changefreq', 'lastmod', 'priority'):
                self.assertEqual(expected[field], got[field])
