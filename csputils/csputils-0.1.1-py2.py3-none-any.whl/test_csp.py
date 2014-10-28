#pylint: disable=line-too-long

import unittest

from csputils import CSP

class Fixtures(object):
    one = {
        'str' : "default-src 'self'; object-src 'self' https://www.youtube.com; script-src 'self' 'unsafe-eval' https://*.twitter.com https://*.twimg.com https://ssl.google-analytics.com https://api-ssl.bitly.com; report-uri https://twitter.com/scribes/csp_report",

        'obj' : CSP({
            'default-src' : CSP.SELF,
            'object-src'  : [CSP.SELF, 'https://www.youtube.com'],
            'script-src'  : [CSP.SELF, CSP.UNSAFE_EVAL, 'https://*.twitter.com',
                             'https://*.twimg.com', 'https://ssl.google-analytics.com',
                             'https://api-ssl.bitly.com'],
            'report-uri'  : 'https://twitter.com/scribes/csp_report' })
    }

    two = {
        'str' : "allow 'self'; object-src 'self' https://www.youtube.com; options eval-script; script-src 'self' https://*.twitter.com https://*.twimg.com https://ssl.google-analytics.com https://api-ssl.bitly.com; report-uri /csp_report",

        'obj' : CSP({
            'allow'      : CSP.SELF,
            'options'    : 'eval-script',
            'object-src' : [CSP.SELF, 'https://www.youtube.com'],
            'script-src' : [CSP.SELF, 'https://*.twitter.com', 'https://*.twimg.com',
                            'https://ssl.google-analytics.com', 'https://api-ssl.bitly.com'],
            'report-uri' : '/csp_report'
            })
    }


    three = {
        'str' : "object-src 'self' https://www.youtube.com; script-src 'self' 'unsafe-eval' https://*.twitter.com https://*.twimg.com https://ssl.google-analytics.com https://graph.facebook.com https://api-read.facebook.com https://api-ssl.bitly.com; report-uri https://twitter.com/scribes/csp_report",

        'obj' : CSP({
            'object-src' : [CSP.SELF, 'https://www.youtube.com'],
            'script-src' : [CSP.SELF, CSP.UNSAFE_EVAL, 'https://*.twitter.com',
                            'https://*.twimg.com', 'https://ssl.google-analytics.com',
                            'https://graph.facebook.com', 'https://api-read.facebook.com',
                            'https://api-ssl.bitly.com'],
            'report-uri' : 'https://twitter.com/scribes/csp_report' })
    }


    four = {
        'str' : "object-src 'self' https://www.youtube.com; options eval-script; script-src 'self' https://*.twitter.com https://*.twimg.com https://ssl.google-analytics.com https://graph.facebook.com https://api-read.facebook.com https://api-ssl.bitly.com; report-uri /csp_report",

        'obj' : CSP({
                'options'    : 'eval-script',
                'object-src' : [CSP.SELF, 'https://www.youtube.com'],
                'script-src' : [CSP.SELF, 'https://*.twitter.com', 'https://*.twimg.com',
                                'https://ssl.google-analytics.com',
                                'https://graph.facebook.com', 'https://api-read.facebook.com',
                                'https://api-ssl.bitly.com'],
                'report-uri' :  '/csp_report' })
    }


class TestCSP(unittest.TestCase):

    def test_equivalence(self):

        for fixture in [ Fixtures.one, Fixtures.two, Fixtures.three, Fixtures.four ]:
            self.assertEqual(str(fixture['obj']), fixture['str'])

