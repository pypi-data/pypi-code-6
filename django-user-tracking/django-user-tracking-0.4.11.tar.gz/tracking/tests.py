
from django.test import TestCase, Client, override_settings
from tracking.models import Visitor


def _create_session(client):
    """
    Add a session to a test client.

    In Django 1.7 it is impossible to do:

    s = self.client.session
    s['foo'] = 'bar'
    s.save()

    This bug is explained and fixed in Django ticket #21357.
    See https://github.com/django/django/commit/
    be88b062afaa58559bb12623e8ed8843f07b97a1
    """
    from importlib import import_module
    from django.conf import settings
    SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
    s = SessionStore()
    s.save()
    client.cookies[settings.SESSION_COOKIE_NAME] = s.session_key
    return s


class VisitorMiddlewareTestCase(TestCase):

    def setUp(self):
        pass

    def test_ajax_call(self):
        """Ajax calls should be skipped."""
        client = Client()
        client.post('/ajax', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(Visitor.objects.count(), 0)

    def test_ip_address(self):
        """Test the ip address."""
        client = Client()
        client.post('/with_ip', REMOTE_ADDR='10.10.10.10')
        all_visitors = Visitor.objects.all()
        self.assertEqual(len(all_visitors), 1)
        self.assertEqual(all_visitors[0].ip_address, '10.10.10.10')

    def test_user_agent(self):
        """Test the user agent."""
        client = Client()
        client.post('/with_user_agent', HTTP_USER_AGENT='Some User Agent')
        all_visitors = Visitor.objects.all()
        self.assertEqual(len(all_visitors), 1)
        self.assertEqual(all_visitors[0].user_agent, 'Some User Agent')

    def test_without_session(self):
        """Test request without any session."""
        self.client = Client()
        self.client.post('/no_session', REMOTE_ADDR='10.10.10.10')
        all_visitors = Visitor.objects.all()
        self.assertEqual(len(all_visitors), 1)
        self.assertEqual(all_visitors[0].session_key, '10.10.10.10:')

    def test_without_session_but_with_a_user_agent(self):
        """Test request without any session but with a username."""
        self.client = Client()
        self.client.post('/no_session_but_user_name',
                         HTTP_USER_AGENT='FooBar',
                         REMOTE_ADDR='10.10.10.10')
        all_visitors = Visitor.objects.all()
        self.assertEqual(len(all_visitors), 1)
        self.assertEqual(all_visitors[0].session_key, '10.10.10.10:FooBar')

    def test_with_session(self):
        """Test request with a session instance."""
        self.client = Client()
        _create_session(self.client)
        session_key = self.client.session.session_key
        self.client.post('/hello', REMOTE_ADDR='10.10.10.10')
        all_visitors = Visitor.objects.all()
        self.assertEqual(len(all_visitors), 1)
        self.assertEqual(all_visitors[0].session_key, session_key)

    def test_with_no_tracking_prefix(self):
        """
        Make sure request to a path starting with NO_TRACKING_PREFIXES are
        skipped.
        """
        self.client = Client()
        from tracking import settings
        # this is very bad, but since override_settings did not seem to work...
        settings.NO_TRACKING_PREFIXES = ['/fizz', '/fuzz']
        self.client.post('/fizz', REMOTE_ADDR='10.10.10.10')
        self.client.post('/fuzz', REMOTE_ADDR='11.11.11.11')
        all_visitors = Visitor.objects.all()
        self.assertEqual(len(all_visitors), 0)

    def test_media_and_static_no_tracking_prefixes(self):
        """
        Make sure request to a path starting with a MEDIA_URL or STATIC_URL
        are skipped.
        """
        self.client = Client()
        from tracking import settings
        # this is very bad, but since override_settings did not seem to work...
        settings.ADMIN_URL = '/admin'
        settings.MEDIA_URL = '/media'
        self.client.post('/admin', REMOTE_ADDR='10.10.10.10')
        self.client.post('/media', REMOTE_ADDR='11.11.11.11')
        all_visitors = Visitor.objects.all()
        self.assertEqual(len(all_visitors), 0)

    def test_referer(self):
        """Test refer(r)er."""
        self.client = Client()
        _create_session(self.client)
        self.client.post('/hello', HTTP_REFERER='http://elevenbits.com')
        all_visitors = Visitor.objects.all()
        self.assertEqual(len(all_visitors), 1)
        self.assertEqual(all_visitors[0].referrer, 'http://elevenbits.com')

    def test_single_visitor_requests(self):
        """Test single visitor request."""
        self.client = Client()
        _create_session(self.client)
        self.client.post('/hello')
        all_visitors = Visitor.objects.all()
        self.assertEqual(len(all_visitors), 1)
        self.assertEqual(all_visitors[0].url, '/hello')
        self.assertEqual(all_visitors[0].referrer, 'unknown')
        self.assertEqual(all_visitors[0].page_views, 1)

    def test_multiple_visitor_requests(self):
        """Test several visitor requests."""
        self.client = Client()
        # first user
        self.client.post('/hello', REMOTE_ADDR='10.10.10.10')
        all_visitors = Visitor.objects.all()
        self.assertEqual(len(all_visitors), 1)
        session_start = all_visitors[0].session_start
        # second user
        self.client.post('/hello', REMOTE_ADDR='11.11.11.11')
        all_visitors = Visitor.objects.all()
        self.assertEqual(len(all_visitors), 2)
        # three new requests from first user
        self.client.post('/hello', REMOTE_ADDR='10.10.10.10')
        self.client.post('/hello', REMOTE_ADDR='10.10.10.10')
        self.client.post('/hello', REMOTE_ADDR='10.10.10.10')
        # assert
        all_visitors = Visitor.objects.all()
        self.assertEqual(len(all_visitors), 2)
        self.assertEqual(session_start, all_visitors[0].session_start)
