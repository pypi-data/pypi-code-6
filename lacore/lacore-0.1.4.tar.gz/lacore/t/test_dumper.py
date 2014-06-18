import os
import httpretty

from . import makeprefs, _temp_home
from testtools import TestCase
from unittest import SkipTest
from mock import Mock, patch
from StringIO import StringIO
from urlparse import urlparse


class DumperTest(TestCase):
    def setUp(self):
        super(DumperTest, self).setUp()
        self.prefs = makeprefs()
        self.home = os.path.join('t', 'data')

    def tearDown(self):
        super(DumperTest, self).tearDown()

    @httpretty.activate
    @patch('sys.stdout', new_callable=StringIO)
    def test_dummy_dumper(self, out):
        try:
            import zipstream  # noqa
        except ImportError:
            raise SkipTest("requires python-zipstream")
        httpretty.register_uri(httpretty.GET, "http://foobar/",
                               body='file contents man',
                               content_type="text/plain")
        from lacore.dumper.urls import UrlDumper
        dest = UrlDumper(title='foo')
        cb = Mock()
        list(dest.dump([('http://foobar', 'rel')], cb))
        self.assertTrue('dummy writing' in out.getvalue())

    def test_dumper_no_archive(self):
        from lacore.dumper import Dumper

        class MyDumper(Dumper):
            def write(self, data):
                pass
        dump = MyDumper().dump([], None)
        self.assertRaises(NotImplementedError, list, dump)

    def test_dumper_file(self):
        from lacore.dumper.file import FileDumper
        from lacore.archive.folders import FolderArchiver

        class MyDumper(FileDumper, FolderArchiver):
            pass
        with _temp_home() as tmpdir:
            dest = MyDumper(tmpdir=tmpdir)
            list(dest.dump([os.path.abspath(self.home)], lambda x, y: None))
            self.assertTrue('links' in dest.docs)
            parsed = urlparse(dest.docs['links'].local)
            self.assertTrue(not parsed.scheme or parsed.scheme == 'file')
            self.assertTrue(os.path.exists(parsed.path))

    def test_dumper_file_zip(self):
        from lacore.dumper.file import FileDumper
        from lacore.archive.folders import FolderArchiver
        from lacore.adf.elements import Certificate, Archive, Meta, Cipher

        class MyDumper(FileDumper, FolderArchiver):
            pass
        with _temp_home() as tmpdir:
            docs = {}
            docs['archive'] = Archive(
                'foo', Meta('zip', Cipher('xor', 1)),
                description='bar')
            docs['cert'] = Certificate(key='\0'*8)
            dest = MyDumper(docs=docs, tmpdir=tmpdir)
            list(dest.dump([os.path.abspath(self.home)], lambda x, y: None))
            self.assertTrue('links' in dest.docs)
            parsed = urlparse(dest.docs['links'].local)
            self.assertTrue(not parsed.scheme or parsed.scheme == 'file')
            self.assertTrue(os.path.exists(parsed.path))
            import zipfile
            z = zipfile.ZipFile(parsed.path)
            z.testzip()
