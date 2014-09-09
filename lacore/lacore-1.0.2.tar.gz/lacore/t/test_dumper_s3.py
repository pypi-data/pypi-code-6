import os
import httpretty

from . import makeprefs
from testtools import TestCase, ExpectedException
from unittest import SkipTest
from mock import Mock
from boto import connect_s3
from moto import mock_s3


class S3DumperTest(TestCase):
    @classmethod
    def setup_class(cls):
        cls._bucket = 'lastage2'

    def setUp(self):
        super(S3DumperTest, self).setUp()
        self.prefs = makeprefs()
        self.home = os.path.join('t', 'data', 'home')
        self.s3 = mock_s3()
        self.s3.start()
        boto = connect_s3()
        boto.create_bucket(self._bucket)

    def tearDown(self):
        self.s3.stop()
        super(S3DumperTest, self).tearDown()

    def test_s3_constructor(self):
        from lacore.dumper.s3 import S3Dumper
        from lacore.storage.s3 import S3Connection
        dest = S3Dumper()
        self.assertTrue(isinstance(dest.connection, S3Connection))

    def test_s3_constructor_min_chunk(self):
        from lacore.dumper.s3 import S3Dumper

        msg = "S3Dumper chunk must be at least 5242880"
        with ExpectedException(ValueError, msg):
            S3Dumper(chunk=123)

    def test_s3_constructor_with_connection(self):
        from lacore.dumper.s3 import S3Dumper
        mockc = Mock()
        dest = S3Dumper(connection=mockc)
        self.assertEqual(dest.connection, mockc)

    def test_s3_dumper(self):
        try:
            import zipstream  # noqa
        except ImportError:
            raise SkipTest("requires python-zipstream")
        httpretty.register_uri(httpretty.GET, "http://foobar/",
                               body='file contents man',
                               content_type="text/plain")
        from lacore.dumper.s3 import S3Dumper
        from lacore.storage.s3 import S3Connection
        c = S3Connection(bucket=self._bucket)
        dest = S3Dumper(key='baz', connection=c, title='foo')
        cb = Mock()
        list(dest.dump([('http://foobar', 'foobar')], cb))
        self.assertEqual(160, dest.docs['archive'].meta.size)
        from hashlib import md5
        m = md5()
        m.update(c.bucket.lookup('baz').get_contents_as_string())
        self.assertEqual(m.digest().encode('hex'),
                         dest.docs['auth'].md5.encode('hex'))

    def test_s3_stream_dumper(self):
        try:
            import zipstream  # noqa
        except ImportError:
            raise SkipTest("requires python-zipstream")
        httpretty.register_uri(httpretty.GET, "http://foobar/",
                               body='file contents man',
                               content_type="text/plain")
        from lacore.dumper.s3 import S3StreamDumper
        from lacore.storage.s3 import S3Connection
        from urllib2 import urlopen
        c = S3Connection(bucket=self._bucket)
        dest = S3StreamDumper(key='baz', connection=c, title='foo')
        cb = Mock()
        list(dest.dump([(urlopen('http://foobar'), 'foobar')], cb))
        self.assertEqual(160, dest.docs['archive'].meta.size)
        from hashlib import md5
        m = md5()
        m.update(c.bucket.lookup('baz').get_contents_as_string())
        self.assertEqual(m.digest().encode('hex'),
                         dest.docs['auth'].md5.encode('hex'))
