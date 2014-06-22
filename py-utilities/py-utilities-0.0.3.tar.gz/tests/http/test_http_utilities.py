#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mock import patch
from nose.tools import ok_
from py_utilities.http.http_utilities import get
import StringIO
import tempfile
import unittest


class MockResponse(object):
    def __init__(self, resp_data, code=200, msg='OK'):
        self.resp_data = resp_data
        self.has_returned_data = False
        self.code = code
        self.msg = msg
        self.headers = {'content-type': 'text/plain; charset=utf-8'}

    def read(self, length=0):
        if not self.has_returned_data:
            self.has_returned_data = True
            return self.resp_data.getvalue()
        else:
            return None

    def getcode(self):
        return self.code


class TestHttp(unittest.TestCase):

    def setUp(self):
        self.temp_file = tempfile.TemporaryFile()

    @patch('urllib2.urlopen')
    def test_get(self, urlopen_mock):
        output = StringIO.StringIO()
        output.write('twitter-google-facebook')
        urlopen_mock.return_value = MockResponse(output)
        get('http://www.google.com', self.temp_file)
        self.temp_file.seek(0)
        get_results = self.temp_file.read()
        ok_(get_results.find('google') >= 0)
        ok_(get_results.find('booyasfasf') == -1)

# vim: filetype=python
