# coding=utf8

"""
Ssdb Python Client Library.

Usage::

    >>> from ssdb import SSDBClient
    >>> c = SSDBClient(host='0.0.0.0', port=8888)
    >>> c.set('key', 'val')
    1
    >>> c.get('key')
    'val'
"""


__version__ = '0.1.0'
__author__ = 'hit9'
__license__ = 'bsd2'


import sys
import socket
import threading


if sys.version_info[0] < 3:  # compat
    rawstr = str
    nativestr = str
else:
    rawstr = lambda string: string.encode('utf8', 'replace')
    nativestr = lambda raw_string: raw_string.decode('utf8', 'replace')


# response type mappings
type_mappings = {
    'set': int,
    'setx': int,
    'expire': int,
    'ttl': int,
    'setnx': int,
    'get': str,
    'getset': str,
    'del': int,
    'incr': int,
    'exists': bool,
    'getbit': int,
    'setbit': int,
    'countbit': int,
    'substr': str,
    'strlen': int,
    'keys': list,
    'scan': list,
    'rscan': list,
    'multi_set': int,
    'multi_get': list,
    'multi_del': int,
    'hset': int,
    'hget': str,
    'hdel': int,
    'hincr': int,
    'hexists': bool,
    'hsize': int,
    'hlist': list,
    'hkeys': list,
    'hgetall': list,
    'hscan': list,
    'hrscan': list,
    'hclear': int,
    'multi_hset': int,
    'multi_hget': list,
    'multi_hdel': int,
    'zset': int,
    'zget': int,
    'zdel': int,
    'zincr': int,
    'zexists': bool,
    'zsize': int,
    'zlist': list,
    'zkeys': list,
    'zscan': list,
    'zrscan': list,
    'zrank': int,
    'zrrank': int,
    'zrange': list,
    'zrrange': list,
    'zclear': int,
    'zcount': int,
    'zsum': int,
    'zavg': int,
    'zremrangebyrank': int,
    'zremrangebyscore': int,
    'multi_zset': int,
    'multi_zget': list,
    'multi_zdel': int,
    'qsize': int,
    'qclear': int,
    'qfront': str,
    'qback': str,
    'qget': str,
    'qslice': list,
    'qpush': str,
    'qpush_front': int,
    'qpush_back': int,
    'qpop': str,
    'qpop_front': str,
    'qpop_back': str
}


py_reserved_words = {
    'delete': 'del'
}


status_ok = 'ok'
status_not_found = 'not_found'


class SSDBException(Exception):
    pass


class Connection(threading.local):
    """Ssdb connection object, usage::

        >>> conn = Connection(host='0.0.0.0', port=8888)
        >>> conn.execute(['set', 'key', 'val'])
        1
    """

    def __init__(self, host='0.0.0.0', port=8888, timeout=None):
        self.sock = None
        self.host = host
        self.port = port
        self.timeout = timeout
        self.batch_mode = False
        self.__commands = []  # commands sent cache

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.connect((self.host, self.port))
        self.sock.setblocking(1)  # block mode
        self.sock.settimeout(self.timeout)

    def compile(self, args):
        pattern = '{0}\n{1}\n'
        buffers = [pattern.format(len(str(arg)), arg) for arg in args]
        return ''.join(buffers) + '\n'

    def send(self, args):
        if self.sock is None:
            self.connect()
        command = self.compile(args)
        self.sock.sendall(rawstr(command))
        self.__commands.append(args[0])

    def recv(self):
        data = ''
        resps_count = len(self.__commands)
        while resps_count > 0:
            buf = nativestr(self.sock.recv(1024))
            data += buf
            resps_count -= buf.count('\n\n')
        try:
            resp = self.response(data)
        except Exception:
            raise
        finally:
            self.clear_commands()
        return resp

    def batch(self, mode=True):
        self.batch_mode = mode

    def execute(self, args):
        if self.batch_mode:
            return self.send(args)
        self.send(args)
        return self.recv()

    def clear_commands(self):
        self.__commands[:] = []

    def response(self, data):
        raw_resps = data.strip().split('\n\n')
        bodys = [raw_resp.splitlines()[1::2] for raw_resp in raw_resps]

        resps = []
        for index, lst in enumerate(bodys):
            command = self.__commands[index]
            status, body = lst[0], lst[1:]
            resps.append(self.make_response(status, body, command))

        if self.batch_mode:
            return resps
        return resps[0]

    def make_response(self, status, body, command):
        if status == status_not_found:
            return None
        elif status == status_ok:
            type = type_mappings.get(command, str)
            if type in (bool, int, str):
                return type(body[0])
            elif type is list:
                return type(body)
        else:
            if body:
                error_message = '{}: {}'.format(status, body[0])
            else:
                error_message = status
            raise SSDBException(error_message)


class SSDBClient(object):
    """Ssdb client object, usage::

        >>> c = SSDBClient(host='0.0.0.0', port=8888)
        >>> c.set('key', 'val')
        1
    """

    def __init__(self, host='0.0.0.0', port=8888, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.conn = Connection(host=host, port=port, timeout=timeout)

    def batch(self, mode=True):
        return self.conn.batch(mode)

    def execute(self):
        return self.conn.recv()

    def __getattr__(self, name):
        name = py_reserved_words.get(name, name)

        def method(*args):
            return self.conn.execute((name,) + args)
        return method
