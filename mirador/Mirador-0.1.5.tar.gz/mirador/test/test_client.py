import unittest
from mirador.client import MiradorClient
from os import getenv as _genv
from os import path as _p

MIRADOR_API_KEY = _genv('MIRADOR_API_KEY', 'demo69')
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
            'http://demo.mirador.im/test/nsfw.jpg',
            'http://demo.mirador.im/test/sfw.jpg'
        )

        self.assertEqual(len(results), 2)
        nsfw, sfw = results

        # check that the filenames were matched correctly
        self.assertEqual(nsfw.name, 'http://demo.mirador.im/test/nsfw.jpg')
        self.assertEqual(sfw.name, 'http://demo.mirador.im/test/sfw.jpg')

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
        self.assertIsNotNone(test_file)

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

    def _prepare_raw(self, filename):
        dirname = _p.dirname(__file__)

        with open(_p.join(dirname, filename), 'rb') as fh:
            return fh.read()

    def test_classify_raw(self):

        nsfw_raw = self._prepare_raw('images/nsfw.jpg')
        sfw_raw = self._prepare_raw('images/sfw.jpg')

        results = self.client.classify_raw(
            {
                'images/nsfw.jpg': nsfw_raw,
                'images/sfw.jpg': sfw_raw
            })

        nsfw, sfw = results

        self.assertEqual(nsfw.name, 'images/nsfw.jpg')
        self.assertEqual(sfw.name, 'images/sfw.jpg')

        self.assertEqual(nsfw.safe, False)
        self.assertEqual(sfw.safe, True)

        self.assertGreaterEqual(nsfw.value, 0.50)
        self.assertLess(sfw.value, 0.50)

    def test_chunked_urls(self):

        TLEN = 20

        nsfw_images = ['http://demo.mirador.im/test/nsfw.jpg'] * TLEN
        sfw_images = ['http://demo.mirador.im/test/sfw.jpg'] * TLEN

        results = self.client.classify_urls(*nsfw_images)
        self.assertEqual(len(results), TLEN)

        for r in results:
            self.assertEqual(r.name, 'http://demo.mirador.im/test/nsfw.jpg')
            self.assertGreaterEqual(r.value, 0.50)
            self.assertEqual(r.safe, False)

        results = self.client.classify_urls(*sfw_images)
        self.assertEqual(len(results), TLEN)

        for r in results:
            self.assertEqual(r.name, 'http://demo.mirador.im/test/sfw.jpg')
            self.assertLess(r.value, 0.50)
            self.assertEqual(r.safe, True)


def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMiradorClient)
    return suite

if __name__ == "__main__":
    unittest.main()
