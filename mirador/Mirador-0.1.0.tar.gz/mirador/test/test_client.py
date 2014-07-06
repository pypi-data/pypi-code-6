import unittest
from mirador.client import MiradorClient
from os import getenv as _genv
from os import path as _p

MIRADOR_API_KEY = _genv('MIRADOR_API_KEY')
__all__ = (
    'TestMiradorClient'
)


class TestMiradorClient(unittest.TestCase):

    def setUp(self):
        self.client = MiradorClient(
            MIRADOR_API_KEY
        )

    def test_classify_urls(self):
        "check that classification works both on server & client"

        results = self.client.classify_urls(
            'http://mirador.im/test/nsfw.jpg',
            'http://mirador.im/test/sfw.jpg'
        )

        self.assertEqual(len(results), 2)
        nsfw, sfw = results

        # check that the filenames were matched correctly
        self.assertEqual(nsfw.name, 'http://mirador.im/test/nsfw.jpg')
        self.assertEqual(sfw.name, 'http://mirador.im/test/sfw.jpg')

        # check that the classification was correct
        self.assertEqual(nsfw.safe, False)
        self.assertGreaterEqual(nsfw.value, 0.50)

        self.assertEqual(sfw.safe, True)
        self.assertLessEqual(sfw.value, 0.50)

    def test_classify_files(self):
        dirname = _p.dirname(__file__)

        nsfw_filename = _p.join(dirname, 'images/nsfw.jpg')
        sfw_filename = _p.join(dirname, 'images/sfw.jpg')

        test_file = open(sfw_filename, 'rb')

        # get the results from API
        results = self.client.classify_files(
            nsfw_filename, test_file)

        self.assertEqual(len(results), 2)
        nsfw, sfw = results

        self.assertEqual(nsfw.name, nsfw_filename)
        self.assertEqual(sfw.name, sfw_filename)

        # check that the results are correct
        self.assertEqual(nsfw.safe, False)
        self.assertGreaterEqual(nsfw.value, 0.50)

        self.assertEqual(sfw.safe, True)
        self.assertLessEqual(sfw.value, 0.50)


def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMiradorClient)
    return suite
