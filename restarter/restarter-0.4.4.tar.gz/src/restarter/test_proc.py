# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

import contextlib
import mock
import os
import restarter
import sys
import tempfile
import unittest
from restarter.proc import Proc, readpid


class ReadpidTest(unittest.TestCase):

    @contextlib.contextmanager
    def self_in_pidfile(self):
        with tempfile.NamedTemporaryFile(mode='w+') as f:
            print(os.getpid(), file=f)
            f.seek(0)
            yield f.name

    def test_should_contain_exe(self):
        with self.self_in_pidfile() as pidfile:
            proc = readpid(pidfile)
            self.assertEqual(os.path.realpath(sys.executable), proc.exe)

    def test_should_contain_maps(self):
        with self.self_in_pidfile() as pidfile:
            proc = readpid(pidfile)
            self.assertIn('/libc-', proc.maps)

    def test_should_fail_unless_pidfile(self):
        tf = tempfile.NamedTemporaryFile()
        filename = tf.name
        tf.close()  # unlinks file
        self.assertRaises(restarter.PidfileError, readpid, filename)

    @mock.patch('os.readlink')
    def test_should_require_running_process(self, _readlink):
        _readlink.side_effect = OSError(2, 'No such file or directory')
        with self.self_in_pidfile() as fn:
            self.assertRaises(restarter.PidfileError, readpid, fn)

    def test_should_require_integer_pid(self):
        with tempfile.NamedTemporaryFile(mode='w+') as f:
            self.assertRaises(restarter.PidfileError, readpid, f.name)

    def test_reread_should_return_new_proc(self):
        with self.self_in_pidfile() as pidfile:
            proc = readpid(pidfile)
            proc2 = proc.reread()
            self.assertEqual(proc, proc2)

    def test_readpid_should_ignore_additional_lines(self):
        with tempfile.NamedTemporaryFile(mode='w+') as pidfile:
            print("""\
{}
/srv/postgresql/8.4/data
  5432001         0
""".format(os.getpid()), file=pidfile)
            pidfile.seek(0)
            proc = readpid(pidfile.name)
            self.assertEqual(os.getpid(), proc.pid)

class ProcTest(unittest.TestCase):

    atd_maps_intact = """\
08048000-0804c000 r-xp 00000000 fd:01 853944     /usr/sbin/atd
08ecc000-08eed000 rw-p 00000000 00:00 0          [heap]
b75e0000-b75ea000 r-xp 00000000 fd:01 622557     /lib/libnss_files-2.11.2.so
b75ec000-b75ee000 rw-p 00000000 00:00 0 
b7738000-b7743000 r-xp 00000000 fd:01 622603     /lib/libpam.so.0.83.0
b774e000-b7750000 rw-p 00000000 00:00 0 
b7750000-b7751000 r-xp 00000000 00:00 0          [vdso]
b7751000-b776d000 r-xp 00000000 fd:01 622562     /lib/ld-2.11.2.so
bfd0f000-bfd30000 rw-p 00000000 00:00 0          [stack]
"""

    atd_maps_deleted = """\
08048000-0804c000 r-xp 00000000 fd:01 853944     /usr/sbin/atd
08ecc000-08eed000 rw-p 00000000 00:00 0          [heap]
b75e0000-b75ea000 r-xp 00000000 fd:01 622557     /lib/libnss_files-2.11.2.so
b75ec000-b75ee000 rw-p 00000000 00:00 0 
b7738000-b7743000 r-xp 00000000 fd:01 622603     /lib/libpam.so.0.83.0 (deleted)
b774e000-b7750000 rw-p 00000000 00:00 0 
b7750000-b7751000 r-xp 00000000 00:00 0          [vdso]
b7751000-b776d000 r-xp 00000000 fd:01 622562     /lib/ld-2.11.2.so
bfd0f000-bfd30000 rw-p 00000000 00:00 0          [stack]
"""

    @mock.patch('os.access')
    def test_intact_exe_should_not_be_stale(self, _access):
        _access.return_value = True
        p = Proc('pidfile', 0)
        p.exe = '/path/to/exe'
        self.assertFalse(p.stale_exe())

    @mock.patch('os.access')
    def test_deleted_exe_should_be_stale(self, _access):
        _access.return_value = False
        p = Proc('pidfile', 0)
        p.exe = '/path/to/exe (deleted)'
        self.assertTrue(p.stale_exe())

    @mock.patch('os.access', new=lambda fn, mode: not '(deleted)' in fn)
    def test_intact_maps_should_not_be_stale(self):
        p = Proc('pidfile', 0)
        p.maps = self.atd_maps_intact
        self.assertFalse(p.stale_maps())

    @mock.patch('os.access', new=lambda fn, mode: not '(deleted)' in fn)
    def test_deleted_maps_should_be_stale(self):
        p = Proc('pidfile', 0)
        p.maps = self.atd_maps_deleted
        self.assertTrue(p.stale_maps())

    @mock.patch('os.access', new=lambda fn, mode: not '(deleted)' in fn)
    def test_exclude_maps_using_filename(self):
        p = Proc('pidfile', 0, exclude=['/irrelevant', '/lib/libpam.so.0.83.0',
                                        '/dummy'])
        p.maps = self.atd_maps_deleted
        self.assertFalse(p.stale_maps())

    @mock.patch('os.access', new=lambda fn, mode: not '(deleted)' in fn)
    def test_exclude_maps_using_glob(self):
        p = Proc('pidfile', 0, exclude=['*pam.so*'])
        p.maps = self.atd_maps_deleted
        self.assertFalse(p.stale_maps())
