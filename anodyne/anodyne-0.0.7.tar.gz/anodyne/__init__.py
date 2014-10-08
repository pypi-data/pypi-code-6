import logging

from sqlalchemy import exc as sqla_exc
from sqlalchemy import event as sqla_event
from sqlalchemy import pool as sqla_pool

logger = logging.getLogger(__name__)

enable_disconnect_rebound = True


@sqla_event.listens_for(sqla_pool.Pool, "checkout")
def disconnect_rebound(dbapi_connection, connection_record, connection_proxy):
    """
    Stolen largely from:
        http://docs.sqlalchemy.org/en/rel_0_8/core/pooling.html#disconnect-handling-pessimistic

    The purpose of this callback is to attempt health checks on a cursor
    before it is given back to an engine from a connection pool. The
    default behavior is to attempt a SELECT 1 cursor execution up to three
    times before re-raising or notifying the requester of a bad connection.

    :param dbapi_connection:
    :param connection_record:
    :param connection_proxy:
    :return:
    """
    if enable_disconnect_rebound:
        cursor = dbapi_connection.cursor()
        try:
            cursor.execute("SELECT 1")
        except:
            # optional - dispose the whole pool
            # instead of invalidating one at a time
            # connection_proxy._pool.dispose()

            # raise DisconnectionError - pool will try
            # connecting again up to three times before raising.
            logger.exception(
                "Failed to establish connection for %r" % repr(dbapi_connection)
            )
            raise sqla_exc.DisconnectionError()
        cursor.close()