# -*- coding: utf-8 -*-
from logging import handlers


REDIS_HOST = 'localhost'
REDIS_PORT= 6379


class SocketHandler(handlers.SocketHandler):
    def emit(self, record):
        try:
            self.send(self.format(record))
        except Exception:
            self.handleError(record)


class DatagramHandler(handlers.DatagramHandler):
    def emit(self, record):
        try:
            self.send(self.format(record))
        except Exception:
            self.handleError(record)


class RedisHandler(handlers.SocketHandler):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=None):
        super().__init__(host, port)

        self.password = password

    def send(self, s):
        if self.sock is None:
            self.createSocket()
            if not self.sock:
                return
            if self.password:
                self.auth(self.password)

        super().send(s)

    def build_command(self, command, *args):
        """
        Build a redis command using RESP
        """
        l = [
            '*{}'.format(len(args)+1),
            '${}'.format(len(command)),
            command,
            ]
    
        for arg in args:
            arg = str(arg)
            l.append('${}'.format(len(arg)))
            l.append(arg)

        l.append('')

        return '\r\n'.join(l).encode('latin-1')

    def execute_command(self, command, *args):
        self.send(self.build_command(command, *args))

    def auth(self, password):
        self.execute_command('AUTH', password)


class RedisListHandler(RedisHandler):
    def __init__(self, list_name, list_maxsize=1024, host=REDIS_HOST, port=REDIS_PORT, password=None):
        self.list_name = list_name
        self.list_maxsize = list_maxsize

        super().__init__(host, port, password)

    def rpush(self, name, *values):
        self.execute_command('RPUSH', name, *values)

    def ltrim(self, name, start, end):
        self.execute_command('LTRIM', name, start, end)

    def emit(self, record):
        try:
            self.rpush(self.list_name, self.format(record))
            if self.list_maxsize:
                self.ltrim(self.list_name, -self.list_maxsize, -1)
        except Exception:
            self.handleError(record)


class RedisPublishHandler(RedisHandler):
    def __init__(self, channel, host=REDIS_HOST, port=REDIS_PORT, password=None):
        self.channel = channel

        super().__init__(host, port, password)

    def publish(self, channel, message):
        self.execute_command('PUBLISH', channel, message)

    def emit(self, record):
        try:
            self.publish(self.channel, self.format(record))
        except Exception:
            self.handleError(record)
