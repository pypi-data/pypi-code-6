import uuid
import logging
import Queue
import random
import os

from sleekxmpp import Iq
from sleekxmpp.plugins import BasePlugin
from sleekxmpp.xmlstream import register_stanza_plugin
from sleekxmpp.xmlstream.handler import Callback
from sleekxmpp.xmlstream.matcher import StanzaPath

import stanza
from .stanza import (Query, Resource, Option, Destination, ResourceInfo)
from .errors import XDError, XDException
from .forward import (ConnectedResource, ListeningResource, ResourceLauncher)


log = logging.getLogger(__name__)


def short_id():
    """
    This util method generates a short ID without UUID.
    """
    return '%x' % (random.getrandbits(24) ^ os.getpid())


def default_behaviour(func):
    """
    This decorator checks if an instance method is callable.
    A default behaviour method is callable if 'custom_behaviour' is false.
    """
    def inner(*args, **kwargs):
        self = args[0]

        if not self.custom_behaviour:
            return func(*args, **kwargs)
        else:
            raise XDException("This method is available only when using default behaviours")
    return inner


class XEP_Digda(BasePlugin):
    """
    Functional architecture of Digda protocol and its workflow.

    This implementation gives default behaviors for queries that have been
    received, but they also can be routed to be handled in a custom way.

    End-user functions /w event triggered
    (events surrounded by [] are triggered only if 'custom_behaviour' option is
    setted, otherwise, the workflow chooses the default behaviour)

    +-- function: 'query_resource()'
    |   [event]: 'forward_requested' (iq: dict)
    |   |
    |   +-- function: 'accept()'
    |   |   event: 'forward_accepted' (rid: string)
    |   |
    |   +-- function: 'decline()'
    |       event: 'forward_refused' (error: dict[rid/reason])
    |
    +-- function: 'close_resource()'
    |   [event]: 'close_requested' (iq: dict)
    |   |
    |   +-- function: 'accept()'
    |   |   event: 'close_accepted' (rid: string)
    |   |
    |   +-- function: 'decline()'
    |       event: 'close_refused' (error: dict[rid/reason])
    |
    +-- function: 'bind_stream()'
    |   event: 'bind_stream' (info: dict[sid/rid])
    |
    +-- function: 'resource_lost()'
        event: 'resource_lost' (rid: string)
    """

    name = 'xep_digda'
    description = 'XEP-Digda: resource forwarding over XMPP'
    dependencies = {
        'xep_0030', 'xep_0047'
    }
    stanza = stanza
    default_config = {
        'custom_behaviour': False
    }

    def plugin_init(self):
        register_stanza_plugin(Iq, Query)
        register_stanza_plugin(Query, Resource)
        register_stanza_plugin(Query, Destination)
        register_stanza_plugin(Resource, Option)
        register_stanza_plugin(Iq, ResourceInfo)

        # Declare class attributes in a not-constructor method is unsafe
        # but since, we're sure this method is called before every others,
        # that's ok.
        self._synchronous = not self.custom_behaviour
        self._resources = dict()
        self._queue = Queue.Queue()

        self.xmpp.register_handler(Callback(
            'query dispatcher',
            StanzaPath('iq@type=set/dquery'),
            self._dispatch_query))

        self.xmpp.register_handler(Callback(
            'resource info',
            StanzaPath('iq@type=set/drinfo'),
            self._resource_info))

    def plugin_end(self):
        self.xmpp.remove_handler('query dispatcher')
        self.xmpp.remove_handler('resource info')
        self.xmpp['xep_0030'].del_feature(feature='digda:forward')

    def session_bind(self, jid):
        self.xmpp['xep_0030'].add_feature('digda:forward')

    """
    Following methods describe internal behaviours
    """

    def _make_error(self, iq, condition):
        """
        Utils method that creates a standard error based on a given iq stanza.
        """
        rid = iq['dquery']['dresource']['rid']

        iq.reply().error()
        iq['error']['type'] = 'cancel'
        iq['error']['code'] = rid  # use 'code' attribute to bring back the rid
        iq['error']['condition'] = condition
        return iq

    def _dispatch_query(self, iq):
        """
        This method allows to route queries according to its type.
        """
        query_type = iq['dquery']['type']

        behaviours = {
            'open': {'default': self._default_open,  # internal handler
                     'custom': 'forward_requested'},  # name of the event

            'listen': {'default': self._default_listen,
                       'custom': 'forward_requested'},

            'connect': {'default': self._default_connect,
                        'custom': 'forward_requested'},

            'close': {'default': self._default_close,
                      'custom': 'close_requested'},

            'disconnect': {'default': self._default_disconnect,
                           'custom': 'forward_requested'}
        }

        if query_type in behaviours.keys():
            if not self.custom_behaviour:
                log.debug("Received a digda %s request from %s (default behaviour)",
                          query_type, iq['from'])
                behaviours[query_type]['default'](iq)
            else:
                log.debug("Received a digda %s request from %s (event triggered)",
                          query_type, iq['from'])
                self.xmpp.event(behaviours[query_type]['custom'], iq)
        else:
            error = self._make_error(iq, XDError.BAD_REQUEST)
            error.send()

    def _resource_info(self, iq):
        """
        This method allows to trigger the appropriate event
        when a resource info is received.
        """
        info_type = iq['drinfo']['info']
        rid = iq['drinfo']['rid']

        if info_type == 'forward':
            sid = iq['drinfo']['sid']  # IBB session ID
            log.debug("Digda incoming resource (%s) from %s", rid, iq['from'])
            self.xmpp.event('bind_stream', {'sid': sid, 'rid': rid})
        elif info_type == 'lost':
            log.debug("Digda resource lost (%s) by %s", rid, iq['from'])
            self.xmpp.event('resource_lost', rid)
        else:
            error = self._make_error(iq, XDError.BAD_REQUEST)
            error.send()

    def _callback_query_resource(self, iq):
        """
        This method is a callback to handle response to a query.
        """
        if iq['type'] == 'result':
            resource_id = iq['dquery']['dresource']['rid']
            self.xmpp.event('forward_accepted', resource_id)
        elif iq['type'] == 'error':
            # the rid is passed through using the 'code' attribute
            resource_id = iq['error']['code']
            reason = iq['error']['condition']
            self.xmpp.event('forward_refused', {'rid': resource_id,
                                                'reason': reason})

    def _callback_close_resource(self, iq):
        """
        This method is a callback to handle the response to a
        close-resource request.
        """
        if iq['type'] == 'result':
            resource_id = iq['dquery']['dresource']['rid']
            self.xmpp.event('close_accepted', resource_id)
        elif iq['type'] == 'error':
            # the rid is passed through using the 'code' attribute
            resource_id = iq['error']['code']
            reason = iq['error']['condition']
            self.xmpp.event('close_refused', {'rid': resource_id,
                                             'reason': reason})

    """
    Following methods are callable at anytime by the end-user of the plugin
    to send queries.
    """

    def close_resource(self, jid, rid):
        """
        This method creates an IQ stanza whith the appropriate elements and
        attributes, and send it to request the terminaison of the specified
        resource handling.
        """
        # Setup the IQ
        iq = self.xmpp.Iq()
        iq['type'] = 'set'
        iq['to'] = jid

        # Setup the query
        iq['dquery']['type'] = 'close'
        iq['dquery']['dresource']['rid'] = rid

        # Send the close request
        iq.send(block=self._synchronous, callback=self._callback_close_resource)

    def query_resource(self, jid, target, query, transport, port, rid=None, **kwargs):
        """
        This method creates an IQ with the appropriate elements and attributes,
        and send it to request the forwarding of a remote resource.

        :param jid to: Who is asked to forward the resource.
        :param jid target: To whom the resource will be forwarded.
        :param string query: How the resource will be accessed (connect, listen).
        :param string transport: What is the transport layer of the resource.
        :param integer port: Which port is it using.
        :param string rid: Optional, force the choice of the resource ID.
        :param dict kwargs: Options to access the resource (address, etc).
        """
        # Setup the IQ
        iq = self.xmpp.Iq()
        iq['type'] = 'set'
        iq['to'] = jid
        dquery = iq['dquery']
        dresource = dquery['dresource']
        # Set query type and transport now, perform checks a bit later
        dquery['type'] = query
        dresource['transport'] = transport
        # 'port' is mandatory whatever the query/transport args
        dresource['port'] = str(port)
        # Generate a new unique resource ID
        if rid is None:
            dresource['rid'] = short_id()
        else:
            dresource['rid'] = rid
        # Jabber ID of the forward target
        dquery['ddestination']['jid'] = target

        # Check the query type/transport value pair and infer the allowed
        # options accordingly
        if query == 'listen' and transport in ('tcp', 'udp'):
            allowed_options = ('address',)
        elif query == 'connect' and transport == 'tcp':
            allowed_options = ('address',)
        elif query == 'open' and transport == 'udp':
            allowed_options = ('address',)
        elif query == 'open' and transport == 'serial':
            allowed_options = ('baudrate', 'bytesize', 'parity', 'stopbits',
                               'xonxoff', 'rtscts', 'dsrdtr')
        else:
            raise XDException("invalid 'query'/'transport' combination "
                              "'%s'/'%s'" % (query, transport))

        # Check and set query options
        for key, value in kwargs.iteritems():
            if key in allowed_options:
                dresource['doption'][key] = value
            else:
                raise XDException("unexpected query option '%s'" % key)

        # Congratulation, you succeed to end up here!
        # If custom_behaviour is True, send is not blocking (asynchronous),
        # since it's impossible to know how would be handled the events.
        iq.send(block=self._synchronous,
                callback=self._callback_query_resource)
        return dresource['rid']

    def bind_stream(self, jid, sid, rid):
        """
        This method creates an IQ stanza that notifies a user a resource is
        ready to be forwarded, and the SessionID that will be used to do so is
        specified. This mechanism allows the recipient to match incoming data
        from a SID with a resource.
        """
        # Setup the IQ
        iq = self.xmpp.Iq()
        iq['type'] = 'set'
        iq['to'] = jid

        # Setup the resource info
        iq['drinfo']['info'] = 'forward'
        iq['drinfo']['sid'] = sid
        iq['drinfo']['rid'] = rid

        iq.send(block=False)

    def resource_lost(self, jid, rid):
        """
        This method is called in order to notify the resource requester,
        that this very resource has been lost.
        """
        # Default behaviours
        if not self.custom_behaviour and rid in self._resources.keys():
            del self._resources[rid]

        # Setup the IQ
        iq = self.xmpp.Iq()
        iq['type'] = 'set'
        iq['to'] = jid

        # Setup the resource info
        iq['drinfo']['info'] = 'lost'
        iq['drinfo']['rid'] = rid

        iq.send(block=False)

    def accept(self, iq):
        """
        This method allows to send a positive feedback.
        """
        rid = iq['dquery']['dresource']['rid']
        iq.reply()
        iq['dquery']['dresource']['rid'] = rid
        iq.send()

    def decline(self, iq, reason):
        """
        This method allows to send a negative feedback.
        However, a reason shall be specified
        """
        error = self._make_error(iq, reason)
        error.send()

    """
    Following methods are available since default behaviours are used.
    """

    @default_behaviour
    def register_observer(self, rid, observer):
        self._resources[rid] = observer

    @default_behaviour
    def unregister_observer(self, rid):
        if self._resources[rid]:
            del self._resources[rid]

    @default_behaviour
    def queue(self, data, resource):
        self._queue.put((data, resource))

    @default_behaviour
    def get_queue(self):
        return self._queue

    @default_behaviour
    def feed_resource(self, rid, data):
        if self._resources[rid] and self._resources[rid].writable():
            log.debug("Digda received data ('%s') to forward to resource %s", data, rid)
            self._resources[rid].feed(data)

    """
    Following methods describe default behaviours
    """

    def _default_open(self, iq):
        """
        Since forwarding from a serial port requiered the use of an external lib,
        this feature is not implemented and should be handled by the user.
        """
        self.decline(iq, XDError.FEATURE_NOT_IMPLEMENTED)

    def _default_listen(self, iq):
        """
        This method creates the appropriate thread that handles the resource,
        and send a positive feedback to the query sender.
        """
        resource = ListeningResource(iq)
        thread = ResourceLauncher(resource, self)
        thread.start()

    def _default_connect(self, iq):
        """
        This method creates the appropriate thread that handles the resource,
        and send a positive feedback to the query sender.
        """
        resource = ConnectedResource(iq)
        thread = ResourceLauncher(resource, self)
        thread.start()

    def _default_close(self, iq):
        """
        This method tells the thread handling the specified resource to stop.
        """
        rid = iq['dquery']['dresource']['rid']

        if not self._resources[rid]:
            self.decline(iq, XDError.ITEM_NOT_FOUND)
        else:
            self._resources[rid].close()
            self.accept(iq)

    def _default_disconnect(self, iq):
        """
        This method disconnects any client connected to a ResourceListener.
        However, the socket remains open.
        """
        rid = iq['dquery']['dresource']['rid']

        if not self._resources[rid]:
            self.decline(iq, XDError.ITEM_NOT_FOUND)
        else:
            try:
                thread = self._resources[rid]
                thread.disconnect()
                self.accept(iq)
            except AttributeError:
                # Call a disconnect on a not-ResourceObserver
                self.decline(iq, XDError.NOT_ACCEPTABLE)
