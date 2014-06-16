"""
Abstracts access to messaging broker.

Currently it is implemented using a STOMP-compatible broker.
Tests are currently dependent on Apollo (Apache ActiveMQ).
"""
import json
import logging

import stomp
from stomp.exception import ConnectionClosedException, ConnectFailedException, NotConnectedException


# Initialise the logger to log to the console
logging.basicConfig()


HOST = "0.0.0.0"
PORT = 61613
USER = "admin"
PASSWORD = "password"
QUEUE = "/queue/tractor"

EXCEPTIONS = (ConnectionClosedException, ConnectFailedException, NotConnectedException)


class Message(object):
    """
    Makes easy to pass dicts as messages to broker notify.

    Usage:
        data = {"name": "Game of Thrones"}
        message = Message(**data)
        Broker().notify(message)
    """
    def __init__(self, **kwargs):
        self.params = kwargs

    def __str__(self):
        return json.dumps(self.params)


class BrokerException(Exception):
    """
    Wrap exceptions that happen inside broker activites.
    """
    def __init__(self, value):
        self.value = value
        Exception.__init__(self)

    def __str__(self):
        return repr(self.value)


class Broker(object):
    "Messaging Broker"

    def __init__(self, host=HOST, port=PORT, user=USER, password=PASSWORD, queue=QUEUE):
        self.connection = stomp.Connection(
            host_and_ports=[(host, port)],
            reconnect_sleep_initial=10,
            reconnect_sleep_increase=1.618,
            reconnect_sleep_jitter=0.1,
            reconnect_sleep_max=300.0,
            reconnect_attempts_max=((24 * 60 * 60) / 300) * 2,  # Almost two days
            keepalive=True,
            heartbeats=(0, 0)
        )
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.queue = queue
        self.connect()

    def set_listener(self, listener_id, listener):
        """
        Set a listener, provided its name and an instance of a Listener class.
        It will be called asynchronously when a message is send to self.queue.
        """
        self.connection.set_listener(listener_id, listener)
        self.connection.subscribe(destination=self.queue, ack='auto', id=1)

    def notify(self, message):
        """
        Provided a message object which has __str__ representation, send it to
        the broker, using the class' settings.
        """
        data = str(message)
        if self.not_connected():
            reconnected = self.connect()
            if not reconnected:
                return False
        try:
            self.connection.send(destination=self.queue, body=data)
        except EXCEPTIONS as e:
            msg = "Broker at {0}:{1} unavailable due to {2}.".format(self.host, self.port, str(e.__class__))
            raise BrokerException(msg)
        return True

    def connect(self):
        """
        Connect to STOMP broker.
        """
        try:
            self.connection.start()
            self.connection.connect(self.user, self.password)
        except EXCEPTIONS as e:
            msg = "Broker at {0}:{1} reconnection failed with error {2}.".format(self.host, self.port, str(e.__class__))
            raise BrokerException(msg)
        return True

    def not_connected(self):
        """
        Return empty string if connected. Otherwise, return the error message.
        """
        error = ""
        try:
            self.connection.begin(transaction='ping')
            self.connection.abort(transaction='ping')
        except EXCEPTIONS as e:
            error = str(e.__class__)
        return error
