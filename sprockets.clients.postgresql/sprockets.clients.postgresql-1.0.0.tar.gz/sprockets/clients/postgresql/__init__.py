"""
PostgreSQL Session Classes
==========================
The Session classes wrap the Queries :py:class:`Session <queries.Session>` and
:py:class:`TornadoSession <queries.tornado_session.TornadoSession>` classes
providing environment variable based configuration.

The environment variables should be set using the ``DBNAME_[VARIABLE]`` format
where ``[VARIABLE]`` is one of  ``HOST``, ``PORT``, ``DBNAME``, ``USER``, and
``PASSWORD``.

For example, given the environment variables:

.. code:: python

    FOO_HOST = 'foodb'
    FOO_PORT = '6000'
    FOO_DBNAME = 'foo'
    FOO_USER = 'bar'
    FOO_PASSWORD = 'baz'

and code for creating a :py:class:`Session` instance for the database name
``foo``:

.. code:: python

    session = sprockets.postgresql.Session('foo')

The uri ``postgresql://bar:baz@foodb:6000/foo`` will be used when creating the
instance of :py:class:`queries.Session`.

"""
version_info = (1, 0, 0)
__version__ = '.'.join(str(v) for v in version_info)

import logging
import os

from queries import pool
import queries
from queries import tornado_session

_ARGUMENTS = ['host', 'port', 'dbname', 'user', 'password']

LOGGER = logging.getLogger(__name__)


def _get_uri(dbname):
    """Construct the URI for connecting to PostgreSQL by appending each
    argument name to the dbname, delimited by an underscore and
    capitalizing the new variable name.

    Values will be retrieved from the environment variable and added to a
    dictionary that is then passed in as keyword arguments to the
    :py:meth:`queries.uri` method to build the URI string.

    :param str dbname: The database name to construct the URI for
    :return: str

    """
    kwargs = dict()
    for arg in _ARGUMENTS:
        value = os.getenv(('%s_%s' % (dbname, arg)).upper())
        if value:
            if arg == 'port':
                kwargs[arg] = int(value)
            else:
                kwargs[arg] = value
    return queries.uri(**kwargs)


class Session(queries.Session):
    """Extends queries.Session using configuration data that is stored
    in environment variables.

    Utilizes connection pooling to ensure that multiple concurrent asynchronous
    queries do not block each other. Heavily trafficked services will require
    a higher ``max_pool_size`` to allow for greater connection concurrency.

    :param str dbname: PostgreSQL database name
    :param queries.cursor: The cursor type to use
    :param int pool_idle_ttl: How long idle pools keep connections open
    :param int pool_max_size: The maximum size of the pool to use

    """
    def __init__(self, dbname,
                 cursor_factory=queries.RealDictCursor,
                 pool_idle_ttl=pool.DEFAULT_IDLE_TTL,
                 pool_max_size=pool.DEFAULT_MAX_SIZE):
        super(Session, self).__init__(_get_uri(dbname),
                                      cursor_factory,
                                      pool_idle_ttl,
                                      pool_max_size)


class TornadoSession(tornado_session.TornadoSession):
    """Extends queries.TornadoSession using configuration data that is stored
    in environment variables.

    Utilizes connection pooling to ensure that multiple concurrent asynchronous
    queries do not block each other. Heavily trafficked services will require
    a higher ``max_pool_size`` to allow for greater connection concurrency.

    :py:meth:`query <queries.tornado_session.TornadoSession.query>` and
    :py:meth:`callproc <queries.tornado_session.TornadoSession.callproc>` must
    call :py:meth:`Results.free <queries.tornado_session.Results.free>`

    :param str dbname: PostgreSQL database name
    :param queries.cursor: The cursor type to use
    :param int pool_idle_ttl: How long idle pools keep connections open
    :param int pool_max_size: The maximum size of the pool to use
    :param tornado.ioloop.IOLoop ioloop: Pass in the instance of the tornado
        IOLoop you would like to use. Defaults to the global instance.

    """
    def __init__(self, dbname,
                 cursor_factory=queries.RealDictCursor,
                 pool_idle_ttl=pool.DEFAULT_IDLE_TTL,
                 pool_max_size=tornado_session.DEFAULT_MAX_POOL_SIZE,
                 io_loop=None):
        super(TornadoSession, self).__init__(_get_uri(dbname),
                                             cursor_factory,
                                             pool_idle_ttl,
                                             pool_max_size,
                                             io_loop)
