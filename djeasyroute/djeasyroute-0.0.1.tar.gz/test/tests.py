import unittest

from django.test.utils import setup_test_environment
from djeasyroute import EasyRoute, route
from django.conf import settings
from django.core.urlresolvers import reverse, NoReverseMatch
from django.conf.urls import patterns, include

settings.configure(USE_I18N=False, SECRET_KEY="MERP")

class URLPatterns(object):
    def __init__(self, urls):
        self.urlpatterns = patterns('',
            (r'^test/', include(urls)),
        )

class RouteTests(unittest.TestCase):
    def setUp(self):
        setup_test_environment()

    def test_single_route(self):
        class SingleRoute(EasyRoute):
            @route('testing')
            def testing(self):
                pass

        r = SingleRoute()
        self.assertEqual(len(r.urls), 1)

    def test_multi_route(self):
        class MultiRoute(EasyRoute):
            @route('testing1')
            @route('testing2')
            def testing(self):
                pass

        r = MultiRoute()
        self.assertEqual(len(r.urls), 2)

    def test_int_route(self):
        class IntRoute(EasyRoute):
            @route('<value:int>', name="takesInt")
            def takesInt(value):
                print value

        r = IntRoute()

        urls = URLPatterns(r.urls)

        rev = reverse('takesInt', urls, kwargs={'value': 1})
        rev = reverse('takesInt', urls, kwargs={'value': '1'})

        with self.assertRaises(NoReverseMatch):
            rev = reverse('takesInt', urls, kwargs={'value': 'string'})

    def test_float_route(self):
        class FloatRoute(EasyRoute):
            @route('<value:float>', name="takesFloat")
            def takesFloat(value):
                print value

        r = FloatRoute()

        urls = URLPatterns(r.urls)

        rev = reverse('takesFloat', urls, kwargs={'value': 1.5})
        rev = reverse('takesFloat', urls, kwargs={'value': '1.5'})
        rev = reverse('takesFloat', urls, kwargs={'value': '100'})

        with self.assertRaises(NoReverseMatch):
            rev = reverse('takesFloat', urls, kwargs={'value': 'string'})

    def test_bool_route(self):
        class BoolRoute(EasyRoute):
            @route('<value:bool>', name="takesBool")
            def takesBool(value):
                print value

        r = BoolRoute()

        urls = URLPatterns(r.urls)

        rev = reverse('takesBool', urls, kwargs={'value': 'false'})
        rev = reverse('takesBool', urls, kwargs={'value': 'true'})
        rev = reverse('takesBool', urls, kwargs={'value': 't'})
        rev = reverse('takesBool', urls, kwargs={'value': 'f'})

