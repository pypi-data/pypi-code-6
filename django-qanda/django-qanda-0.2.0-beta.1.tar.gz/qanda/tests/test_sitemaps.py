from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from .common_data import PUBLISHED_PUBLIC_SLUGS
from qanda.sitemaps import QuestionSitemap

class TestSitemapTestCase(TestCase):

    fixtures = ['qanda_test.json']

    def test_question_sitemap(self):
        client = Client()
        response = self.client.get(reverse(
                'django.contrib.sitemaps.views.sitemap',
                ))
        # We need a 'good' response
        self.assertEqual(response.status_code, 200)
        #... and it should be XML
        self.assertEqual(response['Content-Type'], 'application/xml')

        # TODO: This should be a smarter check, maybe?
        got_slugs = QuestionSitemap().items().values_list('slug', flat=True)
        try:
            self.assertItemsEqual(PUBLISHED_PUBLIC_SLUGS, got_slugs)
        except AttributeError:
            self.assertEqual(sorted(PUBLISHED_PUBLIC_SLUGS), sorted(got_slugs))
