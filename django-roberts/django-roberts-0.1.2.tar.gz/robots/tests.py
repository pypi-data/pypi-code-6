from django.test import TestCase, Client
from django.core.urlresolvers import reverse

class RobotsTestCase(TestCase):
    def test_robots_view_works(self):
        client = Client()
        response = client.get(reverse('robots.views.robotstxt'))
        self.assertEqual(response.status_code, 200)
