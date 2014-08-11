import unittest
from mirador.client import MiradorClient
from mirador.errors import MiradorException, UnauthorizedException
from os import getenv as _genv
from os import path as _p
from base64 import b64encode as b64

MIRADOR_API_KEY = _genv('MIRADOR_API_KEY', 'your_api_key')
__all__ = (
    'TestMiradorClient'
)


class TestMiradorClient(unittest.TestCase):

    def setUp(self):
        self.client = MiradorClient(
            MIRADOR_API_KEY
        )

        dirname = _p.dirname(__file__)

        self.nsfw_filename = _p.join(dirname, 'images/nsfw.jpg')
        self.sfw_filename = _p.join(dirname, 'images/sfw.jpg')

    def test_invalid_apikey(self):

        with self.assertRaises(UnauthorizedException):
            c = MiradorClient('invalid-key')
            c.classify_urls('http://static.mirador.im/test/nsfw.jpg')

    def test_http_request(self):

        mc = MiradorClient(MIRADOR_API_KEY, use_https=False)

        nsfw = mc.classify_url("http://static.mirador.im/test/nsfw.jpg")

        self.assertIsNotNone(nsfw)
        self.assertIsNotNone(nsfw)
        self.assertGreaterEqual(nsfw.value, 0.50)
        self.assertFalse(nsfw.safe)

    def test_bad_request(self):

        with self.assertRaises(MiradorException):
            self.client.classify_urls('http://torg.torf')

    def test_single_url(self):

        nsfw = self.client.classify_url(
            'http://static.mirador.im/test/nsfw.jpg'
        )

        self.assertIsNotNone(nsfw)
        self.assertGreaterEqual(nsfw.value, 0.50)
        self.assertFalse(nsfw.safe)

    def test_single_file(self):

        nsfw = self.client.classify_file(
            self.nsfw_filename
        )

        self.assertIsNotNone(nsfw)
        self.assertGreaterEqual(nsfw.value, 0.50)
        self.assertFalse(nsfw.safe)

    def test_single_buffer(self):

        with open(self.nsfw_filename) as nsfw_f:
            nsfw_buf = nsfw_f.read()

            nsfw = self.client.classify_buffer({"nsfw": nsfw_buf})
            self.assertIsNotNone(nsfw)
            self.assertGreaterEqual(nsfw.value, 0.50)
            self.assertFalse(nsfw.safe)

    def test_single_datauri(self):

        with open(self.nsfw_filename) as nsfw_f:
            nsfw_buf = nsfw_f.read()
            data_nsfw = 'data:image/jpg;base64,' + b64(nsfw_buf)

            nsfw = self.client.classify_data_uri({"nsfw": data_nsfw})

            self.assertIsNotNone(nsfw)
            self.assertGreaterEqual(nsfw.value, 0.50)
            self.assertFalse(nsfw.safe)

    def test_classify_urls(self):
        "check that classification works both on server & client"

        # our testing urls
        nsfw_url = 'http://demo.mirador.im/test/nsfw.jpg'
        sfw_url = 'http://demo.mirador.im/test/sfw.jpg'

        results = self.client.classify_urls(
            nsfw_url,
            sfw_url
        )

        self.assertEqual(len(results), 2)
        nsfw, sfw = results[nsfw_url], results[sfw_url]

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
        nsfw, sfw = results[nsfw_filename], results[sfw_filename]

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

        nsfw, sfw = results['images/nsfw.jpg'], results['images/sfw.jpg']

        self.assertEqual(nsfw.name, 'images/nsfw.jpg')
        self.assertEqual(sfw.name, 'images/sfw.jpg')

        self.assertEqual(nsfw.safe, False)
        self.assertEqual(sfw.safe, True)

        self.assertGreaterEqual(nsfw.value, 0.50)
        self.assertLess(sfw.value, 0.50)

    def test_chunked_urls(self):

        TLEN = 10

        nsfw_url = 'http://demo.mirador.im/test/nsfw.jpg'
        sfw_url = 'http://demo.mirador.im/test/sfw.jpg'

        # generate our tests
        nsfw_images = {}
        for i in xrange(TLEN):
            nsfw_images["{}_{}".format(i, nsfw_url)] = nsfw_url

        sfw_images = {}
        for i in xrange(TLEN):
            sfw_images["{}_{}".format(i, sfw_url)] = sfw_url

        results = self.client.classify_urls(nsfw_images)
        self.assertEqual(len(results), TLEN)

        for id, res in results:
            self.assertTrue((id in nsfw_images))
            self.assertGreaterEqual(res.value, 0.50)
            self.assertEqual(res.safe, False)

        # get the sfw ones
        results = self.client.classify_urls(sfw_images)
        self.assertEqual(len(results), TLEN)

        for id, res in results:
            self.assertTrue(id in sfw_images)
            self.assertLessEqual(res.value, 0.50)
            self.assertEqual(res.safe, True)


def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMiradorClient)
    return suite

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.WARN)

    unittest.main()
