import logging

import msgpack

from .handlers import PackStreamHandler  # noqa


def replay_log(fp):
    unpacker = msgpack.Unpacker(fp)
    for record in unpacker:
        logging.getLogger(record['name']).handle(
            logging.makeLogRecord(record))
