
from django.test import TestCase, RequestFactory
from django.test.utils import override_settings

from rated.middleware import RatedMiddleware

@override_settings(
    REALM_MAP = {'sample': {}},
)
class MiddlewareTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.m = RatedMiddleware()

    def test_not_in_realm(self):
        request = self.factory.get('/')

        def dummy_view(request):
            return ''

        self.assertTrue(self.m.process_view(request, dummy_view, (), {}) is dummy_view)

