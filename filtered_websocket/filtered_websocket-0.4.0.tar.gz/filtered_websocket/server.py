#!/usr/bin/env python

"""
FilteredWebSocket: Morgan (Reece) Phillips @linuxpoetry linux-poetry.com

Create WebSocket servers by composing filter chains.

"""

from __future__ import absolute_import

from twisted.internet.protocol import Factory
from twisted.internet import reactor, ssl
from twisted.internet.task import LoopingCall
from .server_protocol.server import Protocol
import collections
import argparse
import sys

if sys.version_info >= (3, 0, 0):
    from queue import Queue
else:
    from Queue import Queue

from .filters.base import (
    WebSocketDataFilter,
    WebSocketMessageFilter,
    WebSocketDisconnectFilter,
    WebSocketConsumerFilter,
)


class FilteredWebSocket(Protocol):

    def __init__(self, *args, **kwargs):

        # The storage object should inherit from
        # storage_objects.default_storage_object.BaseStorageObject
        self.storage_object = kwargs.pop("storage_object")

        # The token object may be leveraged for authentication via OAuth,
        # session keys, or other such methods.  See the
        # broadcast_messages_by_token module for an example.
        self.token = kwargs.pop("token")

        # A queue to be used in any producer/consumer activities
        self.queue = Queue()

        super(FilteredWebSocket, self).__init__(*args, **kwargs)

    def dataReceived(self, data):
        WebSocketDataFilter.run(self, data)
        super(FilteredWebSocket, self).dataReceived(data)

    def onDisconnect(self):
        WebSocketDisconnectFilter.run(self)

    def onMessage(self, msg):
        WebSocketMessageFilter.run(self, msg)


class FilteredWebSocketFactory(Factory):

    def __init__(self, **kwargs):
        self.storage_object = kwargs.get(
            "storage_object",
            collections.defaultdict(set)
        )
        self.token = kwargs.get("token")
        self.users = {}
        self.queue = Queue()

    def buildProtocol(self, _address):
        return FilteredWebSocket(
            self.users,
            storage_object=self.storage_object,
            token=self.token
        )

    def consumer(self):
        """
        Called in a reactor loop to enable the producer/consumer pattern.
        """
        if not self.queue.empty():
            data = self.queue.get()
            WebSocketConsumerFilter.run(self, data)


def build_reactor(options, **kwargs):
    web_socket_instance = FilteredWebSocketFactory(**kwargs)
    subscriber = kwargs.pop("subscriber", None)

    if options.key and options.cert:
        with open(options.key) as keyFile:
            with open(options.cert) as certFile:
                cert = ssl.PrivateCertificate.loadPEM(keyFile.read() + certFile.read())
                reactor.listenSSL(options.port, web_socket_instance, cert.options())
    else:
        reactor.listenTCP(
            options.port,
            web_socket_instance
        )
    if subscriber is not None:
        reactor.callInThread(
            subscriber.listener,
            web_socket_instance
        )
        reactor.addSystemEventTrigger(
            "before",
            "shutdown",
            subscriber.kill
        )

    # Start the consumer loop
    consumer_loop = LoopingCall(
        web_socket_instance.consumer
    )
    consumer_loop.start(0.001, now=False)
    return web_socket_instance


def default_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--port",
        help="The listening port.",
        type=int,
        default=9000
    )
    parser.add_argument(
        "-c",
        "--config",
        help="A JSON config file."
    )
    parser.add_argument(
        "-f",
        "--filters",
        help="Filters to import at runtime.",
        nargs="*"
    )
    parser.add_argument(
        "-key",
        help="A key file (ssl)."
    )
    parser.add_argument(
        "-cert",
        help="A certificate file (ssl)."
    )
    return parser
