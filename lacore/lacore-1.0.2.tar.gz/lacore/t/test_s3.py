import pickle

from testtools import TestCase, ExpectedException
from moto import mock_s3
from mock import patch, Mock
import boto


class S3ConnectionTest(TestCase):
    @classmethod
    def setup_class(cls):
        cls._token = {
            'token_access_key': '',
            'token_secret_key': '',
            'token_session': '',
            'token_expiration': '',
            'bucket': 'lastage',
            'prefix': 'upload/14/',
        }

    def setUp(self):
        self.s3 = mock_s3()
        self.s3.start()
        boto.connect_s3().create_bucket(self._token['bucket'])

        super(S3ConnectionTest, self).setUp()

    def tearDown(self):
        self.s3.stop()
        super(S3ConnectionTest, self).tearDown()

    def _makeit(self, *args, **kw):
        from lacore.storage.s3 import S3Connection
        return S3Connection(*args,  **kw)

    def test_s3connection(self):
        assert self._makeit(**self._token)

    def test_getconnection(self):
        conn = self._makeit(**self._token)
        assert conn.getconnection()

    def test_getbucket(self):
        conn = self._makeit(**self._token)
        self.assertEqual(conn.bucket.name, self._token['bucket'])

    @patch('lacore.storage.s3.connect_s3')
    def test_getbucket_exc(self, mc):
        from boto.exception import S3ResponseError
        mc.return_value.get_bucket.side_effect = S3ResponseError(
            '401', 'FooError', '')
        conn = self._makeit(**self._token)
        with ExpectedException(S3ResponseError,
                               "S3ResponseError: 401 FooError"):
            print conn.bucket

    def test_getbucket_404(self):
        from boto.exception import S3ResponseError
        tok = {}
        tok.update(self._token)
        tok['bucket'] = 'nosuchbucket'
        conn = self._makeit(**tok)
        with ExpectedException(S3ResponseError,
                               "S3ResponseError: 404 Not Found"):
            print conn.bucket

    def test_newkey(self):
        conn = self._makeit(**self._token)
        key = conn.newkey('foobar')
        self.assertEqual(conn.bucket.name, key.bucket.name)
        self.assertEqual('upload/14/foobar', key.name)

    def test_pickle(self):
        conn = self._makeit(**self._token)
        conn.getconnection()
        self.assertTrue(conn.conn is not None)
        conn = pickle.loads(pickle.dumps(conn))
        self.assertTrue(conn.conn is None)

    def test_multipart_upload(self):
        conn = self._makeit(**self._token)
        u = conn.newupload('foo')
        u2 = conn.getupload(u.id)
        self.assertEqual(u.id, u2.id)
        self.assertEqual(u.key_name, u2.key_name)
        self.assertTrue(conn.getupload('lala') is None)

    @patch.object(boto.s3.bucket.Bucket, 'complete_multipart_upload')
    def test_complete_multipart(self, mock_cu):
        conn = self._makeit(**self._token)
        u = conn.newupload('foo')
        mock_cu.return_value = Mock(etag='foo')
        from lacore.exceptions import UploadInvalidError
        with ExpectedException(UploadInvalidError):
            conn.complete_multipart(u, ['abcd'])
