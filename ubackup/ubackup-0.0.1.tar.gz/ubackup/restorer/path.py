from __future__ import absolute_import

from .base import Restorer
from subprocess import check_call


class PathRestorer(Restorer):
    def restore(self, stream, path):
        check_call(
            ['tar -xp'],
            stdin=stream,
            cwd=path,
            shell=True)
