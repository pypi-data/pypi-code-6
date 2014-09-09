# -*- coding: utf-8 -*-
import os
import sys
import operator
import zipfile
import httpretty

from testtools import TestCase
from unittest import SkipTest
from . import makeprefs, _temp_home
from tempfile import NamedTemporaryFile
from mock import MagicMock, Mock, patch
from itertools import islice, izip, count


class ArchiveTest(TestCase):
    def setUp(self):
        super(ArchiveTest, self).setUp()
        self.prefs = makeprefs()
        self.data = os.path.join('t', 'data')

    def tearDown(self):
        super(ArchiveTest, self).tearDown()

    def test_restore(self):
        from lacore.archive import restore_archive
        from lacore.adf.persist import load_archive
        with _temp_home() as tmpdir:
            cb = Mock()
            cfname = os.path.join(
                self.data, '2013-10-22-foobar.zip.crypt')
            with open(os.path.join(self.data,
                                   'certs',
                                   '2013-10-13-foobar.adf')) as cf:
                cert = load_archive(cf)
            restore_archive(
                cert['archive'], cfname, cert['cert'], tmpdir, tmpdir, cb)
            self.assertEqual(1, cb.call_count)
            self.assertTrue(os.path.exists(
                os.path.join(tmpdir, 'xtQz6ziJ.sh.part')))

    def test_walk_folders(self):
        from lacore.archive.folders import walk_folders
        sample = None
        files = [os.path.abspath(self.data),
                 os.path.abspath(
                     os.path.join('t', 'data', 'longaccess-74-5N93.html'))]
        for p, r in walk_folders(files):
            self.assertEqual(unicode, type(r))
            if r.endswith('sample.adf'):
                sample = r
        self.assertEqual("data/archives/sample.adf", sample)

    def test_folder_args(self):
        from lacore.archive.folders import FolderArchiver

        cb = Mock()
        ar = FolderArchiver()
        for a, k in ar.args([self.data], cb):
            self.assertTrue('arcname' in k)
            self.assertEqual(str, type(k['arcname']))

        self.assertTrue(u'data/archives/sample.adf' in
                        map(operator.itemgetter(1),
                            map(operator.itemgetter(0),
                                cb.call_args_list)))

    def test_folder_args_exception(self):
        from lacore.archive.folders import FolderArchiver

        cb = Mock(side_effect=Exception())
        ar = FolderArchiver()
        args = ar.args([self.data], cb)
        e = self.assertRaises(Exception, list, args)
        self.assertTrue(hasattr(e, 'filename'))

    @httpretty.activate
    def test_url_args(self):
        s = (self.getUniqueString() for _ in xrange(100))
        mkpath = lambda n: "/".join(islice(s, n))
        paths = [(mkpath(n),                              # relative path
                  next(s),                                # content
                  "http://" + next(s) + "/" + mkpath(n))  # url
                 for n in xrange(5)]
        for p, c, u in paths:
            httpretty.register_uri(httpretty.GET, u, body=c)
        from lacore.archive.urls import UrlArchiver
        cb = Mock()
        ar = list(UrlArchiver().args([(u, p) for p, c, u in paths], cb))
        for p, a, c in zip(paths, ar, cb.call_args_list):
            self.assertTrue('arcname' in a[1])
            self.assertEqual(str, type(a[1]['arcname']))
            self.assertEqual(p[0], a[1]['arcname'])
            self.assertEqual(p[0], c[0][1])
            with a[0][0] as contents:
                self.assertEqual(p[1], contents.read())

    @httpretty.activate
    def test_url_args_deprecated(self):
        s = (self.getUniqueString() for _ in xrange(100))
        fname = next(s)+'.txt'
        path = next(s)
        url = 'http://{}/{}'.format(next(s), fname)
        httpretty.register_uri(httpretty.GET, url, body='foo')
        from lacore.archive.urls import UrlArchiver
        ar = UrlArchiver().args([url, (url, path)], Mock())
        f, a = next(ar)
        self.assertEqual(fname, a['arcname'])
        with f[0] as contents:
            self.assertEqual('foo', contents.read())
        f, a = next(ar)
        self.assertEqual(path, a['arcname'])
        with f[0] as contents:
            self.assertEqual('foo', contents.read())

    @httpretty.activate
    def test_url_args_progress(self):
        s = (self.getUniqueString() for _ in xrange(100))
        paths = list(islice(s, 10))
        url = 'http://{}/{}'.format(next(s), next(s))
        body = self.getUniqueString()
        httpretty.register_uri(httpretty.GET, url, body=body)
        from lacore.archive.urls import UrlArchiver
        ar = UrlArchiver()
        args = ar.args([(url, p) for p in paths], Mock())
        for n, a, p in izip(count(), args, paths):
            self.assertEqual(n+1, len(ar.processed))
            self.assertEqual(p, a[1]['arcname'])
            self.assertEqual(0, ar.processed[p])
            self.assertEqual(body, a[0][0].read())
            self.assertEqual(len(body), ar.processed[p])

    def test_zip_archiver_tempfile(self):
        from lacore.archive.zip import ZipArchiver
        ar = ZipArchiver()
        foo = MagicMock()
        with ar._temp_file(foo) as f:
            f.write("BAR")
        foo.__enter__.assert_called()
        foo.__enter__.return_value.write.assert_called_with("BAR")

    def test_zip_archiver_args(self):
        from lacore.archive.zip import ZipArchiver
        ar = ZipArchiver()
        cb = Mock()
        self.assertEqual([], list(ar.args([], cb)))
        cb.assert_not_called()
        self.assertEqual([(('bar',), {})], list(ar.args(['bar'], cb)))
        cb.assert_called_with('bar', 'bar')

    def test_zip_archiver_no_zipstream(self):
        orig_import = __import__

        def import_mock(name, *args):
            if name == 'zipstream':
                raise ImportError()
            return orig_import(name, *args)
        with patch('__builtin__.__import__', side_effect=import_mock):
            if 'lacore.archive.zip' in sys.modules:
                del sys.modules['lacore.archive.zip']
            import lacore.archive.zip as azip
            with NamedTemporaryFile() as f:
                dst = MagicMock()
                dst.__enter__.return_value = f
                ar = azip.ZipArchiver()
                ar._temp_file = Mock(return_value=dst)
                list(ar.archive([os.path.abspath(os.path.join(
                    't', 'data', 'longaccess-74-5N93.html'))], dst, None))
                dst.__enter__.assert_called()
                ar._temp_file.assert_called()
                z = zipfile.ZipFile(f)
                z.testzip()

    def test_zip_archiver_zipstream(self):
        try:
            import zipstream  # noqa
        except ImportError:
            raise SkipTest("requires python-zipstream")
        if 'lacore.archive.zip' in sys.modules:
            del sys.modules['lacore.archive.zip']
        from lacore.archive.zip import ZipArchiver

        with NamedTemporaryFile() as f:
            dst = MagicMock()
            dst.__enter__.return_value = f
            ar = ZipArchiver()
            ar._temp_file = Mock(return_value=dst)
            list(ar.archive([os.path.abspath(os.path.join(
                't', 'data', 'longaccess-74-5N93.html'))], dst, None))
            dst.__enter__.assert_called()
            ar._temp_file.assert_not_called()
            z = zipfile.ZipFile(f)
            z.testzip()
