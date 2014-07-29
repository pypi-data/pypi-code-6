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


__version__ = '0.1.4'
__author__ = 'hit9'
__license__ = 'bsd2'


import sys
import socket
import threading
import contextlib


if sys.version_info[0] < 3:  # unicode issue compat
    def nativestr(s):
        if isinstance(s, unicode):
            return s.encode('utf8', 'replace')
        return str(s)
    rawstr = nativestr
else:
    def rawstr(s):
        return bytes(str(s).encode('utf8', 'replace'))

    def nativestr(s):
        if isinstance(s, bytes):
            s = s.decode('utf8', 'replace')
        return str(s)


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
    'hrlist': list,
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
    'zrlist': list,
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
    'zavg': float,
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
    'qpop_back': str,
    'qlist': list,
    'qrlist': list,
    'info': list
}


py_reserved_words = {
    'delete': 'del'
}


status_ok = 'ok'
status_not_found = 'not_found'


class SSDBException(Exception):
    pass


class ResponseParser(object):

    def __init__(self, sock):
        self.sock = sock

    def read_bytes(self, size):
        return nativestr(self.sock.recv(size))

    def read_unit(self):
        length = ''
        while 1:
            buf = self.read_bytes(1)
            if buf == '\n':
                break
            length += buf
        if length:  # when length != ''
            length = int(length)
            data = self.read_bytes(length)
            assert self.read_bytes(1) == '\n'
            return data
        return None  # when buf == '\n', length == ''

    def parse(self, resps_count):
        resp_datas = []

        while resps_count > 0:
            resp_data = []
            status = self.read_unit()
            resp_data.append(status)

            # try to read bodys
            while 1:
                body = self.read_unit()
                if body is None:
                    break
                resp_data.append(body)
            resp_datas.append(resp_data)
            resps_count -= 1
        return resp_datas


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
        self.parser = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.connect((self.host, self.port))
        self.sock.setblocking(1)  # block mode
        self.sock.settimeout(self.timeout)
        self.parser = ResponseParser(self.sock)

    def compile(self, args):
        pattern = '{0}\n{1}\n'
        buffers = [pattern.format(len(rawstr(arg)), nativestr(arg))
                   for arg in args]
        return ''.join(buffers) + '\n'

    def send(self):
        if self.sock is None:
            self.connect()
        command = ''.join(list(map(self.compile, self.__commands)))
        self.sock.sendall(rawstr(command))

    def recv(self):
        resp_datas = self.parser.parse(len(self.__commands))

        try:
            resp = self.response(resp_datas)
        except Exception:
            raise
        finally:
            self.clear_commands()
        return resp

    def batch(self, mode=True):
        self.batch_mode = mode

    def append_command(self, args):
        self.__commands.append(args)

    def clear_commands(self):
        self.__commands[:] = []

    def execute(self):
        self.send()
        return self.recv()

    def response(self, resp_datas):
        resps = []
        for index, resp_data in enumerate(resp_datas):
            command = self.__commands[index][0]
            status, body = resp_data[0], resp_data[1:]
            resps.append(self.make_response(status, body, command))

        if self.batch_mode:
            return resps
        return resps[0]

    def make_response(self, status, body, command):
        if status == status_not_found:
            return None
        elif status == status_ok:
            type = type_mappings.get(command, str)
            if type in (int, float, str):
                return type(body[0])
            elif type is bool:
                return bool(int(body[0]))
            elif type is list:
                return list(body)
        else:
            if body:
                error_message = '{}: {}'.format(status, body[0])
            else:
                error_message = status
            raise SSDBException(error_message)


class BaseClient(object):

    def __getattr__(self, name):
        name = py_reserved_words.get(name, name)

        def method(*args):
            self.conn.append_command((name,) + args)
            if not self.conn.batch_mode:
                return self.conn.execute()
        return method


class Pipeline(BaseClient):

    def __init__(self, conn):
        self.conn = conn

    def execute(self):
        return self.conn.execute()


class SSDBClient(BaseClient):
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

    @contextlib.contextmanager
    def pipeline(self):
        self.conn.batch(True)
        yield Pipeline(self.conn)
        self.conn.batch(False)
