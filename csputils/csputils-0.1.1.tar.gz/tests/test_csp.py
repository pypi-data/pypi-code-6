#pylint: disable=line-too-long

import unittest

from csputils import CSP

class Fixtures(object):
    one = (
        "default-src 'self'; object-src 'self' https://www.youtube.com; script-src 'self' 'unsafe-eval' https://*.twitter.com https://*.twimg.com https://ssl.google-analytics.com https://api-ssl.bitly.com; report-uri https://twitter.com/scribes/csp_report",
        CSP({
            'default-src' : CSP.SELF,
            'object-src'  : [CSP.SELF, 'https://www.youtube.com'],
            'script-src'  : [CSP.SELF, CSP.UNSAFE_EVAL, 'https://*.twitter.com',
                             'https://*.twimg.com', 'https://ssl.google-analytics.com',
                             'https://api-ssl.bitly.com'],
            'report-uri'  : 'https://twitter.com/scribes/csp_report' })
    )

    two = (
        "allow 'self'; object-src 'self' https://www.youtube.com; script-src 'self' https://*.twitter.com https://*.twimg.com https://ssl.google-analytics.com https://api-ssl.bitly.com; report-uri /csp_report",
        CSP({
            'allow'      : CSP.SELF,
            'object-src' : [CSP.SELF, 'https://www.youtube.com'],
            'script-src' : [CSP.SELF, 'https://*.twitter.com', 'https://*.twimg.com',
                            'https://ssl.google-analytics.com', 'https://api-ssl.bitly.com'],
            'report-uri' : '/csp_report' })
    )


    three = (
        "object-src 'self' https://www.youtube.com; script-src 'self' 'unsafe-eval' https://*.twitter.com https://*.twimg.com https://ssl.google-analytics.com https://graph.facebook.com https://api-read.facebook.com https://api-ssl.bitly.com; report-uri https://twitter.com/scribes/csp_report",
        CSP({
            'object-src' : [CSP.SELF, 'https://www.youtube.com'],
            'script-src' : [CSP.SELF, CSP.UNSAFE_EVAL, 'https://*.twitter.com',
                            'https://*.twimg.com', 'https://ssl.google-analytics.com',
                            'https://graph.facebook.com', 'https://api-read.facebook.com',
                            'https://api-ssl.bitly.com'],
            'report-uri' : 'https://twitter.com/scribes/csp_report' })
    )


    four = (
        "object-src 'self' https://www.youtube.com; script-src 'self' https://*.twitter.com https://*.twimg.com https://ssl.google-analytics.com https://graph.facebook.com https://api-read.facebook.com https://api-ssl.bitly.com; report-uri /csp_report",

        CSP({
                'object-src' : [CSP.SELF, 'https://www.youtube.com'],
                'script-src' : [CSP.SELF, 'https://*.twitter.com', 'https://*.twimg.com',
                                'https://ssl.google-analytics.com',
                                'https://graph.facebook.com', 'https://api-read.facebook.com',
                                'https://api-ssl.bitly.com'],
                'report-uri' :  '/csp_report' })
    )


class TestCSP(unittest.TestCase):

    def test_equivalence(self):
        for fixture_str, fixture_obj in [ Fixtures.one, Fixtures.two, Fixtures.three, Fixtures.four ]:
            self.assertEqual(str(fixture_obj), fixture_str)

    def test_bidirectional_conversion(self):
        for fixture_str, fixture_obj in [ Fixtures.one, Fixtures.two, Fixtures.three, Fixtures.four ]:
            self.assertEqual(fixture_obj, CSP.from_string(fixture_str))

    def test_validates_quoted_reserved_expressions(self):
        for exp in CSP.unquoted_reserved_source_expressions:
            self.assertRaises(ValueError, CSP._validate_source_list, [exp])

        for exp in CSP.quoted_reserved_source_expressions:
            CSP._validate_source_list([exp])


class TestSorting(unittest.TestCase):
    ONE = (
        "default-src 'self'; script-src 'self' 'unsafe-eval' https://*.twitter.com https://*.twimg.com https://ssl.google-analytics.com https://api-ssl.bitly.com; object-src 'self' https://www.youtube.com; report-uri https://twitter.com/scribes/csp_report",
        "default-src 'self'; object-src 'self' https://www.youtube.com; script-src 'self' 'unsafe-eval' https://*.twitter.com https://*.twimg.com https://ssl.google-analytics.com https://api-ssl.bitly.com; report-uri https://twitter.com/scribes/csp_report")

    TWO = (
        "allow 'self'; script-src 'self' https://*.twitter.com https://*.twimg.com https://ssl.google-analytics.com https://api-ssl.bitly.com; object-src 'self' https://www.youtube.com; report-uri /csp_report",
        "allow 'self'; object-src 'self' https://www.youtube.com; script-src 'self' https://*.twitter.com https://*.twimg.com https://ssl.google-analytics.com https://api-ssl.bitly.com; report-uri /csp_report")

    THREE = (
        "script-src 'self' 'unsafe-eval' https://*.twitter.com https://*.twimg.com https://ssl.google-analytics.com https://graph.facebook.com https://api-read.facebook.com https://api-ssl.bitly.com; object-src 'self' https://www.youtube.com; report-uri https://twitter.com/scribes/csp_report",
        "object-src 'self' https://www.youtube.com; script-src 'self' 'unsafe-eval' https://*.twitter.com https://*.twimg.com https://ssl.google-analytics.com https://graph.facebook.com https://api-read.facebook.com https://api-ssl.bitly.com; report-uri https://twitter.com/scribes/csp_report")

    FOUR = (
        "script-src 'self' https://*.twitter.com https://*.twimg.com https://ssl.google-analytics.com https://graph.facebook.com https://api-read.facebook.com https://api-ssl.bitly.com; object-src 'self' https://www.youtube.com; report-uri /csp_report",
        "object-src 'self' https://www.youtube.com; script-src 'self' https://*.twitter.com https://*.twimg.com https://ssl.google-analytics.com https://graph.facebook.com https://api-read.facebook.com https://api-ssl.bitly.com; report-uri /csp_report")

    def test_sorting(self):
        for p1, p2 in [ self.ONE, self.TWO, self.THREE, self.FOUR ]:
            self.assertEqual(str(CSP.from_string(p1)), str(CSP.from_string(p2)))

if __name__ == '__main__':
    unittest.main()
