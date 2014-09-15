# -*- coding: utf-8 -*-
"""
colibri.connection
~~~~~~~~~~~~~~~~~~

AMQP connections.

"""
from __future__ import absolute_import

from array import array

from asyncio import coroutine, get_event_loop

from . import __version__, spec
from .protocol import AMQP
from .channel import Channel
from .frame import FrameHandler
from .serialization import dumps
from .utils import cached_property, YieldFromContextManager
from .log import get_logger

log = get_logger(__name__)


LIBRARY_PROPERTIES = {
    'product': 'colibri',
    'product_version': __version__,
    'capabilities': {},
}


class Connection(object):
    """This class represents a connection to AMQP broker"""

    #: Protocol implementation
    AMQP = AMQP

    #: AMQP channel implementation
    Channel = Channel

    def __init__(self, host='localhost', port=5672,
                 userid='guest', password='guest',
                 virtual_host='/', login_method='AMQPLAIN',
                 login_response=None, locale='en_US', client_properties=None,
                 ssl=False, connect_timeout=None, channel_max=None,
                 frame_max=None, heartbeat_interval=0, on_open=None,
                 on_blocked=None, on_unblocked=None, confirm_publish=False,
                 on_tune_ok=None, loop=None, **kwargs):
        channel_max = self.channel_max = channel_max or 65535
        self.frame_max = frame_max or 131072

        if login_response is None:
            if userid is not None and password is not None:
                if isinstance(userid, str):
                    userid = userid.encode('utf-8')
                if isinstance(password, str):
                    password = password.encode('utf-8')
                login_response = dumps('F', {'LOGIN': userid,
                                             'PASSWORD': password})
                # Skip the length at the beginning
                login_response = login_response[4:]

        self.host = host
        self.port = port
        self.client_properties = dict(
            LIBRARY_PROPERTIES, **client_properties or {}
        )
        self.client_properties.setdefault('capabilities', {})

        self.login_method = login_method
        self.login_response = login_response
        self.locale = locale
        self.virtual_host = virtual_host
        self.ssl = ssl

        self.client_heartbeat = heartbeat_interval

        self._available_channel_ids = array('H', range(channel_max, 0, -1))

        self.version_major = 0
        self.version_minor = 0
        self.server_properties = {}
        self.mechanisms = []
        self.locales = []

        self.confirm_publish = confirm_publish

        # Callbacks
        self.on_open = on_open
        self.on_blocked = on_blocked
        self.on_unblocked = on_unblocked

        self.loop = loop or get_event_loop()

        self.channel_id = 0
        self.channels = {0: self}  # self.Channel(self, 0)}

        self.handler = FrameHandler(self)
        self.handle = self.handler.handle

        self._setup_callbacks()

    def send_method(self, method, payload, message=None,
                    frame_size=None, channel_id=None):
        # This method is private and should not be used directly
        if self.protocol is None:
            raise Exception('Call `open` method at first')
        channel_id = channel_id or self.channel_id
        protocol = self.protocol
        # if protocol.closing.done():
        #     raise Exception('Channel #{} is closed'.format(channel_id))
        protocol.send_method(channel_id, method, payload,
                             message=message, frame_size=frame_size)

    @cached_property
    def protocol(self):
        return self.AMQP(self)

    def open(self, host=None, port=None, reply_method=spec.ConnectionStart):
        """Open connection to AMQP broker.

        :keyword host: Override `host` specified in constructor.
        :keyword port: Override `port` specified in constructor.
        """
        host, port = host or self.host, port or self.port
        with self.handler.wait_for(reply_method) as fut:
            yield from self.loop.create_connection(
                lambda: self.protocol, host=host, port=port
            )
            return (yield from fut)

    def __enter__(self):
        raise RuntimeError(
            '"yield from" should be used as context manager exception')

    def __exit__(self, *args):
        pass

    def __iter__(self):
        # This is not a coroutine.  It is meant to enable the idiom:
        #
        #     with (yield from conn):
        #         <block>
        #
        # as an alternative to:
        #
        #     yield from conn.open()
        #     try:
        #         <block>
        #     finally:
        #         conn.close()
        yield from self.open()
        return YieldFromContextManager(self)

    def close(self, reply_code=0, reply_text='', class_id=0, method_id=0,
              method=spec.ConnectionClose,
              reply_method=spec.ConnectionCloseOK):
        """Close connection to AMQP broker.

        :keyword reply_code: The reply code. Must be one of constants defined
            in `colibri.spec`.
        :keyword reply_text: Localized reply text. This text can be logged
            as an aid to resolving issues.
        :keyword class_id: Tell the broker which method (class)
            caused the close.
        :keyword method_id: Tell the broker which method (ID)
            caused the close.
        """
        with self.handler.wait_for(reply_method) as fut:
            self.send_method(
                method, (reply_code, reply_text, class_id, method_id),
            )
            return (yield from fut)

    def channel(self, channel_id=None, on_open=None):
        """Get channel instance. If channel with `channel_id` does not exist,
        it will be created.

        :keyword channel_id: Channel ID. If set to None (default value),
            channel id will be chosen from available channel ids.
        :keyword on_open: Optional callback, must accept a single
            argument - channel instance.
        """
        try:
            return self.channels[channel_id]
        except KeyError:
            chan = self.Channel(self, channel_id, on_open=on_open)
            self.channels[channel_id] = chan
            return chan

    def _get_free_channel_id(self):
        try:
            return self._available_channel_ids.pop()
        except IndexError:
            raise Exception(
                'No free channel ids, current={}, channeld_max={}'.format(
                    len(self.channels), self.channel_max)
            )

    def _claim_channel_id(self, channel_id):
        try:
            return self._available_channel_ids.remove(channel_id)
        except ValueError:
            raise Exception('Channel #{} already open'.format(channel_id))

    def _do_close(self):
        del self.channels[0]
        for channel in self.channels.values():
            channel.close()

        self.protocol.transport.close()
        self.channels = {}

    def _setup_callbacks(self):
        self.handler.update({
            spec.ConnectionStart: self._on_start,
            spec.ConnectionOpenOK: self._on_open_ok,
            spec.ConnectionSecure: self._on_secure,
            spec.ConnectionTune: self._on_tune,
            spec.ConnectionClose: self._on_close,
            # spec.ConnectionBlocked: self._on_blocked,
            # spec.ConnectionUnblocked: self._on_unblocked,
            spec.ConnectionCloseOK: self._on_close_ok,
        })

    @coroutine
    def _on_start(self, version_major, version_minor, server_properties,
                  mechanisms, locales, method=spec.ConnectionStartOK,
                  reply_method=spec.ConnectionTune):
        client_properties = self.client_properties
        self.version_major = version_major
        self.version_minor = version_minor
        self.server_properties = server_properties
        self.mechanisms = mechanisms.split(' ')
        self.locales = locales.split(' ')

        scap = server_properties.get('capabilities') or {}
        if scap.get('consumer_cancel_notify'):
            client_properties['consumer_cancel_notify'] = True
        if scap.get('connection.blocked'):
            client_properties['connection.blocked'] = True

        self.handler.expected_methods = (reply_method,)
        self.send_method(
            method,
            (client_properties, self.login_method,
             self.login_response, locales),
        )

    @coroutine
    def _on_tune(self, channel_max, frame_max, server_heartbeat,
                 method=spec.ConnectionTuneOK):
        cmax = self.channel_max = channel_max or self.channel_max
        fmax = self.frame_max = frame_max or self.frame_max
        sheartbeat = self.server_heartbeat = server_heartbeat or 0
        cheartbeat = self.client_heartbeat

        if sheartbeat == 0 or cheartbeat == 0:
            negotiate = max
        else:
            negotiate = min
        heartbeat = self.heartbeat = negotiate(sheartbeat, cheartbeat)

        # Ignore server heartbeat if client_heartbeat is disabled
        if not cheartbeat:
            self.heartbeat = 0

        self.send_method(method, (cmax, fmax, heartbeat))
        self._after_tune()

    def _after_tune(self, method=spec.ConnectionOpen,
                    reply_method=spec.ConnectionOpenOK):
        self.handler.expected_methods = (reply_method,)
        self.send_method(method, (self.virtual_host, '', False))

    @coroutine
    def _on_open_ok(self, reserved_1):
        self.on_open and self.on_open(self)
        self.handler.ready()

    @coroutine
    def _on_secure(self, challenge):
        print('Challenge is: ', challenge)

    @coroutine
    def _on_close(self, reply_code, reply_text, class_id, method_id,
                  method=spec.ConnectionCloseOK):
        # XXX logging
        self.send_method(method, ())
        self._do_close()
        # XXX raise

    @coroutine
    def _on_close_ok(self):
        self._do_close()
        self.handler.ready()

    @coroutine
    def _on_blocked(self):
        self.on_blocked and self.on_blocked(self)

    @coroutine
    def _on_unblocked(self):
        self.on_unblocked and self.on_unblocked(self)
