# -*- coding: utf-8 -*-
from .frame import HeartbeatFrame
from .spec import ConnectionClose, FRAME_ERROR

# TODO fix this


class HeartbeatMonitor(object):

    frame = HeartbeatFrame.pack()

    def __init__(self, protocol, interval, timeout=None):
        self.protocol = protocol
        self.interval = interval
        self.timeout = timeout or interval * 2
        self.on_timeout = None

    def start(self, interval=None, timeout=None):
        self.send(interval)
        self.monitor(timeout)

    def send(self, interval=None):
        if interval:
            self.interval = interval
            self.monitor = interval * 2
        protocol = self.protocol
        protocol._send_frame(self.frame)
        protocol.loop.call_later(self.interval, self.send)

    def monitor(self, timeout=None):
        if timeout:
            self.timeout = timeout
        self.on_timeout = self.protocol.loop.call_later(self.timeout,
                                                        self.timed_out)

    def timed_out(self, FRAME_ERROR=FRAME_ERROR):
        self.protocol.send_method(
            0, ConnectionClose,
            (FRAME_ERROR, 'Heartbeat timed out', 0, 0),
        )

    def maybe_received(self):
        if self.on_timeout is not None:
            self.on_timeout.cancel()
            self.monitor()
