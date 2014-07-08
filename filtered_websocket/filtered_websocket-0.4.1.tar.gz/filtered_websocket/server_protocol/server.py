from __future__ import absolute_import

import uuid
import re
import hashlib
import base64
from twisted.internet.protocol import Protocol as BaseProtocol
from .exception import FrameError, ProtocolError
from .frame import Frame


class Protocol(BaseProtocol, object):

    def __init__(self, users=None):
        if users is None:
            users = {}
        self.bufferIn = bytearray()
        self.bufferOut = bytearray()
        self.users = users
        self.id = uuid.uuid4()
        self.users[self.id] = self
        self.websocket_ready = False

    @staticmethod
    def buildHandshakeHeader(key):
        _response = b""
        _response += b"HTTP/1.1 101 Web Socket Protocol Handshake\r\n"
        _response += b"Upgrade: WebSocket\r\n"
        _response += b"Connection: Upgrade\r\n"
        _response += b"Sec-WebSocket-Accept: "
        _response += key
        _response += b"\r\n\r\n"
        return _response

    def buildHandshake(self):
        buf = self.bufferIn
        pos_check = re.compile(b"\r\n\r\n")
        pos = pos_check.search(buf)
        if pos is None:
            raise ProtocolError("Incomplete Handshake")
        pos = pos.span()[0]
        self.onHandshake(buf)
        cmd = buf[:pos+5]
        self.bufferIn = buf[pos+4:]
        key_check = re.compile(b"Sec-WebSocket-Key:\s*(\S+)\s*")
        key = key_check.search(cmd)
        if not key:
            raise Exception("Missing Key")
        key = key.group(1)
        self.key = key
        key = bytes(key) + b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
        key = base64.b64encode(hashlib.sha1(key).digest())
        handshake = Protocol.buildHandshakeHeader(key)
        return handshake

    def sendHandshake(self):
        try:
            hc = self.buildHandshake()
        except ProtocolError:
            pass
        except Exception as e:
            print(e)
            self.transport.abortConnection()
        else:
            self.transport.write(hc)
            self.websocket_ready = True

    def dataReceived(self, data):
        self.bufferIn += data
        if not self.websocket_ready:
            self.sendHandshake()
            self.onConnect()
        else:
            try:
                frame = Frame(self.bufferIn)
            except FrameError:
                pass
            else:
                f_len = frame.length()
                self.bufferIn = self.bufferIn[f_len:]
                self.onMessage(frame.message())

    def connectionLost(self, *args, **kwargs):
        if self.id in self.users:
            del self.users[self.id]
        self.onDisconnect()

    def loseConnection(self):
        if self.id in self.users:
            del self.users[self.id]
        self.onDisconnect()
        self.transport.loseConnection()

    def abortConnection(self):
        if self.id in self.users:
            del self.users[self.id]
        self.onDisconnect()
        self.transport.abortConnection()

    def sendMessage(self, msg):
        self.bufferOut += Frame.buildMessage(msg, mask=False)
        if not self.websocket_ready:
            return
        self.transport.write(bytes(self.bufferOut))
        self.bufferOut = bytearray()

    def onHandshake(self, header):
        pass

    def onConnect(self):
        pass

    def onDisconnect(self):
        pass

    def onMessage(self, msg):
        pass
