import unittest

class TestIprestrictTweenFactory(unittest.TestCase):

    def _makeOne(self, **kw):
        from ..tweens import iprestrict_tween_factory
        return iprestrict_tween_factory(**kw)

    def _makeHandler(self):
        return lambda x: 'response'

    def _makeRegistry(self, ip_str):
        class DummyRegistry(object):
            def __init__(self, settings=None):
                self.settings = settings or {}
        return DummyRegistry({'iprestrict.allowed_ips': ip_str})

    def _makeRequest(self, remote_addr, xff=None):
        from pyramid.request import Request
        if xff is not None:
            return Request(environ={
                'REMOTE_ADDR': remote_addr,
                'HTTP_X_FORWARDED_FOR': xff,
            })
        return Request(environ={
            'REMOTE_ADDR': remote_addr,
        })

    def test_ip_restriction_disabled(self):
        handler = self._makeHandler()
        registry = self._makeRegistry(None)
        request = self._makeRequest('192.168.0.1')
        tween = self._makeOne(handler=handler, registry=registry)
        self.assertEqual(tween(request), 'response')

    def test_ip_address_allowed(self):
        handler = self._makeHandler()
        registry = self._makeRegistry('192.168.0.1')
        request = self._makeRequest('192.168.0.1')
        tween = self._makeOne(handler=handler, registry=registry)
        self.assertEqual(tween(request), 'response')

    def test_subnet_allowed(self):
        handler = self._makeHandler()
        registry = self._makeRegistry('192.168.0.0/24')
        request = self._makeRequest('192.168.0.1')
        tween = self._makeOne(handler=handler, registry=registry)
        self.assertEqual(tween(request), 'response')

    def test_multiple_ip_address_allowed(self):
        handler = self._makeHandler()
        registry = self._makeRegistry('127.0.0.1 192.168.0.0/24')
        request = self._makeRequest('127.0.0.1')
        tween = self._makeOne(handler=handler, registry=registry)
        self.assertEqual(tween(request), 'response')

    def test_ip_address_forbidden(self):
        from pyramid.httpexceptions import HTTPForbidden
        handler = self._makeHandler()
        registry = self._makeRegistry('192.168.0.1')
        request = self._makeRequest('127.0.0.1')
        tween = self._makeOne(handler=handler, registry=registry)
        self.assertTrue(isinstance(tween(request), HTTPForbidden))

    def test_subnet_forbidden(self):
        from pyramid.httpexceptions import HTTPForbidden
        handler = self._makeHandler()
        registry = self._makeRegistry('192.168.0.0/24')
        request = self._makeRequest('127.0.0.1')
        tween = self._makeOne(handler=handler, registry=registry)
        self.assertTrue(isinstance(tween(request), HTTPForbidden))

    def test_multiple_ip_address_forbidden(self):
        from pyramid.httpexceptions import HTTPForbidden
        handler = self._makeHandler()
        registry = self._makeRegistry('127.0.0.1 192.168.0.0/24')
        request = self._makeRequest('10.0.0.1')
        tween = self._makeOne(handler=handler, registry=registry)
        self.assertTrue(isinstance(tween(request), HTTPForbidden))

    def test_ip_restriction_disabled_with_xff(self):
        handler = self._makeHandler()
        registry = self._makeRegistry(None)
        request = self._makeRequest('127.0.0.1', '192.168.0.1')
        tween = self._makeOne(handler=handler, registry=registry)
        assert tween(request) == 'response'

    def test_xff_allowed(self):
        handler = self._makeHandler()
        registry = self._makeRegistry('192.168.0.0/24')
        request = self._makeRequest('127.0.0.1', '192.168.0.1')
        tween = self._makeOne(handler=handler, registry=registry)
        assert tween(request) == 'response'

    def test_multiple_ip_address_allowed_with_xff(self):
        handler = self._makeHandler()
        registry = self._makeRegistry('192.168.0.0/24 10.0.0.1')
        request = self._makeRequest('127.0.0.1', '192.168.0.1')
        tween = self._makeOne(handler=handler, registry=registry)
        assert tween(request) == 'response'

    def test_ip_address_forbidden_with_xff(self):
        from pyramid.httpexceptions import HTTPForbidden
        handler = self._makeHandler()
        registry = self._makeRegistry('127.0.0.1')
        request = self._makeRequest('192.168.0.1', '192.168.0.2')
        tween = self._makeOne(handler=handler, registry=registry)
        assert isinstance(tween(request), HTTPForbidden)

    def test_subnet_forbidden_with_xff(self):
        from pyramid.httpexceptions import HTTPForbidden
        handler = self._makeHandler()
        registry = self._makeRegistry('192.168.0.0/24')
        request = self._makeRequest('127.0.0.1', '10.0.0.1')
        tween = self._makeOne(handler=handler, registry=registry)
        assert isinstance(tween(request), HTTPForbidden)

    def test_multiple_ip_address_forbidden_with_xff(self):
        from pyramid.httpexceptions import HTTPForbidden
        handler = self._makeHandler()
        registry = self._makeRegistry('127.0.0.1 192.168.0.0/24')
        request = self._makeRequest('192.168.0.1', '10.0.0.1')
        tween = self._makeOne(handler=handler, registry=registry)
        assert isinstance(tween(request), HTTPForbidden)
