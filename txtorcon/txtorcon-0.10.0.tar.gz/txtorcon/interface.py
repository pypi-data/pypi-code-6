from zope.interface import implements, Interface, Attribute


class IStreamListener(Interface):
    """
    Notifications about changes to a :class:`txtorcon.Stream`.

    If you wish for your listener to be added to *all* new streams,
    see :meth:`txtorcon.TorState.add_stream_listener`.
    """

    def stream_new(stream):
        "a new stream has been created"

    def stream_succeeded(stream):
        "stream has succeeded"

    def stream_attach(stream, circuit):
        "the stream has been attached to a circuit"

    def stream_detach(stream, **kw):
        """
        the stream has been detached from its circuit

        :param kw:
            provides any flags for this event, which will include at
            least REASON (but may include anything). See control-spec.
        """

    def stream_closed(stream, **kw):
        """
        stream has been closed (won't be in controller's list anymore).

        :param kw:
            provides any flags for this event, which will include at
            least REASON (but may include anything). See control-spec.
        """

    def stream_failed(stream, **kw):
        """
        stream failed for some reason (won't be in controller's list anymore).

        :param kw:
            a dict of all the flags for the stream failure; see
            control-spec but these will include REASON and sometimes
            REMOTE_REASON (if the remote Tor closed the
            connection). Both an all-uppercase and all-lowercase
            version of each keyword is supplied (by the library; Tor
            provides all-uppercase only). Others may include
            BUILD_FLAGS, PURPOSE, HS_STATE, REND_QUERY, TIME_CREATED
            (or anything else).
        """


class StreamListenerMixin(object):
    """
    Implements all of :class:`txtorcon.IStreamListener` with no-op
    methods. You may subclass from this if you don't care about most
    of the notifications.
    """

    implements(IStreamListener)

    def stream_new(self, stream):
        pass

    def stream_succeeded(self, stream):
        pass

    def stream_attach(self, stream, circuit):
        pass

    def stream_detach(self, stream, **kw):
        pass

    def stream_closed(self, stream, **kw):
        pass

    def stream_failed(self, stream, **kw):
        pass


class IStreamAttacher(Interface):
    """
    Used by :class:`txtorcon.TorState` to map streams to circuits (see
    :meth:`txtorcon.TorState.set_attacher`).

    Each time a new :class:`txtorcon.Stream` is created, this
    interface will be queried to find out which
    :class:`txtorcon.Circuit` it should be attached to.
    """

    def attach_stream(stream, circuits):
        """
        :param stream:
            The stream to attach, which will be in NEW or NEWRESOLVE
            state.

        :param circuits:
            all currently available :class:`txtorcon.Circuit` objects
            in the :class:`txtorcon.TorState` in a dict indexed by id.
            Note they are *not* limited to BUILT circuits.

        You should return a :class:`txtorcon.Circuit` instance which
        should be at state BUILT in the currently running Tor. You may
        also return a Deferred which will callback with the desired
        circuit. In this case, you will probably need to be aware that
        the callback from :meth:`txtorcon.TorState.build_circuit` does
        NOT call back with a Circuit (just Tor's response of 'EXTEND
        1234') and any circuit you do return must be in the BUILT
        state anyway (which the above will not).

        See :ref:`attach_streams_by_country.py` for a complete
        example of using a Deferred in an IStreamAttacher.

        Alternatively, you may return None in which case the Tor
        controller will be told to choose a circuit itself.

        Note that Tor will refuse to attach to any circuit not in
        BUILT state; see ATTACHSTREAM in control-spec.txt

        Note also that although you get a request to attach a stream
        that ends in .onion Tor doesn't currently let you specify how
        to attach .onion addresses and will always give a 551 error.
        """


class ICircuitContainer(Interface):
    """
    An interface that contains a bunch of Circuit objects and can look
    them up by id.
    """

    def find_circuit(id):
        ":return: a circuit for the id, or exception."

    def close_circuit(circuit, **kwargs):
        """
        Close a circuit.
        :return: a Deferred which callbacks when the closing process
        is started (not necessarily finished inside Tor).
        """

    ## FIXME do we need an IStreamContainer that Stream instances get?
    ## (Currently, they get an ICircuitContainer...)
    def close_stream(stream, **kwargs):
        """
        Close a stream.
        :return: a Deferred which callbacks when the closing process
        is started (not necessarily finished inside Tor).
        """


