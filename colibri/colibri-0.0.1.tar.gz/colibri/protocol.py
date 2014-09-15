# -*- coding: utf-8 -*-
"""
colibri.protocol
~~~~~~~~~~~~~~~~

AMQP implementation as `asyncio` Protocol.

"""
from __future__ import absolute_import

from struct import unpack

from asyncio import Protocol, async

from .spec import FRAME_END
from .exceptions import UnexpectedFrame
from .utils import chunks
from .frame import (FRAME_BY_TYPE, MethodFrame, BodyFrame,
                    HeaderFrame, HeartbeatFrame)
from .heartbeat import HeartbeatMonitor


UNEXPECTED_FRAME_FMT = 'Expected {} but received {}'


class AMQP(Protocol):

    HeartbeatMonitor = HeartbeatMonitor

    def __init__(self, connection):
        self.connection = connection
        self.loop = connection.loop

        self.heartbeat = HeartbeatMonitor(protocol=self, interval=10)
        self.prev = bytes()

        self._wait = None
        self._result = None
        self._callbacks = {}

    def connection_made(self, transport):
        """Called once when the connection is established."""
        self.transport = transport
        self.send_protocol_header()

    def connection_lost(self, exc=None):
        """Called once when the connection is lost."""
        if exc is not None:
            # TODO logging
            pass

    def data_received(self, data, bytes=bytes, len=len,
                      unpack=unpack, async=async, FRAME_BY_TYPE=FRAME_BY_TYPE,
                      FRAME_END=FRAME_END):
        """Main callback, called when `data` is received."""
        channel = self.connection.channel
        # channels = self.connection.channels
        maybe_received_heartbeat = self.heartbeat.maybe_received

        while True:
            # Each frame may be a heartbeat frame
            maybe_received_heartbeat()

            data = self.prev + data
            self.prev = bytes()

            len_data = len(data)
            if len_data < 7:
                self.prev = data
                return

            header = data[:7]
            type_, channel_id, size = unpack('!BHL', header)

            if len_data < size + 8:
                self.prev = data
                return

            payload = data[7:7+size]
            ending = data[7+size]

            if ending != FRAME_END:
                self.transport.close()
                raise UnexpectedFrame(UNEXPECTED_FRAME_FMT.format(
                    FRAME_END, ending
                ))

            frame = FRAME_BY_TYPE[type_]
            if frame != HeartbeatFrame:
                channel(channel_id).handle(frame, payload)
                # channels[channel_id].handle(frame, payload)

            reminder = data[8+size:]
            if not reminder:
                return

            # Next loop
            data = reminder

    def send_protocol_header(self, HEADER=b'AMQP\x00\x00\x09\x01'):
        self.transport.write(HEADER)

    def send_method(self, channel_id, method, payload,
                    message=None, frame_size=None):
        frame = MethodFrame.pack(channel_id, method, payload)
        self._send_frame(frame)
        if message is not None:
            assert frame_size is not None
            self._send_message(channel_id, message, frame_size,
                               method.method_type[0])

    def _send_message(self, channel_id, message, frame_size, class_id):
        header_payload = message.dump_properties(class_id)
        header_frame = HeaderFrame.pack(channel_id, header_payload)
        self._send_frame(header_frame)
        for payload in chunks(message.body, frame_size):
            frame = BodyFrame.pack(channel_id, payload)
            self._send_frame(frame)

    def _send_frame(self, frame):
        self.transport.write(frame)
