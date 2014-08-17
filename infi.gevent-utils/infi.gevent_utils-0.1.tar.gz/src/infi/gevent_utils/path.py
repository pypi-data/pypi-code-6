"""
This module acts as a replacement to some of Python's `os.path` module where the blocking operations are done in a
gevent-friendly manner.
"""
from __future__ import absolute_import
from os import path as _path
from .deferred import create_threadpool_executed_func

DEFERRED_FUNCTIONS = [
    'realpath', 'islink', 'lexists', 'samefile', 'sameopenfile', 'ismount'
]


module = globals()
for name in DEFERRED_FUNCTIONS:
    module[name] = create_threadpool_executed_func(_path.dict[name])
