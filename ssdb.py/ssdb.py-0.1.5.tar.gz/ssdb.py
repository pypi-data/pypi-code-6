# coding=utf8

"""
Python client for https://github.com/ideawu/ssdb
"""

__version__ = '0.1.5'
__license__ = 'basd2'


import sys
import socket
import threading
import contextlib


if sys.version > '3':
    # binary: cast str to bytes
    binary = lambda string: bytes(string, 'utf8')
    # string: cast bytes to native string
    string = lambda binary: binary.decode('utf8')
else:
    binary = str
    string = str


commands = {
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


class SSDBException(Exception):
    pass


class Connection(threading.local):

    def __init__(self, host='0.0.0.0', port=8888):
        self.host = host
        self.port = port
        self.sock = None
        self.commands = []

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setblocking(1)
        self.sock.connect((self.host, self.port))

    def compile(self, args):
        lst = []
        pattern = '%d\n%s\n'

        for arg in args:
            size = len(binary(str(arg)))
            lst.append(pattern % (size, arg))
        lst.append('\n')
        # native string
        return ''.join(lst)

    def build(self, type, data):
        if type in (int, str, float):
            return type(data[0])
        elif type is bool:
            return bool(int(data[0]))
        elif type is list:
            return data

    def fix_types(self, cmd, data):
        # zset score should be int
        if cmd in ('zscan', 'zrscan', 'zrange', 'zrrange', 'multi_zget'):
            for index, score in enumerate(data):
                if index % 2 == 1:
                    data[index] = int(score)
        return data

    def request(self):
        if self.sock is None:
            self.connect()
        cmds = list(map(self.compile, self.commands))
        self.sock.sendall(binary(''.join(cmds)))
        chunks = parse(self.sock, len(self.commands))
        resps = []

        for index, chunk in enumerate(chunks):
            cmd = self.commands[index]
            status, body = chunk[0], chunk[1:]
            if status == 'ok':
                data = self.build(commands[cmd[0]], body)
                data = self.fix_types(cmd[0], data)
                resps.append(data)
            elif status == 'not_found':
                resps.append(None)
            else:
                raise SSDBException('%r on command %r', status, cmd)

        self.commands[:] = []
        return resps


class BaseClient(object):

    def __init__(self):
        def create_method(command):
            def method(*args):
                self.conn.commands.append((command, ) + args)
                if not isinstance(self, Pipeline):
                    return self.conn.request()[0]
            return method

        for command in commands:
            name = {'del': 'delete'}.get(command, command)
            setattr(self, name, create_method(command))


class Client(BaseClient):

    def __init__(self, host='0.0.0.0', port=8888):
        super(Client, self).__init__()
        self.host = host
        self.port = port
        self.conn = Connection(host=host, port=port)

    @contextlib.contextmanager
    def pipeline(self):
        yield Pipeline(self.conn)


class Pipeline(BaseClient):

    def __init__(self, conn):
        super(Pipeline, self).__init__()
        self.conn = conn

    def execute(self):
        return self.conn.request()


def recv_all(sock, size):
    data = binary('')
    while size > 0:
        buf = sock.recv(size)
        size -= len(buf)
        data += buf
    return data


def recv_ch(sock):
    return sock.recv(1)


def recv_until(sock, ch):
    data = binary('')
    while 1:
        buf = recv_ch(sock)
        if buf == ch:
            break
        data += buf
    return data


def parse(sock, count):
    chunk = []
    chunks = []
    n = binary('\n')

    while count > 0:
        buf = recv_until(sock, n)
        if not buf:
            chunks.append(chunk)
            chunk = []
            count -= 1
            continue
        size = int(buf)
        body = recv_all(sock, size)
        chunk.append(string(body))
        assert n == recv_ch(sock)
    return chunks
