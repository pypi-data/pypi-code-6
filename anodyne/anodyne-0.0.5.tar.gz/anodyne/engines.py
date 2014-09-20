import logging

from sqlalchemy import exc as sqla_exc
from sqlalchemy import create_engine as sqla_create_engine
from sqlalchemy import pool as sqla_pool
from sqlalchemy import orm

from anodyne import exceptions as _exceptions

on_engine_failure = None

logger = logging.getLogger(__name__)
server_engines = {}
backends = {}
default_server_engine = None
configured = False


class engine_types:
    postgres = "postgresql"
    postgres_psycopg2 = "postgresql+psycopg2"
    mysql = "mysql"
    pymysql = "mysql+pymysql"
    sqlite = "sqlite"

_engine_types = [
    engine_types.postgres,
    engine_types.postgres_psycopg2,
    engine_types.mysql,
    engine_types.pymysql,
    engine_types.sqlite
]


def configure(server_backends, default_engine=None, failure_callback=None):
    global on_engine_failure, backends, configured, default_server_engine
    if configured:
        raise _exceptions.ConfigurationException(
            "The connection layer has already been configured."
        )

    if backends is None:
        raise ValueError("server_backends cannot be None!")

    backends = server_backends
    on_engine_failure = failure_callback

    if default_engine is not None and default_engine in _engine_types:
        default_server_engine = default_server_engine

    configured = True


def create_engine(engine_type, connection_details, log_name_prefix=None):
    """
    Creates an engine based on the provided engine type and connection details.

    :param engine_type: a tincture.engines.engine_types string.
    :param connection_details: a dictionary containing connection details.
            Must include keys: user, passwd, host, port and db.
    :return: a dictionary of engine meta data, including the engine reference.
    """
    global configured
    if not configured:
        raise _exceptions.ConfigurationException(
            "Cannot create engines before configuration."
        )
    if engine_type == engine_types.sqlite:
        url = connection_details.get("url")
        if url is None:
            dbname = connection_details.get("dbname")
            if dbname is not None:
                connection_string = "%s:///%s" % (
                    engine_type, connection_details.get("dbname")
                )
            else:
                raise _exceptions.CongifurationException("SQLite databases must have a url or dbname configured.")
        else:
            connection_string = url
    else:
        connection_string = "%s://%s:%s@%s:%s/%s" % (
            engine_type,
            connection_details.get("username"),
            connection_details.get("password"),
            connection_details.get("host"),
            connection_details.get("port"),
            connection_details.get("dbname")
        )
    kwargs = {
        "poolclass": sqla_pool.QueuePool,
    }
    if log_name_prefix is not None:
        kwargs["logging_name"] = "%s.%s" % (__name__, log_name_prefix)

    engine = sqla_create_engine(connection_string, **kwargs)
    engine_data = {
        "failed": False,
        "engine_type": engine_type,
        "connection_details": connection_details,
        "engine": engine,
        "session_class": orm.sessionmaker(bind=engine)
    }
    return engine_data


def poke_engine(engine_meta_data, attempt):
    """
    "Poking" an engine. Meaning attempting a connection on said engine in order
    to revive it's health status (failed => False).

    This function is useful for periodic health checks on a given engine,
    as well as recovery of a dead engine. It will call the global callback
    function `failure_callback`, in the event that the connection fails.

    It is useful to configure this as something such as "gevent.spawn_later",
    using this function as the callback.

    :param engine_meta_data: the engine_meta_data to check.
    :param attempt: how many times we've already poked this engine.
    """
    global on_engine_failure, configured
    if not configured:
        raise _exceptions.ConfigurationException(
            "Cannot poke engine before configuration."
        )

    engine = engine_meta_data.get("engine")
    logger.info("Poking engine: %r. This is attempt: %d" % (
        repr(engine), (attempt + 1)
    ))
    try:
        conn = engine.connect()
        conn.close()
        engine_meta_data["failed"] = False
        logger.info("Engine revived.")
    except sqla_exc.OperationalError:
        logger.warning(
            "Poked %r, but it still appears to be down." % repr(engine)
        )
        if on_engine_failure is not None:
            on_engine_failure(engine_meta_data, attempt + 1)


