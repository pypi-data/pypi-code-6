from __future__ import absolute_import

import random
from .exception import FrameError


class Frame(object):
    """
    A partial, text only, implementation of the WebSocket protocol.
    For more info see:
    http://www.altdevblogaday.com/2012/01/23/writing-your-own-websocket-server/
    """
    def __init__(self,  buf):
        # HEADER FIELDS
        self.fin = 0
        self.opcode = 0
        self.payload = 0
        self.mask = 0

        self.key = bytearray()
        self.len = 0
        self.buf = buf
        self.msg = bytearray()
        self.frame_length = 0
        self.isReady()

    def isReady(self):
        buf = self.buf
        if len(buf) < 2:
            raise FrameError("Incomplete Frame: HEADER DATA")
        self.fin = buf[0] >> 7
        self.opcode = buf[0] & 0b1111
        self.payload = buf[1] & 0b1111111
        self.mask = buf[1] >> 7
        buf = buf[2:]
        if self.payload < 126:
            self.len = self.payload
            if self.mask:
                self.frame_length = 6 + self.len
            else:
                self.frame_length = 2 + self.len
            if self.frame_length > len(self.buf):
                raise FrameError("Incomplete Frame: FRAME DATA")
            if len(buf) < 4 and self.mask:
                raise FrameError("Incomplete Frame: KEY DATA")
            if self.mask:
                self.key = buf[:4]
                buf = buf[4:4+len(buf)+1]
            else:
                buf = buf[:self.len]

        elif self.payload == 126:
            if len(buf) < 6 and self.mask:
                raise FrameError("Incomplete Frame: KEY DATA")
            for k, i in [(0, 1), (1, 0)]:
                self.len += buf[k] * 1 << (8*i)
            if self.mask:
                self.frame_length = 8 + self.len
            else:
                self.frame_length = 4 + self.len
            if self.frame_length > len(self.buf):
                raise FrameError("Incomplete Frame: FRAME DATA")
            buf = buf[2:]
            if self.mask:
                self.key = buf[:4]
                buf = buf[4:4+len(buf)+1]
            else:
                buf = buf[:self.len]

        else:
            if len(buf) < 10 and self.mask:
                raise FrameError("Incomplete Frame: KEY DATA")
            for k, i in [(0, 7), (1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1), (7, 0)]:
                self.len += buf[k] * 1 << (8*i)
            if self.mask:
                self.frame_length = 14 + self.len
            else:
                self.frame_length = 10 + self.len
            if self.frame_length > len(self.buf):
                raise FrameError("Incomplete Frame: FRAME DATA")
            buf = buf[8:]
            if self.mask:
                self.key = buf[:4]
                buf = buf[4:4+len(buf)+1]
            else:
                buf = buf[self.len]
        self.msg = buf

    def message(self):
        if not self.mask:
            return self.msg
        decoded_msg = bytearray()
        for i in range(self.len):
            c = self.msg[i] ^ self.key[i % 4]
            decoded_msg.append(c)
        return decoded_msg

    def length(self):
        return self.frame_length

    @staticmethod
    def encodeMessage(buf, key):
        encoded_msg = bytearray()
        buf_len = len(buf)
        for i in range(buf_len):
            c = buf[i] ^ key[i % 4]
            encoded_msg.append(c)
        return encoded_msg

    @staticmethod
    def buildMessage(buf,  mask=True):
        msg = bytearray()
        if mask:
            key = [random.randrange(1, 255) for i in range(4)]
        #first half of header => 10000001
        msg.append(0x81)
        #second byte
        buf_len = len(buf)
        if buf_len < 126:
            msg_header = buf_len
            if mask:
                msg.append(msg_header + (1 << 7))
            else:
                msg.append(msg_header)
            if mask:
                msg.append(key)
                msg.append(Frame.encodeMessage(buf, key))
            else:
                msg += bytearray(buf)
            return msg

        if buf_len <= ((1 << 16) - 1):
            if mask:
                msg.append(126 + (1 << 7))
            else:
                msg.append(126)
            for i in range(1, 3):
                msg_header = (buf_len >> (16 - (8*i))) & (2**8 - 1)
                msg.append(msg_header)
            if mask:
                msg.append(key)
                msg.append(Frame.encodeMessage(buf, key))
            else:
                msg += bytearray(buf)
            return msg

        if buf_len <= ((1 << 64) - 1):
            if mask:
                msg.append(127 + (1 << 7))
            else:
                msg.append(127)
            for i in range(1, 9):
                msg_header = (buf_len >> (64 - (8*i))) & (2**8 - 1)
                msg.append(msg_header)
            if mask:
                msg.append(key)
                msg.append(Frame.encodeMessage(buf, key))
            else:
                msg += bytearray(buf)
            return msg
