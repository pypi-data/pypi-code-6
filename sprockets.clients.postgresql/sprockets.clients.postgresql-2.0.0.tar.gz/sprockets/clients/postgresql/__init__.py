"""
PostgreSQL Session API
======================
The Session classes wrap the Queries :py:class:`Session <queries.Session>` and
:py:class:`TornadoSession <queries.tornado_session.TornadoSession>` classes
providing environment variable based configuration.

Environment variables should be set using the ``PGSQL[_DBNAME]`` format
where the value is a PostgreSQL URI.

For PostgreSQL URI format, see:

http://www.postgresql.org/docs/9.3/static/libpq-connect.html#LIBPQ-CONNSTRING

As example, given the environment variable:

.. code:: python

    PGSQL_FOO = 'postgresql://bar:baz@foohost:6000/foo'

and code for creating a :py:class:`Session` instance for the database name
``foo``:

.. code:: python

    session = sprockets.postgresql.Session('foo')

A :py:class:`queries.Session` object will be created that connects to Postgres
running on ``foohost``, port ``6000`` using the username ``bar`` and the
password ``baz``, connecting to the ``foo`` database.

"""
version_info = (2, 0, 0)
__version__ = '.'.join(str(v) for v in version_info)

import logging
import os

from queries import pool
import queries
from queries import tornado_session

_ARGUMENTS = ['host', 'port', 'dbname', 'user', 'password']

LOGGER = logging.getLogger(__name__)


# For ease of access to different cursor types
from queries import DictCursor
from queries import NamedTupleCursor
from queries import RealDictCursor
from queries import LoggingCursor
from queries import MinTimeLoggingCursor

# Expose exceptions so clients do not need to import queries as well
from queries import DataError
from queries import DatabaseError
from queries import IntegrityError
from queries import InterfaceError
from queries import InternalError
from queries import NotSupportedError
from queries import OperationalError
from queries import ProgrammingError
from queries import QueryCanceledError
from queries import TransactionRollbackError


def _get_uri(dbname):
    """Return the URI for the specified database name from an environment
    variable. If dbname is blank, the ``PGSQL`` environment variable is used,
    otherwise the database name is cast to upper case and concatenated to
    ``PGSQL_`` and the URI is retrieved from ``PGSQL_DBNAME``. For example,
    if the value ``foo`` is passed in, the environment variable used would be
    ``PGSQL_FOO``.

    :param str dbname: The database name to construct the URI for
    :return: str
    :raises: KeyError

    """
    if not dbname:
        return os.environ['PGSQL']
    return os.environ['PGSQL_{0}'.format(dbname).upper()]


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