def mark_failed(server_list_key, engine):
    """
    Marks a given engine as failed, If the failure callback is defined, it will
    be executed with the engine object.

    :param server_list_key: a db name mapping to connection engine meta data.
    :param engine: engine metadata that should have a reference to.
    """
    global server_engines, on_engine_failure, configured
    if not configured:
        raise _exceptions.ConfigurationException(
            "Cannot mark failures before configuration."
        )

    if engine is None:
        logger.error("Cannot mark %s engine meta as failed" % type(None))
        return

    if server_list_key is None:
        logger.error("Need a server in order to mark a failed engine.")

    engines = server_engines.get(server_list_key)

    if engines is None:
        logger.error("No engines configured for: %s." % server_list_key)
        return

    if engine not in engines:
        logger.error("Engine: %r does not belong to %r" % (
            engine.get("engine"), server_list_key
        ))

    engine["failed"] = True
    if on_engine_failure is not None:
        on_engine_failure(engine, 0)


def shuffle_engines(server_list_key):
    """
    Shuffles the engines in an engine list mapped by server_list_key.

    :param server_list_key: a db name mapping to connection engine meta data.
    """
    global server_engines, configured
    if not configured:
        raise _exceptions.ConfigurationException(
            "Cannot shuffle engines before configuration."
        )

    engine_list = server_engines.get(server_list_key, [])
    if len(engine_list) > 1:
        being_recycled = engine_list.pop(0)
        logger.info("Shuffling database engine: %s to %s" % (
            being_recycled,
            engine_list[0]
        ))
        engine_list.append(being_recycled)
        server_engines[server_list_key] = engine_list
    else:
        logger.warning(
            "Cannot shuffle engines with less than 2 servers defined."
        )


def get_engine(server_list_key, recycle=False, log_name=""):
    """
    Retrieves a sqlalchemy Engine object to use for database connections.

    :param server_list_key: a db name mapping to connection engine meta data.
    :param recycle: Whether we should recycle the engines for server_list_key.
    :return: engine meta data used to create a connection.
    """
    global server_engines, configured, backends, default_server_engine
    if not configured:
        raise _exceptions.ConfigurationException(
            "Cannot get engines before configuration."
        )
    database_engine = None
    if default_server_engine is not None:
        database_engine = default_server_engine

    server_info = backends.get(server_list_key)
    database_engine = server_info.get("engine_type", database_engine)
    engines = server_engines.get(server_list_key)

    if engines is None:
        server_list = server_info.get("servers")
        if server_list is None:
            server_list = []

        engine_list = []
        for index, engine_def in enumerate(server_list):
            one_based = index + 1
            num_prefix = "0%d" % one_based if index < 10 else one_based
            if log_name.startswith("-"):
                num_prefix = "%s-" % num_prefix

            log_prefix = "%s%s-%s" % (
                num_prefix,
                log_name,
                server_list_key
            )
            new_engine = create_engine(
                database_engine,
                engine_def,
                log_name_prefix=log_prefix
            )
            engine_list.append(new_engine)
        server_engines[server_list_key] = engine_list
    else:
        if recycle:
            shuffle_engines(server_list_key)

    engines = server_engines[server_list_key]
    for engine in engines:
        if not engine.get("failed", False):
            return engine
    return None


def clean_engines(server_list_key=None):
    """
    Disposes of all listed engines mapped to by server_list_key.
    If server_list_key is empty, we clear them all.

    :param server_list_key: a db name mapping to connection engine meta data.
    """
    global server_engines, configured
    if not configured:
        raise _exceptions.ConfigurationException(
            "Cannot clean engines before configuration."
        )
    if server_list_key is None:
        keys_to_clear = server_engines.keys()
    else:
        keys_to_clear = [server_list_key]
    for key in keys_to_clear:
        engine_list = server_engines.get(key)
        if engine_list is not None:
            for engine_data in engine_list:
                engine_data["engine"].dispose()
            del server_engines[key]
        else:
            # raise an exception?
            logger.error(
                "Tried to clear engines for keys: '%s', but key was not "
                "found." % keys_to_clear
            )
