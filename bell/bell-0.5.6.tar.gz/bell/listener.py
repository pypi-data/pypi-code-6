# coding=utf8


"""
bell.listener
~~~~~~~~~~~~~

Receive metrics from carbon-relay over ctp and unpack them, then put
metrics to job queue.
"""

from fnmatch import fnmatch
import cjson
import socket
import struct
from struct import Struct

from bell.logger import logger
from bell.base import serve_wrapper, Service
from bell.configs import configs
from bell.utils import pickle, recvall


class Listener(Service):

    name = 'listener'

    def __init__(self):
        super(Listener, self).__init__()
        self.beans = None
        self.sock = None
        self.conn = None

    def initialize(self):
        self.host = configs['listener']['host']
        self.port = configs['listener']['port']
        self.initialize_logger()
        self.beans = self.initialize_beans(as_user=True)
        self.bind()
        self.accept()

    def bind(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.sock.setblocking(1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)  # max queued connection number

    def accept(self):
        if self.conn:  # close current conn if it's alive
            self.conn.close()
        logger.info('Listening over tcp on %s:%d..', self.host, self.port)
        (self.conn, address) = self.sock.accept()
        logger.info('Accepted connection from %s:%d', *address)

    def recv(self):
        buf = recvall(self.conn, 4)
        if buf:
            size = Struct('!I').unpack(buf)[0]
            body = Struct('!%ss' % size).unpack(recvall(self.conn, size))[0]
            body, tail = body[:-1], body[-1]
            assert tail == '\x00'  # buffer tailed with a '\x00'
            metrics = cjson.decode(body)
            return metrics
        logger.warn('Connection lost..')
        self.accept()
        return self.recv()

    def queue(self, metric):
        job = pickle.dumps(metric)
        self.beans.put(job)
        logger.info('Queued: %s', metric)

    def match(self, name):
        matches = configs['listener']['patterns']['matches']
        ignores = configs['listener']['patterns']['ignores']

        for pattern in matches:
            if fnmatch(name, pattern):
                for ignore in ignores:
                    if fnmatch(name, ignore):
                        return False
                else:
                    return True
        return False

    def shutdown(self):
        if self.beans:
            self.beans.close()
        if self.conn:
            self.conn.close()
            self.sock.close()

    @serve_wrapper
    def serve(self):
        self.initialize()

        while 1:
            try:
                metrics = self.recv()
            except (struct.error, ValueError) as e:
                logger.warn('Bad data received: %r, dropping..', e)
                continue
            for metric in metrics:
                if self.match(metric[0]) and metric[1][1] is not None:
                    self.queue(metric)


listener = Listener()
