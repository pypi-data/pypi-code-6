# -*- coding: utf-8 -*-
"""
colibri.frame
~~~~~~~~~~~~~

This module contains classes that represent different kinds of AMQP
frames.

"""
from contextlib import contextmanager

from asyncio import Lock, Future, async

from .serialization import dumps
from .message import load_properties, BasicMessage
from .spec import (select_method, FRAME_METHOD, FRAME_HEADER,
                   FRAME_BODY, FRAME_HEARTBEAT, FRAME_END, METHODS,
                   BasicReturn, BasicDeliver, BasicGetOK)
from .exceptions import UnexpectedFrame

__all__ = ['MethodFrame', 'HeaderFrame', 'BodyFrame',
           'HeartbeatFrame', 'FrameHandler', 'FRAME_BY_TYPE']


def pack(frame_type, channel_id, payload, dumps=dumps, frame_end=FRAME_END):
    return (dumps('oBl', (frame_type, channel_id, len(payload))) +
            payload + dumps('o', FRAME_END))


class FrameMeta(type):

    def __eq__(cls, other):
        return cls.frame_type == other.frame_type

    def __neq__(cls, other):
        return cls.frame_type != other.frame_type


class MethodFrame(object, metaclass=FrameMeta):

    frame_type = FRAME_METHOD

    @classmethod
    def pack(cls, channel_id, method, payload):
        return pack(cls.frame_type, channel_id, method.pack(payload))

    @classmethod
    def unpack(cls, payload, select_method=select_method):
        method_type, payload = payload[:4], payload[4:]
        method = select_method(method_type)
        return method.unpack(payload), method


class HeaderFrame(object, metaclass=FrameMeta):

    frame_type = FRAME_HEADER

    properties = BasicMessage.PROPERTIES

    @classmethod
    def pack(cls, channel_id, payload, pack=pack):
        return pack(cls.frame_type, channel_id, payload)

    @classmethod
    def unpack(cls, payload, load_properties=load_properties):
        return load_properties(payload, cls.properties)


class BodyFrame(object, metaclass=FrameMeta):

    frame_type = FRAME_BODY

    @classmethod
    def pack(cls, channel_id, payload, pack=pack):
        return pack(cls.frame_type, channel_id, payload)

    @classmethod
    def unpack(cls, payload):
        return payload


class HeartbeatFrame(object, metaclass=FrameMeta):

    frame_type = FRAME_HEARTBEAT

    @classmethod
    def pack(cls, pack=pack):
        return pack(cls.frame_type, 0, b'')

    @classmethod
    def unpack(cls, payload):
        return payload


FRAME_BY_TYPE = {
    FRAME_METHOD: MethodFrame,
    FRAME_HEADER: HeaderFrame,
    FRAME_BODY: BodyFrame,
    FRAME_HEARTBEAT: HeartbeatFrame,
}


UNEXPECTED_FRAME_FMT = 'Expected {} but received {}'


class FrameHandler(object):

    def __init__(self, channel):
        self.channel = channel
        self.loop = channel.loop

        self.partial_message = None
        self.callbacks = {}

        self.expected_frame = None
        self.expected_methods = ()
        self.response = None

        self.lock = Lock(loop=self.loop)

    def update(self, d):
        self.callbacks.update(d)

    @contextmanager
    def wait_for(self, *expected):
        yield from self.lock.acquire()
        self.expected_frame = MethodFrame
        self.expected_methods = expected
        r = self.response = Future(loop=self.loop)
        # Some methods may not wait for the reply
        # In this case the code below will allow to instantly return
        # when yielding from r
        if expected[0] is None:
            r.set_result(None)
        try:
            yield r
        finally:
            self.expected_frame = None
            self.expected_methods = ()
            self.response = None
            self.lock.release()

    def ready(self, result=None):
        self.response.set_result(result)

    def handle(self, frame, payload,
               CONTENT_SPEC=(BasicReturn, BasicDeliver, BasicGetOK)):
        # At first, check if an unexpected frame was received
        response = self.response
        if self.expected_frame is not None and frame != self.expected_frame:
            exc = UnexpectedFrame(UNEXPECTED_FRAME_FMT.format(
                self.expected_frame, frame
            ))
            response.set_exception(exc)
            return
        if frame == MethodFrame:
            payload, method = frame.unpack(payload)
            if method.synchronous:
                # Check of an unexpected method was received
                if not any(method == cls for cls in self.expected_methods):
                    exc = UnexpectedFrame(UNEXPECTED_FRAME_FMT.format(
                        self.expected_methods, method
                    ))
                    response.set_exception(exc)
                    return
            if any(method == cls for cls in CONTENT_SPEC):
                self.partial_message = BasicMessage()
                self.expected_frame = HeaderFrame
            else:
                try:
                    callback = self.callbacks[method.method_type]
                except KeyError:
                    # Recieved reply and there is no handler for it
                    if method.method_type not in METHODS:
                        raise Exception('Unknown method')
                    self.ready(payload)
                else:
                    # Schedule task to handle the method
                    async(callback(*payload))
        elif frame == HeaderFrame:
            msg = self.partial_message
            msg.add_header(payload)
            if msg._ready:
                # Bodyless message
                self.partial_message = None
                response.set_result(msg)
            else:
                self.expected_frame = BodyFrame
        elif frame == BodyFrame:
            msg = self.partial_message
            msg.add_body_chunk(payload)
            if msg._ready:
                self.partial_message = None
                response.set_result(msg)
                self.expected_frame = None
