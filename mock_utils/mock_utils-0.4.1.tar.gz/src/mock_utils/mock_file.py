# The MIT License (MIT)
#
# Copyright (c) 2014 Tarcisio E. M. Crocomo <tarcisio.crocomo AT gmail DOT com>
# Copyright (c) 2014 Felipe Trzaskowski <666.felipe AT gmail DOT com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""Utilities for mocking files."""

from functools import partial
from unittest.mock import patch, mock_open, Mock


def _mock_next(mock_file):
    """Implement next for a mocked file.

    Args:
        mock_file (Mock): the mocked file being iterated.
    """
    current = mock_file.current
    print(current, mock_file.lines)
    mock_file.current += 1
    if current == len(mock_file.lines):
        raise StopIteration
    return mock_file.lines[current]


def make_mock_file(contents=''):
    """Create a mocked file.

    Args:
        contents (str): the contents of the file, for the read() functions
                        and/or iterating.

    Returns:
        Mock: the mocked file.
    """
    mocked = mock_open(read_data=contents)()
    mocked.lines = contents.splitlines(keepends=True)
    mocked.current = 0
    mocked.__next__.side_effect = partial(_mock_next, mocked)
    mocked.__iter__ = Mock(return_value=mocked)
    return mocked


def _make_mock_open(files):
    """Create a mock open() function.

    Args:
        files (dict): a dict mapping filenames (str) to contents (str).

    Returns:
        function: the mocked open function.
    """
    def open_mock_file(filename, *args, **kwargs):
        return make_mock_file(contents=files[filename])
    return open_mock_file


def with_mock_file_factories(factories):
    """Make a decorator similar to :func:`with_mock_files`, but with functions
    that instantiate mock files.

    Args:
        factories (dict): a dict mapping filenames (str) to factories
                          (function).

    Returns:
        decorator: a decorator which mocks `builtins.open` in a context.
    """
    def mock_open_on_context(c):
        return patch('builtins.open',
                     lambda filename, *a, **k:
                     factories[filename]())(c)
    return mock_open_on_context


def with_mock_files(files):
    """Make a decorator for a context in which to mock `builtins.open`,
    with the contents of the files to mock.

    Args:
        files (dict): a dict mapping filenames (str) to contents (str).

    Returns:
        decorator: a decorator which mocks `builtins.open` in a context.
    """
    def mock_open_on_context(c):
        """Mock `builtins.open` on a context.

        Args:
            c (context): the context in which to mock `open`.
        """
        return patch('builtins.open', _make_mock_open(files))(c)
    return mock_open_on_context
