from __future__ import absolute_import, unicode_literals
from django.conf import settings
try:
    from django.utils.timezone import utc
except:
    pass

try:
    import pytds
except ImportError:
    pytds = None
    raise Exception('pytds is not available, run pip install python-tds to fix this')

from sqlserver.base import SqlServerBaseWrapper

from .introspection import DatabaseIntrospection

Database = pytds


def utc_tzinfo_factory(offset):
    if offset != 0:
        raise AssertionError("database connection isn't set to UTC")
    return utc


class _CursorWrapper(object):
    """Used to intercept database errors for cursor's __next__ method"""
    def __init__(self, cursor, error_wrapper):
        self._cursor = cursor
        self._error_wrapper = error_wrapper
        self.execute = cursor.execute
        self.fetchall = cursor.fetchall

    def __getattr__(self, attr):
        return getattr(self._cursor, attr)

    def __iter__(self):
        it = iter(self._cursor)
        return _CursorIterator(it, self._error_wrapper)


class _CursorIterator(object):
    """Used to intercept database errors for cursor's __next__ method"""
    def __init__(self, it, error_wrapper):
        self._it = it
        self._error_wrapper = error_wrapper

    def __iter__(self):
        return self

    def next(self):
        with self._error_wrapper:
            return self._it.next()

    def __next__(self):
        with self._error_wrapper:
            return self._it.__next__()


class DatabaseWrapper(SqlServerBaseWrapper):
    Database = pytds

    def __init__(self, *args, **kwargs):
        super(DatabaseWrapper, self).__init__(*args, **kwargs)
        self.introspection = DatabaseIntrospection(self)

    def create_cursor(self):
        """Creates a cursor. Assumes that a connection is established."""
        cursor = self.connection.cursor()
        cursor.tzinfo_factory = utc_tzinfo_factory if settings.USE_TZ else None
        error_wrapper = self.wrap_database_errors
        return _CursorWrapper(cursor, error_wrapper)

    def _set_autocommit(self, autocommit):
        self.connection.autocommit = autocommit

    def get_connection_params(self):
        """Returns a dict of parameters suitable for get_new_connection."""
        settings_dict = self.settings_dict
        options = settings_dict.get('OPTIONS', {})
        autocommit = options.get('autocommit', False)
        conn_params = {
            'server': settings_dict['HOST'],
            'database': settings_dict['NAME'],
            'user': settings_dict['USER'],
            'password': settings_dict['PASSWORD'],
            'timeout': self.command_timeout,
            'autocommit': autocommit,
            'use_mars': options.get('use_mars', False),
            'load_balancer': options.get('load_balancer', None),
            'use_tz': utc if getattr(settings, 'USE_TZ', False) else None,
        }
        return conn_params

    def _get_new_connection(self, conn_params):
        return pytds.connect(**conn_params)

    def _enter_transaction_management(self, managed):
        if self.features.uses_autocommit and managed:
            self.connection.autocommit = False

    def _leave_transaction_management(self, managed):
        if self.features.uses_autocommit and not managed:
            self.connection.autocommit = True

    def _is_sql2005_and_up(self, conn):
        return conn.tds_version >= pytds.TDS72

    def _is_sql2008_and_up(self, conn):
        return conn.tds_version >= pytds.TDS73

    def is_usable(self):
        try:
            # Use a cursor directly, bypassing Django's utilities.
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT 1")
        except self.Database.Error:
            return False
        else:
            return True