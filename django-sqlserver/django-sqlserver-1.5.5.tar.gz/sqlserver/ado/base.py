from __future__ import absolute_import, unicode_literals
import sys
from django.db import utils
from django.core.exceptions import ImproperlyConfigured, ValidationError
from . import dbapi as Database
adodb = Database

from sqlserver.base import SqlServerBaseWrapper

from .introspection import DatabaseIntrospection

DatabaseError = Database.DatabaseError
IntegrityError = Database.IntegrityError


def is_ip_address(value):
    """
    Returns True if value is a valid IP address, otherwise False.
    """
    # IPv6 added with Django 1.4
    from django.core.validators import validate_ipv46_address as ip_validator

    try:
        ip_validator(value)
    except ValidationError:
        return False
    return True


def connection_string_from_settings():
    from django.conf import settings
    db_settings = getattr(settings, 'DATABASES', {}).get('default', None) or settings
    return make_connection_string(db_settings)


def make_connection_string(settings):
    db_name = settings['NAME'].strip()
    db_host = settings['HOST'] or '127.0.0.1'
    db_port = settings['PORT']
    db_user = settings['USER']
    db_password = settings['PASSWORD']
    options = settings.get('OPTIONS', {})

    if len(db_name) == 0:
        raise ImproperlyConfigured("You need to specify a DATABASE NAME in your Django settings file.")

    # Connection strings courtesy of:
    # http://www.connectionstrings.com/?carrier=sqlserver

    # If a port is given, force a TCP/IP connection. The host should be an IP address in this case.
    if db_port:
        if not is_ip_address(db_host):
            raise ImproperlyConfigured("When using DATABASE PORT, DATABASE HOST must be an IP address.")
        try:
            port = int(db_port)
        except ValueError:
            raise ImproperlyConfigured("DATABASE PORT must be a number.")
        db_host = '{0},{1};Network Library=DBMSSOCN'.format(db_host, db_port)

    # If no user is specified, use integrated security.
    if db_user != '':
        user = db_user
        if isinstance(user, bytes):
            user = user.decode('utf8')
        password = db_password
        if isinstance(password, bytes):
            password = password.decode('utf8')
        auth_string = 'UID={0};PWD={1}'.format(user, password)
    else:
        auth_string = 'Integrated Security=SSPI'

    parts = [
        'DATA SOURCE={0};Initial Catalog={1}'.format(db_host, db_name),
        auth_string
    ]

    if not options:
        options = {}

    if not options.get('provider', None):
        options['provider'] = 'sqlncli10'

    parts.append('PROVIDER={0}'.format(options['provider']))

    if 'sqlncli' in options['provider'].lower():
        # native client needs a compatibility mode that behaves like OLEDB
        parts.append('DataTypeCompatibility=80')

    if options.get('use_mars', True):
        parts.append('MARS Connection=True')

    if options.get('extra_params', None):
        parts.append(options['extra_params'])

    return ";".join(parts)


VERSION_SQL2000 = 8
VERSION_SQL2005 = 9
VERSION_SQL2008 = 10
VERSION_SQL2012 = 11


class DatabaseWrapper(SqlServerBaseWrapper):
    Database = adodb

    def __init__(self, *args, **kwargs):
        super(DatabaseWrapper, self).__init__(*args, **kwargs)
        self.introspection = DatabaseIntrospection(self)

    def get_connection_params(self):
        """Returns a dict of parameters suitable for get_new_connection."""
        settings_dict = self.settings_dict.copy()
        if settings_dict['NAME'] == '':
            from django.core.exceptions import ImproperlyConfigured
            raise ImproperlyConfigured(
                "settings.DATABASES is improperly configured. "
                "Please supply the NAME value.")
        if not settings_dict['NAME']:
            # if _nodb_connection, connect to master
            settings_dict['NAME'] = 'master'

        autocommit = settings_dict.get('OPTIONS', {}).get('autocommit', False)
        return {
            'connection_string': make_connection_string(settings_dict),
            'timeout': self.command_timeout,
            'use_transactions': not autocommit,
            }

    def _get_new_connection(self, conn_params):
        conn = Database.connect(**conn_params)

        # cache the properties on the connection
        conn.adoConnProperties = dict([(x.Name, x.Value) for x in conn.adoConn.Properties])
        return conn

    def create_cursor(self):
        """Creates a cursor. Assumes that a connection is established."""
        cursor = self.connection.cursor()
        return cursor

    def _set_autocommit(self, value):
        self.connection.set_autocommit(value)

    def __get_dbms_version(self, conn):
        """
        Returns the 'DBMS Version' string
        """
        return conn.adoConnProperties.get('DBMS Version', '') if conn else ''

    def _is_sql2005_and_up(self, conn):
        return int(self.__get_dbms_version(conn).split('.')[0]) >= VERSION_SQL2005

    def _is_sql2008_and_up(self, conn):
        return int(self.__get_dbms_version(conn).split('.')[0]) >= VERSION_SQL2008

    def is_usable(self):
        try:
            # Use a cursor directly, bypassing Django's utilities.
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT 1")
        except self.Database.Error:
            return False
        else:
            return True