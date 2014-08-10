from __future__ import absolute_import

from .base import Creator
from ubackup.utils import stream_shell, gzip_stream, md5_stream

import logging
logger = logging.getLogger(__name__)


class PathCreator(Creator):
    TYPE = "path"

    def __init__(self, path):
        self.path = path

    @property
    def data(self):
        return {
            'path': self.path
        }

    @property
    def unique_name(self):
        return "path-" + self.path

    def checksum(self):
        logger.info('Process checksum for %s' % self.path)
        return md5_stream(stream_shell(
            cmd='tar -cp .',
            cwd=self.path))

    def create(self):
        logger.info('Creating backup for %s' % self.path)
        return gzip_stream(stream_shell(
            cmd='tar -cp .',
            cwd=self.path))
