from testtools import TestCase
from mock import patch, Mock
from . import makeprefs


class ApiHttpTest(TestCase):
    def setUp(self):
        super(ApiHttpTest, self).setUp()
        self.prefs = makeprefs()['api']

    def _makeit(self):
        from lacore.api import RequestsFactory
        return RequestsFactory

    @patch('lacore.api.Api')
    def test_request_factory_no_prefs(self, api):
        factory = self._makeit()
        s = self.getUniqueString()
        self.patch(factory, 'TwistedRequestsSession',
                   Mock(return_value=s))
        factory()
        api.assert_called_with({}, s)

    @patch('lacore.api.Api')
    def test_request_factory(self, api):
        factory = self._makeit()
        s = self.getUniqueString()
        self.patch(factory, 'TwistedRequestsSession',
                   Mock(return_value=s))
        p = {self.getUniqueString(): self.getUniqueString()}
        factory(prefs=p)
        api.assert_called_with(p, s)

    @patch('lacore.api.Api')
    def test_request_factory_verify(self, api):
        factory = self._makeit()
        s = self.getUniqueString()
        rs = Mock(return_value=s)
        self.patch(factory, 'TwistedRequestsSession', rs)
        p = {'verify': self.getUniqueString()}
        factory(prefs=p)
        self.assertEqual(1, len(rs.call_args[0]))
        sobj = rs.call_args[0][0]
        self.assertTrue(hasattr(sobj, 'verify'))
        self.assertEqual(sobj.verify, p['verify'])

    @patch('lacore.api.Api')
    def test_request_factory_auth(self, api):
        factory = self._makeit()
        s = self.getUniqueString()
        rs = Mock(return_value=s)
        self.patch(factory, 'TwistedRequestsSession', rs)
        p = {
            'user': self.getUniqueString(),
            'pass': self.getUniqueString()
        }
        factory(prefs=p)
        self.assertEqual(1, len(rs.call_args[0]))
        sobj = rs.call_args[0][0]
        self.assertTrue(hasattr(sobj, 'auth'))
        self.assertEqual(sobj.auth, (p['user'], p['pass']))

    @patch('lacore.api.Api')
    def test_request_factory_useragent(self, api):
        factory = self._makeit()
        s = self.getUniqueString()
        rs = Mock(return_value=s)
        self.patch(factory, 'TwistedRequestsSession', rs)
        p = {'user_agent': self.getUniqueString()}
        factory(prefs=p)
        self.assertEqual(1, len(rs.call_args[0]))
        sobj = rs.call_args[0][0]
        self.assertTrue(hasattr(sobj, 'user_agent'))
        self.assertEqual(sobj.user_agent, p['user_agent'])

    @patch('lacore.api.Api')
    def test_request_factory_session(self, api):
        factory = self._makeit()
        factory()
        args, _ = api.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(args[0], {})
        self.assertTrue(hasattr(args[1], 'get'))
        self.assertTrue(hasattr(args[1], 'post'))
        self.assertTrue(hasattr(args[1], 'patch'))
