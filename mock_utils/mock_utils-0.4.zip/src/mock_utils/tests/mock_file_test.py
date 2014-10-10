"""Tests for mocking of files."""

import unittest

from functools import partial
from textwrap import dedent
from unittest.mock import Mock

from mock_utils.mock_file import (make_mock_file,
                                  with_mock_files,
                                  with_mock_file_factories)

FILES = {'testfile': dedent('''\
                            example mocked file
                            with multiline contents!
                            ''')}

FILE_FACTORIES = {'testfile': partial(make_mock_file,
                                      contents=FILES['testfile'])}


class MockFileTests:
    def assert_lines(self, actual, expected_string):
        self.assertEqual(actual, expected_string.splitlines(keepends=True))

    def test_as_iterable(self):
        with open('testfile', 'r') as f:
            l = [line for line in f]
        self.assert_lines(l, self.contents('testfile'))

    def test_as_not_a_context_manager(self):
        l = [line for line in open('testfile', 'r')]
        self.assert_lines(l, self.contents('testfile'))

    def test_read(self):
        with open('testfile', 'r') as f:
            l = f.read()
        self.assertEqual(l, self.contents('testfile'))


@with_mock_files(FILES)
class WithMockFileTests(MockFileTests, unittest.TestCase):
    def contents(self, filename):
        return FILES[filename]


@with_mock_file_factories(FILE_FACTORIES)
class WithExistingMockFiles(MockFileTests, unittest.TestCase):
    def contents(self, filename):
        return ''.join(FILE_FACTORIES[filename]().lines)


def failing_read_factory():
    mock = make_mock_file()
    mock.read = Mock(side_effect=UnicodeDecodeError("", b"", 0, 0, ""))
    return mock


@with_mock_file_factories({'file': failing_read_factory})
class FailingMockTest(unittest.TestCase):
    def test_raises(self):
        with self.assertRaises(UnicodeDecodeError):
            with open('file', 'r') as f:
                f.read()
