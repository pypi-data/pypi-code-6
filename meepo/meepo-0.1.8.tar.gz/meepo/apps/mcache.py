# -*- coding: utf-8 -*-

"""
    meepo.apps.mrcache
    ~~~~~~~~~~~~~~~~~~

    Meepo Redis Cache App.

    This app will automatically generate a redis cache layer on top of
    the database, and update it in real time.
"""

import click

import sqlalchemy as sa
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.exc import SQLAlchemyError

from meepo.replicator import ZmqReplicator


class RedisCacheReplicator(ZmqReplicator):
    def __init__(self, table_callbacks=None):
        self.table_callbacks = table_callbacks


repl = ZmqReplicator(config.ZMQ_FORWARDER)


@click.command()
@click.option("-b", "--blocking", is_flag=True)
@click.option('-m', '--master_dsn')
@click.option('-s', '--slave_dsn')
@click.argument('tables', nargs=-1)
def main(bind, db_dsn, redis_dsn, tables, blocking=False):
    """Redis cache subscriber.

    Serialization process by providing a {table: callback} mapping.
    """
    logger = logging.getLogger("meepo.sub.rcache_sub")

    if not callable(namespace):
        namespace = lambda: namespace if namespace else "meepo:rcache"

    if not table_callbacks:
        # sqlalchemy reflection
        logger.info("reflecting database: {}".format(db_dsn))
        engine = sa.create_engine(db_dsn)
        base = automap_base()
        base.prepare(engine=engine, reflect=True)
        Session = scoped_session(sessionmaker(bind=engine))

        def _table_cb(table, pk):
            Model = base.classes[table]
            obj = Session.query(Model).get(pk)
            return obj.__dict__

    for table in set(tables):
        def _sub(pk, table=table):
            key = "%s:%s" % (namespace(), table)
            try:
                pass
            except redis.ConnectionError:
                logger.error("event sourcing failed: %s" % pk)
            except Exception as e:
                logger.exception(e)

        signal("%s_write" % table).connect(
            functools.partial(_sub, "write"), weak=False)
        signal("%s_update" % table).connect(
            functools.partial(_sub, "update"), weak=False)
        signal("%s_delete" % table).connect(
            functools.partial(_sub, "delete"), weak=False)



