from __future__ import absolute_import

from .base import Restorer


class MysqlRestorer(Restorer):
    def restore(self, stream, databases):
        pass
