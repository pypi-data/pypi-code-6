"""Cobertura aggregator tests"""
import os
import unittest
import urllib2
from mock import patch, MagicMock
from base import CoberturaJSONAggregator

API_SETTINGS = {
    CoberturaJSONAggregator.USERNAME_KEY: "test",
    CoberturaJSONAggregator.API_TOKEN_KEY: "test",
    CoberturaJSONAggregator.DOMAIN_KEY: "http://localhost",
    CoberturaJSONAggregator.JOBS_KEY: ["test"],
    CoberturaJSONAggregator.TARGETS_KEY: [
        'club',
        'cron',
    ],
}


class CoberturaJSONAggregatorTests(unittest.TestCase):
    """Test cases for aggregating Cobertura JSON via Jenkins REST API"""
    def setUp(self):
        self.test_name = 'test'
        self.aggregator = CoberturaJSONAggregator(self.test_name, API_SETTINGS)
        fixture_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'fixtures/cobertura.json'
        )
        with open(fixture_path) as fixture_file:
            self._cobertura_json = fixture_file.read()

    @patch('base.urllib2.urlopen')
    def test_report_generator(self, urlopen_mock):
        urlopen_mock().read.return_value = self._cobertura_json
        self.aggregator.generate_report()
        expected_result = [
            ['club', '67.50%', '62.50%'],
            ['cron', '8.15%', '6.25%']
        ]
        self.assertEqual(self.aggregator._report, expected_result)

    @patch('base.urllib2.urlopen')
    @patch('base.LOGGER')
    def test_http_error(self, logger_mock, urlopen_mock):
        """Test urllib2.HTTPError exceptions"""
        log = []
        logger_mock.error.side_effect = log.append
        logger_mock.info.side_effect = log.append

        urlopen_mock.side_effect = urllib2.HTTPError(
            "test",
            404,
            "test",
            {},
            MagicMock()
        )
        self.aggregator.generate_report()
        http_error_results = [
            'http://localhost/job/test/lastSuccessfulBuild/cobertura/api/json?depth=4\nHTTP error: HTTP Error 404: test'
        ]
        self.assertEqual(log, http_error_results)

    @patch('base.urllib2.urlopen')
    @patch('base.LOGGER')
    def test_url_error(self, logger_mock, urlopen_mock):
        """Test urllib2.URLError exceptions"""
        log = []
        logger_mock.error.side_effect = log.append
        logger_mock.info.side_effect = log.append

        urlerror_results = [
            'http://localhost/job/test/lastSuccessfulBuild/cobertura/api/json?depth=4\nURL error: URL Error'
        ]
        urlopen_mock.side_effect = urllib2.URLError("URL Error")
        self.aggregator.generate_report()
        self.assertEqual(log, urlerror_results)

    @patch('base.urllib2.urlopen')
    @patch('base.LOGGER')
    def test_simplejson_error(self, logger_mock, urlopen_mock):
        """Test simplejson.loads error"""
        log = []
        logger_mock.error.side_effect = log.append
        logger_mock.info.side_effect = log.append

        urlopen_mock().read.return_value = '{'
        self.aggregator.generate_report()
        simplejson_error = [
            "{\nCobertura URL did not return valid json: Expecting property name enclosed in double quotes or '}': line 1 column 2 (char 1)"
        ]
        self.assertEqual(log, simplejson_error)
