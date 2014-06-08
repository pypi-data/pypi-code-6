#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import ok_
import os
from py_utilities.compression.tar_utilities import create_tarball
import shutil
import tarfile
import tempfile
import unittest


class TestTarUtilities(unittest.TestCase):

    def setUp(self):
        self.cwd = os.path.dirname(os.path.realpath(__file__))
        self.temp_dir = tempfile.gettempdir()
        self.temp_tar = os.path.join(self.temp_dir, 'tar_test')
        self.test_dir = os.path.join(self.cwd, '..', 'data')

        if not os.path.exists(self.temp_tar):
            os.makedirs(self.temp_tar)

    def tearDown(self):
        if os.path.exists(self.temp_tar):
            shutil.rmtree(self.temp_tar)

    def test_create_tarball_gzip(self):
        f = create_tarball([self.test_dir], 'foobar', self.temp_tar)
        ok_(os.path.basename(f) != 'foobar.tar.gz')
        ok_(os.stat(f).st_size > 0)
        tarball = tarfile.open(f)
        ok_(len(tarball.getmembers()) > 0)

    def test_create_tarball_gzip_with_no_format_filename_is_itself(self):
        f = create_tarball([self.test_dir], 'foobarx', self.temp_tar, "")
        ok_(os.path.basename(f) == 'foobarx.tar.gz')
        ok_(os.path.basename(f).find('_') == -1)

    def test_create_tarball(self):
        f = create_tarball([self.test_dir],
                           'foobar2',
                           self.temp_tar,
                           gzip=False)

        ok_(os.path.basename(f) != 'foobar2.tar')
        ok_(os.stat(f).st_size > 0)
        tarball = tarfile.open(f)
        ok_(len(tarball.getmembers()) > 0)

    def test_create_tarball_with_no_format_filename_is_itself(self):
        f = create_tarball([self.test_dir], 'foobar2', self.temp_tar, "",
                           gzip=False)
        ok_(os.path.basename(f) == 'foobar2.tar')
        ok_(os.path.basename(f).find('_') == -1)

# vim: filetype=python
