import contextlib
import logging

from anodyne import exceptions
from anodyne import engines

from sqlalchemy import exc as sqla_exc

logger = logging.getLogger(__name__)


def _get_engine(database, recycle=False):
    """
    Convenience function for retrieving a database engine from tincture.engines.

    :param database: The database to retrieve an engine for.
    :param recycle: Whether or not to direct the engines to be recycled.
    :return: a database engine object.
    """
    engine_data = engines.get_engine(database, recycle=recycle)
    if engine_data is None:
        err = "No engines available for '%s'" % database
        raise exceptions.NoValidEnginesException(err)
    if engine_data.get("engine") is None:
        err = "Engine Data found, but no engine was created. %s" % engine_data
        raise exceptions.EmptyEngineException(err)
    return engine_data


def get_connection(database):
    """
    Retrieves a database connection for the database reference provided.

    :param database: a name of database engine managed by tincture.
    :return: a connection.
    """
    engine_data = _get_engine(database)
    engine = engine_data.get("engine")
    try:
        conn = engine.connect()
    except sqla_exc.OperationalError, ex:
        logger.exception(
            "Engine failed with error: %r. Switching over." % repr(ex)
        )
        engines.mark_failed(database, engine_data)
        engine_data = _get_engine(database, recycle=True)
        engine = engine_data.get("engine")
        try:
            conn = engine.connect()
        except sqla_exc.OperationalError:
            engines.mark_failed(database, engine_data)
            logger.exception("Failed to connect to the database")
            raise
    return conn


@contextlib.contextmanager
def connection(database):
    """
    Context manager for a database connection.

    Used by the:
    with connection("Foo") as conn:
        conn.execute("...")
        ...
    paradigm.

    Begins a database transaction for the requester. Cleans up appropriately
    on error or successful transaction.

    :param database: a name of database engine managed by tincture.
    :yields: a database connection to the requester.
    """
    conn = get_connection(database)
    transaction = conn.begin()
    try:
        yield conn
    except sqla_exc.OperationalError:
        logger.exception("Failed to execute sql statement.")
        transaction.rollback()
        conn.close()
        raise
    except sqla_exc.DBAPIError:
        logger.exception("Failed to execute transaction.")
        transaction.rollback()
        conn.close()
        raise
    except Exception:
        logger.exception("Unknown exception occurred during transaction.")
        transaction.rollback()
        conn.close()
        raise
    else:
        transaction.commit()
        conn.close()


def get_orm_session(database):
    """
    Retrieves a sqlalchemy orm session for the database reference provided.

    :param database: a name of database engine managed by tincture.
    :return: a session.
    """
    engine_data = _get_engine(database)
    engine = engine_data.get("engine")
    try:
        engine.connect()
        session = engine_data.get("session_class")()
    except sqla_exc.OperationalError, ex:
        logger.exception(
            "Engine failed with error: %r. Switching over." % repr(ex)
        )
        engines.mark_failed(database, engine_data)
        engine_data = _get_engine(database, recycle=True)
        engine = engine_data.get("engine")
        try:
            engine.connect()
            session = engine_data.get("session_class")()
        except sqla_exc.OperationalError:
            engines.mark_failed(database, engine_data)
            logger.exception("Failed to connect to the database")
            raise
    return session


@contextlib.contextmanager
def orm_session(database):
    """
    Context manager for a database connection.

    Used by the:
    with orm_session("Foo") as session:
        session.add(object)
        ...
    paradigm.

    Begins a sqlalchemy orm session for the requester. Cleans up appropriately
    on error or successful transaction.

    :param database: a name of database engine managed by tincture.
    :yields: a database connection to the requester.
    """
    session = get_orm_session(database)
    connection = session.connection()
    transaction = connection.begin()
    try:
        yield session
    except sqla_exc.OperationalError:
        logger.exception("Failed to execute sql statement.")
        transaction.rollback()
        raise
    except sqla_exc.DBAPIError:
        logger.error("Failed to execute transaction.")
        transaction.rollback()
        raise
    else:
        session.commit()
    finally:
        session.close()
        connection.close()
