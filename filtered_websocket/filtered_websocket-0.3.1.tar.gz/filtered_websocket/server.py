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
    pubsub_listener = kwargs.pop("pubsub_listener", None)

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
    if pubsub_listener is not None:
        reactor.callInThread(
            pubsub_listener.listener,
            web_socket_instance
        )
        reactor.addSystemEventTrigger(
            "before",
            "shutdown",
            pubsub_listener.kill
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


if __name__ == '__main__':
    import os
    import importlib

    from . import config_deserializer
    from .storage_objects.base import BasePubSubStorageObject

    # Storage objects are configured via env variables for now,
    # consider .conf files in the future
    STORAGE_OBJECT_MODULE = os.environ.get("STORAGE_OBJECT_MODULE", None)
    if STORAGE_OBJECT_MODULE is None:
        STORAGE_OBJECT_MODULE = \
            "filtered_websocket.storage_objects.default"

    storage_object = importlib.import_module(STORAGE_OBJECT_MODULE)
    StorageObject = storage_object.StorageObject  # NOQA

    parser = default_parser()
    parser = StorageObject.parser(parser)
    options = parser.parse_args(sys.argv[1:])

    # A passed in config file will overwrite all other args
    if options.config is not None:
        options = parser.parse_args(config_deserializer(options.config))

    # If no filters are specified this will be imported.
    # the broadcast_by_message filter just creates a simple broadcast server
    FILTERS = [
        "filtered_websocket.filters.broadcast_messages",
        "filtered_websocket.filters.stdout_messages",
    ]

    storage_object_instance = StorageObject(options)
    if issubclass(StorageObject, BasePubSubStorageObject):
        storage_object_listener = StorageObject.get_pubsub_listener()(
            client=storage_object_instance.get_client(),
            options=options,
        )
        # Build our server reactor.
        web_socket_instance = build_reactor(
            options,
            storage_object=storage_object_instance,
            pubsub_listener=storage_object_listener
        )
    else:
        build_reactor(options)

    if options.filters is not None:
        FILTERS = options.filters

    # Importing the filters will inject them into event handlers at runtime
    for _filter in FILTERS:
        importlib.import_module(_filter)

    reactor.run()
