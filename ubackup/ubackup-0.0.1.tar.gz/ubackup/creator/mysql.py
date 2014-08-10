from __future__ import absolute_import

from .base import Creator
from ubackup.utils import stream_shell, gzip_stream, md5_stream

import logging
logger = logging.getLogger(__name__)


class MysqlCreator(Creator):
    TYPE = "mysql"

    def __init__(self, databases):
        self.databases = databases

    @property
    def data(self):
        return {
            'databases': self.databases
        }

    @property
    def unique_name(self):
        return "mysql-" + "-".join(self.databases)

    def mysql_dump(self):
        cmd = 'mysqldump -uroot --skip-comments'

        if len(self.databases) == 0:
            cmd += ' --all-databases'
        else:
            cmd += ' --databases %s' % " ".join(self.databases)
        return stream_shell(cmd)

    def checksum(self):
        logger.info('Process checksum for MySQL')
        return md5_stream(self.mysql_dump())

    def create(self):
        logger.info('Creating a MySQL backup')
        return gzip_stream(self.mysql_dump())