class ICircuitListener(Interface):
    """
    An interface to listen for updates to Circuits.
    """

    def circuit_new(circuit):
        """A new circuit has been created.  You'll always get one of
        these for every Circuit even if it doesn't go through the "launched"
        state."""

    def circuit_launched(circuit):
        "A new circuit has been started."

    def circuit_extend(circuit, router):
        "A circuit has been extended to include a new router hop."

    def circuit_built(circuit):
        """
        A circuit has been extended to all hops (usually 3 for user
        circuits).
        """

    def circuit_closed(circuit, **kw):
        """
        A circuit has been closed cleanly (won't be in controller's list any more).

        :param kw:
            A dict of additional args. REASON is alsways included, and
            often REMOTE_REASON also. See the control-spec
            documentation.  As of this writing, REASON is one of the
            following strings: MISC, RESOLVEFAILED, CONNECTREFUSED,
            EXITPOLICY, DESTROY, DONE, TIMEOUT, NOROUTE, HIBERNATING,
            INTERNAL,RESOURCELIMIT, CONNRESET, TORPROTOCOL,
            NOTDIRECTORY, END, PRIVATE_ADDR. However, don't depend on
            that: it could be anything.

            To facilitate declaring args you want in the method
            (e.g. circuit_failed(self, circuit, reason=None,
            remote_reason=None, **kw)) lower-case versions of all the
            keys are also provided (pointing to the same -- usually
            UPPERCASE -- strings as the upper-case keys).
        """

    def circuit_failed(circuit, **kw):
        """
        A circuit has been closed because something went wrong.

        The circuit won't be in the TorState's list anymore.

        :param kw:
            A dict of additional args. REASON is alsways included, and
            often REMOTE_REASON also. See the control-spec
            documentation.  As of this writing, REASON is one of the
            following strings: MISC, RESOLVEFAILED, CONNECTREFUSED,
            EXITPOLICY, DESTROY, DONE, TIMEOUT, NOROUTE, HIBERNATING,
            INTERNAL,RESOURCELIMIT, CONNRESET, TORPROTOCOL,
            NOTDIRECTORY, END, PRIVATE_ADDR. However, don't depend on
            that: it could be anything.

            To facilitate declaring args you want in the method
            (e.g. circuit_failed(self, circuit, reason=None,
            remote_reason=None, **kw)) lower-case versions of all the
            keys are also provided (pointing to the same -- usually
            UPPERCASE -- strings as the upper-case keys).
        """


class CircuitListenerMixin(object):
    """
    Implements all of ICircuitListener with no-op methods. Subclass
    from this if you don't care about most of the notifications.
    """
    implements(ICircuitListener)

    def circuit_new(self, circuit):
        pass

    def circuit_launched(self, circuit):
        pass

    def circuit_extend(self, circuit, router):
        pass

    def circuit_built(self, circuit):
        pass

    def circuit_closed(self, circuit, **kw):
        pass

    def circuit_failed(self, circuit, **kw):
        pass


class ITorControlProtocol(Interface):
    """
    This defines the API to the TorController object.

    This is the usual entry-point to this library, and you shouldn't
    need to call methods outside this interface.
    """

    def get_info(info):
        """
        :return: a Deferred which will callback with the info keys you
           asked for. For values ones, see control-spec.
        """

    def get_conf(*args):
        """
        Returns one or many configuration values via Deferred. See
        control-spec for valid keys. The value will be a dictionary.
        """

    def signal(signal_name):
        """
        Issues a signal to Tor. See control-spec or .valid_signals for
        which ones are available and their return values.
        """

    def build_circuit(routers):
        """
        Builds a circuit consisting of exactly the routers specified,
        in order.  This issues a series of EXTENDCIRCUIT calls to Tor;
        the deferred returned from this is for the final
        EXTEND. FIXME: should return the Circuit instance, but
        currently returns final extend message 'EXTEND 1234' for
        example.
        """

    def close_circuit(circuit):
        """
        Asks Tor to close the circuit. Note that the Circuit instance
        is only removed as a result of the next CIRC CLOSED event. The
        Deferred returned from this method callbacks when the
        CLOSECIRCUIT command has successfully executed, not when the
        circuit is actually gone.

        If you wish to know when this circuit is actually gone, add an
        ICircuitListener and wait for circuit_closed()
        """

    def add_circuit_listener(icircuitlistener):
        """
        Add an implementor of :class:`txtorcon.interface.ICircuitListener`
        which will be added to all new circuits as well as all
        existing ones (you won't, however, get circuit_new calls for
        the existing ones)
        """

    def add_stream_listener(istreamlistener):
        """
        Add an implementor of :class:`txtorcon.interface.IStreamListener`
        which will be added to all new circuits as well as all
        existing ones (you won't, however, get stream_new calls for
        the existing ones)
        """

    def add_event_listener(evt, callback):
        """
        Add a listener to an Event object. This may be called multiple
        times for the same event. Every time the event happens, the
        callback method will be called. The callback has one argument
        (a string, the contents of the event, minus the '650' and the
        name of the event)

        FIXME: should have an interface for the callback.
        """


class IRouterContainer(Interface):

    unique_routers = Attribute("contains a list of all the Router instances")

    def router_from_id(routerid):
        """
        Note that this method MUST always return a Router instance --
        if you ask for a router ID that didn't yet exist, it is
        created (although without IP addresses and such because it
        wasn't in the consensus). You may find out if a Router came
        from the 'GETINFO ns/all' list by checking the from_consensus
        attribute. This is to simplify code like in Circuit.update()
        that needs to handle the case where an EXTENDED circuit event
        is the only time we've seen a Router -- it's possible for Tor
        to do things with routers not in the consensus (like extend
        circuits to them).

        :return: a router by its ID.
        """


class IAddrListener(Interface):
    def addrmap_added(addr):
        """
        A new address was added to the address map.
        """

    def addrmap_expired(name):
        """
        An address has expired from the address map.
        """
