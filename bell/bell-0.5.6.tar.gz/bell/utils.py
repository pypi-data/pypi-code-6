# coding=utf8

import os
import sys
import subprocess
from werkzeug.wsgi import pop_path_info, peek_path_info
from werkzeug.serving import run_simple

try:
    import cPickle as pickle
except ImportError:
    import pickle

if sys.version_info[0] < 3:
    from Queue import Queue
else:
    from queue import Queue

from bell._compat import nativestr


def normjoin(*pathes):
    path = os.path.join(*pathes)
    return os.path.normpath(path)


def rsync(src, dest='.'):
    pattern = 'rsync -aqu {0} {1}'
    command = pattern.format(src, dest)
    return subprocess.call(command, shell=True)


def update_nested_dict(dct, other):
    """Inplace update nested dict, usage:
        >>> dct = {'x': {'y': 1}}
        >>> other = {'x': {'y': 3, 'z': 2}, 'w': 4}
        >>> update_nested_dict(dct, other)
        {'x': {'y': 3, 'z': 2}, 'w': 4}
    """

    for key, val in other.items():
        if isinstance(val, dict):
            tmp = dct.setdefault(key, {})
            update_nested_dict(tmp, val)
        else:
            dct[key] = val
    return dct


def recvall(sock, size):
    """Recv all bytes from a socket due to buffer size limit on recv
    functions"""
    data = ''
    while size > 0:
        buf = nativestr(sock.recv(size))
        size -= len(buf)
        data += buf
    return data


class PathDispatcher(object):

    def __init__(self, default_app, prefix):
        self.default_app = default_app
        self.prefix = prefix

    def __call__(self, env, start_response):
        app = self.default_app
        prefix = peek_path_info(env)
        if prefix == self.prefix:
            pop_path_info(env)
            return app(env, start_response)
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return ['Not Found']


class PrefixedApp(object):

    def __init__(self, app, prefix):
        self.wsgi = PathDispatcher(app, prefix)

    def run(self, host, port, use_reloader=True):
        return run_simple(host, port, self.wsgi, use_reloader=use_reloader)
