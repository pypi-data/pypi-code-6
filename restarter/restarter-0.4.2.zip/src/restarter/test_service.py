# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

import logging
import mock
import os
import restarter
import restarter.proc
import tempfile
import time
import unittest
from restarter.service import Service


class ServiceTest(unittest.TestCase):

    def setUp(self):
        # silence logger
        logging.getLogger('restarter').setLevel(logging.CRITICAL+1)

    @mock.patch('restarter.service.Service._restart_verify')
    def test_check_should_call_restart_if_stale(self, _rv):
        proc = restarter.proc.Proc('pidfile', 4711)
        proc.exe = '(deleted)'
        s = Service(proc, 'cmd1')
        s.check_restart()
        self.assertEqual(_rv.call_count, 1)

    @mock.patch('restarter.service.Service._restart_verify')
    def test_restart_should_do_nothing_if_no_restart_cmd(self, _rv):
        s = Service('dummy proc')
        s.restart()
        self.assertEqual(_rv.call_count, 0)

    @mock.patch('restarter.service.Service._restart_verify')
    def test_restart_should_call_restart_verify(self, _rv):
        s = Service('dummy proc', 'cmd1')
        s.restart()
        self.assertGreater(_rv.call_count, 0)

    @mock.patch('restarter.service.Service._restart_verify')
    def test_restart_should_try_once_unless_hard_restart_cmd(self, _rv):
        _rv.side_effect = restarter.RestartError('restart failed')
        s = Service('dummy proc', 'cmd1')
        self.assertRaises(restarter.RestartError, s.restart)
        self.assertEqual(_rv.call_count, 1)

    @mock.patch('restarter.service.Service._restart_verify')
    def test_restart_should_try_twice_if_hard_restart_cmd(self, _rv):
        _rv.side_effect = restarter.RestartError('restart failed')
        s = Service('dummy proc', 'cmd1', 'cmd2')
        self.assertRaises(restarter.RestartError, s.restart)
        self.assertEqual(_rv.call_count, 2)


class ServiceRestartVerifyTest(unittest.TestCase):

    def setUp(self):
        self.pidfile = tempfile.NamedTemporaryFile(mode='w+')
        print(os.getpid(), file=self.pidfile)
        self.pidfile.seek(0)
        self.proc = restarter.proc.Proc(self.pidfile.name, os.getpid())

    def tearDown(self):
        self.pidfile.close()

    @mock.patch('subprocess.call')
    def test_rv_should_call_command(self, _call):
        _call.return_value = 0
        s = Service(self.proc)
        try:
            s._restart_verify('cmd')
        except restarter.RestartError:
            pass
        self.assertEqual(1, _call.call_count)

    def test_rv_should_raise_on_command_failure(self):
        s = Service(self.proc)
        self.assertRaises(restarter.RestartError, s._restart_verify, 'false')

    def test_rv_should_raise_if_no_new_pidfile(self):
        s = Service(self.proc)
        with mock.patch.object(self.proc, 'reread') as _reread:
            _reread.side_effect = restarter.PidfileError()
            self.assertRaises(restarter.RestartError, s._restart_verify, 'true')

    def test_rv_should_raise_if_same_pid(self):
        s = Service(self.proc)
        self.assertRaises(restarter.RestartError, s._restart_verify, 'true')

    @mock.patch('time.sleep')
    def test_rv_should_sleep(self, _sleep):
        s = Service(self.proc, 'true', delay=3)
        try:
            s.restart()
        except restarter.RestartError:
            pass
        _sleep.assert_called_with(3)

