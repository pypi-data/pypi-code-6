import logging
from unittest.case import TestCase

from django_request_logger import middleware, logger


class FakeUser(object):
    def __init__(self, username):
        self.username = username


class FakeRequest(object):
    def __init__(self, username, absolute_url, raw_post_data, meta):
        self.user = FakeUser(username)
        self.absolute_url = absolute_url
        self.raw_post_data = raw_post_data
        self.META = meta

    def build_absolute_uri(self):
        return self.absolute_url


class AddDjangoRequestFilterTest(TestCase):
    def test_no_request(self):
        filter = logger.AddDjangoRequestFilter()
        record = logging.LogRecord("name", 0, None, None, "msg", None, None)

        self.assertEqual(1, filter.filter(record))
        self.assertEqual("", record.username)
        self.assertEqual("", record.client_ip)
        self.assertEqual("", record.absolute_url)
        self.assertEqual("", record.raw_post_data)
        self.assertFalse(hasattr(record, 'data'))

    def test_with_request(self):
        filter = logger.AddDjangoRequestFilter()
        record = logging.LogRecord("name", 0, None, None, "msg", None, None)

        request = FakeRequest("testuser", "http://fake.url/test", "post=data", {'REMOTE_ADDR': "123.4.5.67"})
        middleware._set_request(request)

        self.assertEqual(1, filter.filter(record))
        self.assertEqual("testuser", record.username)
        self.assertEqual("123.4.5.67", record.client_ip)
        self.assertEqual("http://fake.url/test", record.absolute_url)
        self.assertEqual("post=data", record.raw_post_data)
        self.assertEqual("testuser", record.data['username'])
        self.assertEqual("123.4.5.67", record.data['client_ip'])
        self.assertEqual("http://fake.url/test", record.data['absolute_url'])
        self.assertEqual("post=data", record.data['raw_post_data'])

        request = FakeRequest("", "http://fake.url/test", None,
                {'REMOTE_ADDR': "1.2.3.4", 'HTTP_X_FORWARDED_FOR': "5.6.7.8"})
        request.user = None
        middleware._set_request(request)

        self.assertEqual(1, filter.filter(record))
        self.assertEqual("", record.username)
        self.assertEqual("1.2.3.4 [5.6.7.8]", record.client_ip)
        self.assertEqual("http://fake.url/test", record.absolute_url)
        self.assertEqual(None, record.raw_post_data)
