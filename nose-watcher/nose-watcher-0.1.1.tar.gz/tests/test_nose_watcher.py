# -*- coding: utf-8 -*-
from collections import namedtuple
import sys
import unittest

from mock import Mock, patch

from nose_watcher.nose_watcher import WatcherPlugin


class TestNoseWatcher(unittest.TestCase):

    def setUp(self):
        self.plugin = WatcherPlugin()
        self.plugin.testing = True
        self.plugin.call = Mock()


class TestFileTypes(TestNoseWatcher):
    def test_file_types_py(self):
        self.assertTrue(self.plugin.check_files({'test.py'}))

    def test_file_types_pyx(self):
        self.assertTrue(self.plugin.check_files({'test.pyx'}))

    def test_file_types_pyc(self):
        self.assertFalse(self.plugin.check_files({'test.pyc'}))

    def test_file_types_py_and_pyc(self):
        self.assertTrue(self.plugin.check_files({'test.py', 'test.pyc'}))

    def test_file_types_pyc_and_txt(self):
        self.assertFalse(self.plugin.check_files({'test.txt', 'test.pyc'}))


class TestArgumentParsing(TestNoseWatcher):
    def test_arguments(self):
        args_in = ['laa', '--with-%s' % WatcherPlugin.name, '--with-cover']
        args_out = self.plugin.get_commandline_arguments(args_in)

        self.assertEqual(
            args_out,
            ['laa', '--with-cover']
        )

    def test_argument_parsing_from_sys_argv(self):
        self.assertEqual(
            self.plugin.get_commandline_arguments(),
            [a for a in sys.argv if a != '--with-watcher']
        )


class TestWatching(TestNoseWatcher):
    @patch('inotify.watcher.AutoWatcher')
    @patch('inotify.watcher.Threshold')
    @patch('select.poll')
    def test_watch_no_files_modified(self, poll_mock, threshold_patch,
                                     watcher_mock):
        threshold = Mock()
        threshold_patch.return_value = threshold
        threshold.return_value = True
        self.plugin.finalize(None)

        self.assertFalse(self.plugin.call.called)

    @patch('inotify.watcher.AutoWatcher')
    @patch('inotify.watcher.Threshold')
    @patch('select.poll')
    def test_watch_no_files_watched(self, poll_mock, threshold_patch,
                                    watcher_mock):
        threshold = Mock()
        threshold_patch.return_value = threshold
        threshold.return_value = True

        watcher = Mock()
        watcher_mock.return_value = watcher

        watcher.num_watches.return_value = False
        self.plugin.finalize(None)

        self.assertFalse(self.plugin.call.called)

    @patch('inotify.watcher.AutoWatcher')
    @patch('inotify.watcher.Threshold')
    @patch('select.poll')
    def test_watch_python_files_modified(self, poll_mock, threshold_patch,
                                         watcher_mock):
        threshold = Mock()
        threshold_patch.return_value = threshold
        threshold.return_value = True

        watcher = Mock()
        watcher_mock.return_value = watcher

        Event = namedtuple('Event', ['fullpath'])
        watcher.read.return_value = [
            Event('aaa/python.py')
        ]
        self.plugin.finalize(None)

        self.assertTrue(self.plugin.call.called)

    @patch('inotify.watcher.AutoWatcher')
    @patch('inotify.watcher.Threshold')
    @patch('select.poll')
    def test_watch_text_files_modified(self, poll_mock, threshold_patch,
                                       watcher_mock):
        threshold = Mock()
        threshold_patch.return_value = threshold
        threshold.return_value = True

        watcher = Mock()
        watcher_mock.return_value = watcher

        Event = namedtuple('Event', ['fullpath'])
        watcher.read.return_value = [
            Event('aaa/python.txt')
        ]
        self.plugin.finalize(None)

        self.assertFalse(self.plugin.call.called)
