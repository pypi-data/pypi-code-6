import unittest
import mock

import ziptools.core

@mock.patch("ziptools.core.subprocess")
class TestGunzip(unittest.TestCase):
    def test_gunzip_given_gz_file_gunzips_file(self, subprocess):
        gzfile = "file.nc.gz"
        result = ziptools.core.gunzip(gzfile)
        subprocess.call.assert_called_once_with(["gunzip", gzfile,])

    def test_gunzip_given_normal_file_does_nothing(self, subprocess):
        file = "file.nc"
        result = ziptools.core.gunzip(file)
        self.assertFalse(subprocess.call.called)
        self.assertEqual(file, result)

    def test_gunzip_given_gz_file_returns_correct_name(self, subprocess):
        gzfile = "file.nc.gz"
        result = ziptools.core.gunzip(gzfile)
        expect = "file.nc"
        self.assertEqual(result, expect)

    def test_gunzip_given_force_calls_gunzip_f(self, subprocess):
        gzfile = "file.nc.gz"
        result = ziptools.core.gunzip(gzfile, force=True)
        subprocess.call.assert_called_once_with(["gunzip", "-f", gzfile,])

@mock.patch("ziptools.core.subprocess")
class TestGzip(unittest.TestCase):
    def test_gzip_given_normal_file_gzips_file(self, subprocess):
        file = "file.nc"
        result = ziptools.core.gzip(file)
        subprocess.call.assert_called_once_with(["gzip", file,])

    def test_gzip_given_gzfile_does_nothing(self, subprocess):
        gzfile = "file.nc.gz"
        result = ziptools.core.gzip(gzfile)
        self.assertFalse(subprocess.call.called)
        self.assertEqual(gzfile, result)

    def test_gzip_given_normal_file_returns_correct_name(self, subprocess):
        file = "file.nc"
        result = ziptools.core.gzip(file)
        expect = "file.nc.gz"
        self.assertEqual(result, expect)

    def test_gzip_given_force_calls_gzip_f(self, subprocess):
        file = "file.nc"
        result = ziptools.core.gzip(file, force=True)
        subprocess.call.assert_called_once_with(["gzip", "-f", file,])

@mock.patch("ziptools.core.gzip")
class TestGzipped(unittest.TestCase):
    def test_basic_usage(self, mock_gzip):
        items = ["a", "b", "c"]
        mock_gzip.return_value = 1
        result = ziptools.core.gzipped(items)
        expected = [mock.call(item, force=False) for item in items]
        self.assertEqual(expected, mock_gzip.call_args_list)
        self.assertEqual(mock_gzip.call_count, len(items))
    def test_gzipped_takes_force_argument(self, mock_gzip):
        items = ["a", "b", "c"]
        mock_gzip.return_value = 1
        result = ziptools.core.gzipped(items, force=True)
        expected = [mock.call(item, force=True) for item in items]
        self.assertEqual(expected, mock_gzip.mock_calls)
        self.assertEqual(mock_gzip.call_count, len(items))

@mock.patch("ziptools.core.gunzip")
class TestGunzipped(unittest.TestCase):
    def test_basic_usage(self, mock_gunzip):
        items = ["a", "b", "c"]
        mock_gunzip.return_value = 1
        result = ziptools.core.gunzipped(items)
        expected = [mock.call(item, force=False) for item in items]
        self.assertEqual(expected, mock_gunzip.call_args_list)
        self.assertEqual(mock_gunzip.call_count, len(items))
    def test_gunzipped_takes_force_argument(self, mock_gunzip):
        items = ["a", "b", "c"]
        mock_gunzip.return_value = 1
        result = ziptools.core.gunzipped(items, force=True)
        expected = [mock.call(item, force=True) for item in items]
        self.assertEqual(expected, mock_gunzip.mock_calls)
        self.assertEqual(mock_gunzip.call_count, len(items))

@mock.patch("ziptools.core.gzipped")
class TestGzipfilesDecorator(unittest.TestCase):
    def test_basic_usage_without_arguments(self, mock_gzipped):
        @ziptools.core.gzipfiles
        def func(items):
            return items
        items = []
        func(items)
        mock_gzipped.assert_called_once_with(items, force=False)
    def test_basic_usage_with_arguments(self, mock_gzipped):
        @ziptools.core.gzipfiles(force=True)
        def func(items):
            return items
        items = []
        func(items)
        mock_gzipped.assert_called_once_with(items, force=True)

@mock.patch("ziptools.core.gunzipped")
class TestGunzipfilesDecorator(unittest.TestCase):
    def test_basic_usage_without_arguments(self, mock_gunzipped):
        @ziptools.core.gunzipfiles
        def func(items):
            return items
        items = []
        func(items)
        mock_gunzipped.assert_called_once_with(items, force=False)
    def test_basic_usage_with_arguments(self, mock_gunzipped):
        @ziptools.core.gunzipfiles(force=True)
        def func(items):
            return items
        items = []
        func(items)
        mock_gunzipped.assert_called_once_with(items, force=True)
