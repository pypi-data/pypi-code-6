import threading
import socket
import logging
import asyncore

from .errors import XDError


LOCALHOST = '127.0.0.1'
BUFFER_SIZE = 4096  # default IBB block size, up to 8192

log = logging.getLogger(__name__)


"""
The purpose of this module is to give default behaviours for Digda protocol.
"""


class ResourceBase(object):
    """
    This class is an object representation of a resource.
    It gather the raw IQ used to make the request and any usefull information
    that could be used to proceed the request.
    """
    def __init__(self, iq):
        # Raw query
        self.iq = iq
        # Who's ask for the resource.
        self.requester = iq['from']
        # Who will receive data forwarded from the resource.
        self.destination = iq['dquery']['ddestination']['jid']
        # The resource identifier.
        self.rid = iq['dquery']['dresource']['rid']
        # Transport protocol
        self.transport = iq['dquery']['dresource']['transport']
        # The port
        self.port = int(iq['dquery']['dresource']['port'])


class ConnectedResource(ResourceBase):
    """
    This class is inherited to ResourceBase and implements specific fields of
    a resource that should connect on a server.
    """
    def __init__(self, iq):
        super(ConnectedResource, self).__init__(iq)
        self.address = iq['dquery']['dresource']['doption']['address']


class ListeningResource(ResourceBase):
    """
    This class is inherited to ResourceBase and implements specific fields of
    a resource connected on Digda.
    """
    def __init__(self, iq):
        super(ListeningResource, self).__init__(iq)
        self.address = iq['dquery']['dresource']['doption']['address']
        if self.address is None:
            self.address = ''


class ResourceLauncher(threading.Thread):
    """
    This class is an object representation of a thread. It only purpose is to
    contain an asynchronous loop handling incoming TCP/UDP data, regardless
    who's the client and who's the server.
    """
    def __init__(self, resource, plugin):
        super(ResourceLauncher, self).__init__()
        self._resource = resource
        self._plugin = plugin

    def run(self):
        AsyncResourceObserver(self._resource, self._plugin)
        asyncore.loop()
        self._plugin.unregister_observer(self._resource.rid)


class AsyncResourceObserver(asyncore.dispatcher):
    """
    This class is an object representation of an infinite loop running
    asynchronously and handling the creation/destruction of a TCP or UDP socket,
    working as a client or a server.
    """
    def __init__(self, resource, plugin):
        asyncore.dispatcher.__init__(self)
        self._resource = resource
        self._plugin = plugin
        self._client = None

        socket_t = {
            'tcp': socket.SOCK_STREAM,
            'udp': socket.SOCK_DGRAM
        }
        self.create_socket(socket.AF_INET, socket_t[resource.transport])

        try:
            # According to the type of resource, it decides using the socket
            # as a client or a server.
            if type(resource) is ConnectedResource:
                self.connect((resource.address, resource.port))
                log.debug("Digda is connected to %s:%d", resource.address, resource.port)
            else:
                self.set_reuse_addr()
                self.bind((LOCALHOST, resource.port))
                self.listen(5)
                log.debug("Digda listen on port %d and waiting for connection", resource.port)
        except Exception:
            # If the socket creation/binding/connection went wrong,
            # terminate the asynchronous loop will terminate its thread
            log.debug("Digda failed to resolve resource")
            plugin.decline(resource.iq, XDError.REMOTE_SERVER_NOT_FOUND)
            self.close()
            raise SystemExit
        else:
            # If everything went ok, this observer could be registered as
            # an effective resource handler.
            plugin.register_observer(resource.rid, self)
            plugin.accept(resource.iq)

    def handle_close(self):
        # This function can cause an unexpected exception sometimes,
        # this is a known issue.
        self.close()
        return False

    def handle_read(self):
        data = self.recv(BUFFER_SIZE)
        if data:
            # This observer does not forward data by itself
            self._plugin.queue(data=data, resource=self._resource)

    def handle_accept(self):
        # As a server, the observer should handle connections.
        if self._client is None:
            pair = self.accept()
            if pair is not None:
                sock, addr = pair
                self._client = sock
                log.debug("Resource connected on digda port %d", self._resource.port)
                AsyncResourceConnected(sock, self._resource, self._plugin)

    def feed(self, data):
        if self._client is not None:
            self._client.send(data)
        else:
            self.send(data)


class AsyncResourceConnected(asyncore.dispatcher_with_send):
    """
    This class is an extension of the observer, it handles a resource to
    connect on Digda as a client.
    """
    def __init__(self, sock, resource, plugin):
        asyncore.dispatcher_with_send.__init__(self, sock)
        self._resource = resource
        self._plugin = plugin

    def handle_read(self):
        data = self.recv(BUFFER_SIZE)
        if data:
            self._plugin.queue(data=data, resource=self._resource)