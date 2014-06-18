#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sundowner Tests

Unit tests for Sundowner
"""
import sundowner
import unittest
try:
    import simplejson as json
except ImportError:
    import json
import urllib.parse

class SundownerTestCase(unittest.TestCase):

    def setUp(self):
        """Setup for testing"""
        sundowner.app.config['TESTING'] = True
        self.app = sundowner.app.test_client()

    def tearDown(self):
        pass

    def test_index(self):
        """Check the index page loads"""
        rv = self.app.get('/')
        assert '200 OK' in rv.status
        assert b'Sundowner' in rv.data

    # Test request data
    test_request_data = {
        'lat': -67.57,
        'lon': -68.13,
        'output_type': 'iso',
        'start': '2014-06-10T03:00:00.000Z',
        'end': '2014-06-10T03:00:00.000Z'
    }
    enc_request_data = urllib.parse.urlencode(test_request_data)

    def test_api_json(self):
        """Check a standard API request returns valid JSON"""
        rv = self.app.get('/api/sun/?{0}'.format(self.enc_request_data))
        try:
            jdata = json.loads(rv.data.decode('utf-8'))
        except ValueError:
            raise Exception('Invalid JSON response')
        events = jdata['days'][0]['events']
        assert '200 OK' in rv.status
        assert jdata['days'][0]['date'] == '2014-06-10'
        assert events['civil_dawn'] == '2014-06-10T13:35:54.968129+00:00'
        assert events['civil_dusk'] == '2014-06-10T19:27:46.806923+00:00'
        assert events['sunrise'] == '2014-06-10T15:57:56.853457+00:00'
        assert events['sunset'] == '2014-06-10T17:05:45.835109+00:00'

if __name__ == '__main__':
    unittest.main()
