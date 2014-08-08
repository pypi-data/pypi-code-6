from funcy import decorator

from django.conf import settings
if not settings.configured:
    settings.configure()

from django.db import models  # noqa
from django.db import connections


DATABASE_ENGINE_TO_DRIVER_PATH = {
    'sqlite': 'django.db.backends.sqlite3',
    'postgresql': 'django.db.backends.postgresql_psycopg2',
}

DEFAULT_ALIAS = 'default'


def table(table_name):
    """
    Patch Meta with neccesary attributes.

    """
    # Create decorator
    def patcher(cls):
        cls.app_label = ''
        cls.managed = False
        cls.db_table = table_name
        return cls

    # Return decorator
    return patcher


def patch_settings(settings_module, alias, engine='sqlite', name='', host=None, port=None, user=None, password=None, options=None):
    settings_module.DATABASES[alias] = {
        'ENGINE': DATABASE_ENGINE_TO_DRIVER_PATH[engine],
        'NAME': name,
        'HOST': host,
        'PORT': port,
        'USER': user,
        'PASSWORD': password,
        'OPTIONS': options if options is not None else {},
    }


def setup_database(alias=DEFAULT_ALIAS, **db_config):
    patch_settings(settings, alias, **db_config)


def run_query(sql_filename, alias=DEFAULT_ALIAS, params=None, with_description=False):
    """
    Run given sql query on given Django database and return the rows.

    """
    # Set SQL dir default
    sql_directory = settings.SQL_DIR if hasattr(settings, 'SQL_DIR') else 'sql'

    # Read sql query from file
    with open('{}/{}'.format(sql_directory, sql_filename)) as f:
        sql = f.read()

    # Create database connection
    cursor = connections[alias].cursor()

    # Run query and fetch results
    try:
        if params is None:
            cursor.execute(sql)
        else:
            cursor.execute(sql, params)

        rows = cursor.fetchall()

        if with_description:
            return rows, cursor.description
        else:
            return rows

    finally:
        cursor.close()


@decorator
def with_query(call, sql_filename, alias=DEFAULT_ALIAS, params=None, with_description=False):
    rows = run_query(sql_filename, alias, params, with_description)
    return call(rows)
