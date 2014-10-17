import os
import unittest

import django
import mock


def no_db_testcase(func):
    """ Decorator that prevents your test touching database.

    :raises RuntimeError: if test try to do database query
    """
    cursor_wrapper = mock.MagicMock(side_effect=RuntimeError("Do not touch the database!"))
    mocking_dict = {
        'execute': cursor_wrapper,
        'executemany': cursor_wrapper,
        'callproc': cursor_wrapper,
    }
    try:
        from django.db.backends.util import CursorWrapper
    except ImportError:  # pragma: no cover
        # Django < 1.3 has no CursorWrapper so give support at least for sqlite
        from django.db.backends.sqlite3.base import SQLiteCursorWrapper as CursorWrapper  # pragma: no cover
        del mocking_dict['callproc']  # pragma: no cover
    try:
        CursorWrapper.execute
    except AttributeError:  # pragma: no cover
        # Django < 1.6 uses __getattr__
        mocking_dict = {'__getattr__': cursor_wrapper}  # pragma: no cover
    wrapped = mock.patch.multiple(CursorWrapper, **mocking_dict)
    return wrapped(func)



def test_type(name):
    """ Function creating decorators that allows skipping tests of declared type.

    :param str name: arbitrary name of test type e.g. acceptance,unit
    """
    return unittest.skipIf(name in os.environ.get('IGNORE_TESTS', ''), '%s test skipped' % name)
