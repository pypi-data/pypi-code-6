import unittest

from . import URL


class TestUrl(unittest.TestCase):

    def test_invalids_url(self):
        url = URL('http://google.com')
        self.assertEqual(url.url, 'http://google.com')

        with self.assertRaises(ValueError):
            url = URL('http://google.com.')

        with self.assertRaises(ValueError):
            url = URL('google.com.')

        with self.assertRaises(ValueError):
            url = URL('.google.com')



class TestBaseInspector(unittest.TestCase):
    pass
