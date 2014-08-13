# -*- coding: utf-8 -*-

import socket
from netkit.stream import Stream


class TcpClient(object):
    """
    封装过的tcp client
    """

    box_class = None
    host = None
    port = None
    timeout = None
    stream = None

    def __init__(self, box_class, host, port, timeout=None):
        self.box_class = box_class
        self.host = host
        self.port = port
        self.timeout = timeout

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)
        self.stream = Stream(sock)

    def connect(self):
        """
        连接服务器，失败会抛出异常
        :return:
        """
        address = (self.host, self.port)
        self.stream.sock.connect(address)

    def read(self):
        """
        如果超时会抛出异常 socket.timeout
        :return:
        """
        data = self.stream.read_with_checker(self.box_class.instance().check)
        if not data:
            return None

        box = self.box_class()
        box.unpack(data)

        return box

    def write(self, data):
        """
        写入
        :param data:
        :return:    True/False
        """
        if isinstance(data, self.box_class):
            data = data.pack()

        return self.stream.write(data)

    def close(self):
        return self.stream.close()

    def closed(self):
        return self.stream.closed()
