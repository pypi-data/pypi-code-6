# -*- coding: utf-8 -*-
"""
colibri.spec
~~~~~~~~~~~~

Implementation of AMQP specification.

This file was generated 2014-09-15 15:42:09.973725 from amqp0-9-1.extended.xml.

"""

from __future__ import absolute_import

from struct import pack, unpack

from .serialization import (dumps, loads, BIT, OCTET, SHORT, LONG,
                            LONGLONG, SHORTSTR, LONGSTR, TABLE)


def select_method(method_type, unpack=unpack):
    code = unpack('!HH', method_type)
    return METHODS[code]


class MethodMeta(type):

    def __hash__(cls):
        return hash(cls.method_type)

    def __eq__(cls, other):
        if not isinstance(other, tuple):
            other = other.method_type
        return cls.method_type == other


class BaseMethod(object, metaclass=MethodMeta):
    """Base class for all AMQP methods."""

    @classmethod
    def unpack(cls, raw):
        return loads(''.join(type_ for _, type_ in cls.field_info), raw)[0]

    @classmethod
    def pack(cls, payload):
        payload = list(payload)
        fmt, values = [], []
        for name, type_ in cls.field_info:
            fmt.append(type_)
            values.append(payload.pop(0))
        return pack('!HH', *cls.method_type) + dumps(''.join(fmt), values)


class ConnectionStart(BaseMethod):
    """This method starts the connection negotiation process by telling the
    client the protocol version that the server proposes, along with a list of
    security mechanisms which the client can use for authentication.

    Arguments:
        version_major: OCTET
        version_minor: OCTET
        server_properties: TABLE
        mechanisms: LONGSTR
        locales: LONGSTR
    """
    method_type = (10, 10)
    field_info = (
        ('version_major', OCTET),
        ('version_minor', OCTET),
        ('server_properties', TABLE),
        ('mechanisms', LONGSTR),
        ('locales', LONGSTR),
    )
    synchronous = True


class ConnectionStartOK(BaseMethod):
    """This method selects a SASL security mechanism.

    Arguments:
        client_properties: TABLE
        mechanism: SHORTSTR
        response: LONGSTR
        locale: SHORTSTR
    """
    method_type = (10, 11)
    field_info = (
        ('client_properties', TABLE),
        ('mechanism', SHORTSTR),
        ('response', LONGSTR),
        ('locale', SHORTSTR),
    )
    synchronous = True


class ConnectionSecure(BaseMethod):
    """The SASL protocol works by exchanging challenges and responses until
    both peers have received sufficient information to authenticate each other.
    This method challenges the client to provide more information.

    Arguments:
        challenge: LONGSTR
    """
    method_type = (10, 20)
    field_info = (
        ('challenge', LONGSTR),
    )
    synchronous = True


class ConnectionSecureOK(BaseMethod):
    """This method attempts to authenticate, passing a block of SASL data for
    the security mechanism at the server side.

    Arguments:
        response: LONGSTR
    """
    method_type = (10, 21)
    field_info = (
        ('response', LONGSTR),
    )
    synchronous = True


class ConnectionTune(BaseMethod):
    """This method proposes a set of connection configuration values to the
    client. The client can accept and/or adjust these.

    Arguments:
        channel_max: SHORT
        frame_max: LONG
        heartbeat: SHORT
    """
    method_type = (10, 30)
    field_info = (
        ('channel_max', SHORT),
        ('frame_max', LONG),
        ('heartbeat', SHORT),
    )
    synchronous = True


class ConnectionTuneOK(BaseMethod):
    """This method sends the client's connection tuning parameters to the
    server. Certain fields are negotiated, others provide capability
    information.

    Arguments:
        channel_max: SHORT
        frame_max: LONG
        heartbeat: SHORT
    """
    method_type = (10, 31)
    field_info = (
        ('channel_max', SHORT),
        ('frame_max', LONG),
        ('heartbeat', SHORT),
    )
    synchronous = True


class ConnectionOpen(BaseMethod):
    """This method opens a connection to a virtual host, which is a collection
    of resources, and acts to separate multiple application domains within a
    server. The server may apply arbitrary limits per virtual host, such as the
    number of each type of entity that may be used, per connection and/or in
    total.

    Arguments:
        virtual_host: SHORTSTR
        reserved_1: SHORTSTR
        reserved_2: BIT
    """
    method_type = (10, 40)
    field_info = (
        ('virtual_host', SHORTSTR),
        ('reserved_1', SHORTSTR),
        ('reserved_2', BIT),
    )
    synchronous = True


class ConnectionOpenOK(BaseMethod):
    """This method signals to the client that the connection is ready for use.

    Arguments:
        reserved_1: SHORTSTR
    """
    method_type = (10, 41)
    field_info = (
        ('reserved_1', SHORTSTR),
    )
    synchronous = True


class ConnectionClose(BaseMethod):
    """This method indicates that the sender wants to close the connection.
    This may be due to internal conditions (e.g. a forced shut-down) or due to
    an error handling a specific method, i.e. an exception. When a close is due
    to an exception, the sender provides the class and method id of the method
    which caused the exception.

    Arguments:
        reply_code: SHORT
        reply_text: SHORTSTR
        class_id: SHORT
        method_id: SHORT
    """
    method_type = (10, 50)
    field_info = (
        ('reply_code', SHORT),
        ('reply_text', SHORTSTR),
        ('class_id', SHORT),
        ('method_id', SHORT),
    )
    synchronous = True


class ConnectionCloseOK(BaseMethod):
    """This method confirms a Connection.Close method and tells the recipient
    that it is safe to release resources for the connection and close the
    socket.
    """
    method_type = (10, 51)
    field_info = ()
    synchronous = True


class ChannelOpen(BaseMethod):
    """This method opens a channel to the server.

    Arguments:
        reserved_1: SHORTSTR
    """
    method_type = (20, 10)
    field_info = (
        ('reserved_1', SHORTSTR),
    )
    synchronous = True


class ChannelOpenOK(BaseMethod):
    """This method signals to the client that the channel is ready for use.

    Arguments:
        reserved_1: LONGSTR
    """
    method_type = (20, 11)
    field_info = (
        ('reserved_1', LONGSTR),
    )
    synchronous = True


class ChannelFlow(BaseMethod):
    """This method asks the peer to pause or restart the flow of content data
    sent by a consumer. This is a simple flow-control mechanism that a peer can
    use to avoid overflowing its queues or otherwise finding itself receiving
    more messages than it can process. Note that this method is not intended
    for window control. It does not affect contents returned by Basic.Get-Ok
    methods.

    Arguments:
        active: BIT
    """
    method_type = (20, 20)
    field_info = (
        ('active', BIT),
    )
    synchronous = True


class ChannelFlowOK(BaseMethod):
    """Confirms to the peer that a flow command was received and processed.

    Arguments:
        active: BIT
    """
    method_type = (20, 21)
    field_info = (
        ('active', BIT),
    )
    synchronous = False


class ChannelClose(BaseMethod):
    """This method indicates that the sender wants to close the channel. This
    may be due to internal conditions (e.g. a forced shut-down) or due to an
    error handling a specific method, i.e. an exception. When a close is due to
    an exception, the sender provides the class and method id of the method
    which caused the exception.

    Arguments:
        reply_code: SHORT
        reply_text: SHORTSTR
        class_id: SHORT
        method_id: SHORT
    """
    method_type = (20, 40)
    field_info = (
        ('reply_code', SHORT),
        ('reply_text', SHORTSTR),
        ('class_id', SHORT),
        ('method_id', SHORT),
    )
    synchronous = True


class ChannelCloseOK(BaseMethod):
    """This method confirms a Channel.Close method and tells the recipient
    that it is safe to release resources for the channel.
    """
    method_type = (20, 41)
    field_info = ()
    synchronous = True


class ExchangeDeclare(BaseMethod):
    """This method creates an exchange if it does not already exist, and if
    the exchange exists, verifies that it is of the correct and expected class.

    Arguments:
        reserved_1: SHORT
        exchange: SHORTSTR
        type: SHORTSTR
        passive: BIT
        durable: BIT
        auto_delete: BIT
        internal: BIT
        no_wait: BIT
        arguments: TABLE
    """
    method_type = (40, 10)
    field_info = (
        ('reserved_1', SHORT),
        ('exchange', SHORTSTR),
        ('type', SHORTSTR),
        ('passive', BIT),
        ('durable', BIT),
        ('auto_delete', BIT),
        ('internal', BIT),
        ('no_wait', BIT),
        ('arguments', TABLE),
    )
    synchronous = True


class ExchangeDeclareOK(BaseMethod):
    """This method confirms a Declare method and confirms the name of the
    exchange, essential for automatically-named exchanges.
    """
    method_type = (40, 11)
    field_info = ()
    synchronous = True


class ExchangeDelete(BaseMethod):
    """This method deletes an exchange. When an exchange is deleted all queue
    bindings on the exchange are cancelled.

    Arguments:
        reserved_1: SHORT
        exchange: SHORTSTR
        if_unused: BIT
        no_wait: BIT
    """
    method_type = (40, 20)
    field_info = (
        ('reserved_1', SHORT),
        ('exchange', SHORTSTR),
        ('if_unused', BIT),
        ('no_wait', BIT),
    )
    synchronous = True


class ExchangeDeleteOK(BaseMethod):
    """This method confirms the deletion of an exchange.
    """
    method_type = (40, 21)
    field_info = ()
    synchronous = True


class ExchangeBind(BaseMethod):
    """This method binds an exchange to an exchange.

    Arguments:
        reserved_1: SHORT
        destination: SHORTSTR
        source: SHORTSTR
        routing_key: SHORTSTR
        no_wait: BIT
        arguments: TABLE
    """
    method_type = (40, 30)
    field_info = (
        ('reserved_1', SHORT),
        ('destination', SHORTSTR),
        ('source', SHORTSTR),
        ('routing_key', SHORTSTR),
        ('no_wait', BIT),
        ('arguments', TABLE),
    )
    synchronous = True


class ExchangeBindOK(BaseMethod):
    """This method confirms that the bind was successful.
    """
    method_type = (40, 31)
    field_info = ()
    synchronous = True


class ExchangeUnbind(BaseMethod):
    """This method unbinds an exchange from an exchange.

    Arguments:
        reserved_1: SHORT
        destination: SHORTSTR
        source: SHORTSTR
        routing_key: SHORTSTR
        no_wait: BIT
        arguments: TABLE
    """
    method_type = (40, 40)
    field_info = (
        ('reserved_1', SHORT),
        ('destination', SHORTSTR),
        ('source', SHORTSTR),
        ('routing_key', SHORTSTR),
        ('no_wait', BIT),
        ('arguments', TABLE),
    )
    synchronous = True


class ExchangeUnbindOK(BaseMethod):
    """This method confirms that the unbind was successful.
    """
    method_type = (40, 51)
    field_info = ()
    synchronous = True


class QueueDeclare(BaseMethod):
    """This method creates or checks a queue. When creating a new queue the
    client can specify various properties that control the durability of the
    queue and its contents, and the level of sharing for the queue.

    Arguments:
        reserved_1: SHORT
        queue: SHORTSTR
        passive: BIT
        durable: BIT
        exclusive: BIT
        auto_delete: BIT
        no_wait: BIT
        arguments: TABLE
    """
    method_type = (50, 10)
    field_info = (
        ('reserved_1', SHORT),
        ('queue', SHORTSTR),
        ('passive', BIT),
        ('durable', BIT),
        ('exclusive', BIT),
        ('auto_delete', BIT),
        ('no_wait', BIT),
        ('arguments', TABLE),
    )
    synchronous = True


class QueueDeclareOK(BaseMethod):
    """This method confirms a Declare method and confirms the name of the
    queue, essential for automatically-named queues.

    Arguments:
        queue: SHORTSTR
        message_count: LONG
        consumer_count: LONG
    """
    method_type = (50, 11)
    field_info = (
        ('queue', SHORTSTR),
        ('message_count', LONG),
        ('consumer_count', LONG),
    )
    synchronous = True


class QueueBind(BaseMethod):
    """This method binds a queue to an exchange. Until a queue is bound it
    will not receive any messages. In a classic messaging model,
    store-and-forward queues are bound to a direct exchange and subscription
    queues are bound to a topic exchange.

    Arguments:
        reserved_1: SHORT
        queue: SHORTSTR
        exchange: SHORTSTR
        routing_key: SHORTSTR
        no_wait: BIT
        arguments: TABLE
    """
    method_type = (50, 20)
    field_info = (
        ('reserved_1', SHORT),
        ('queue', SHORTSTR),
        ('exchange', SHORTSTR),
        ('routing_key', SHORTSTR),
        ('no_wait', BIT),
        ('arguments', TABLE),
    )
    synchronous = True


class QueueBindOK(BaseMethod):
    """This method confirms that the bind was successful.
    """
    method_type = (50, 21)
    field_info = ()
    synchronous = True


class QueueUnbind(BaseMethod):
    """This method unbinds a queue from an exchange.

    Arguments:
        reserved_1: SHORT
        queue: SHORTSTR
        exchange: SHORTSTR
        routing_key: SHORTSTR
        arguments: TABLE
    """
    method_type = (50, 50)
    field_info = (
        ('reserved_1', SHORT),
        ('queue', SHORTSTR),
        ('exchange', SHORTSTR),
        ('routing_key', SHORTSTR),
        ('arguments', TABLE),
    )
    synchronous = True


class QueueUnbindOK(BaseMethod):
    """This method confirms that the unbind was successful.
    """
    method_type = (50, 51)
    field_info = ()
    synchronous = True


class QueuePurge(BaseMethod):
    """This method removes all messages from a queue which are not awaiting
    acknowledgment.

    Arguments:
        reserved_1: SHORT
        queue: SHORTSTR
        no_wait: BIT
    """
    method_type = (50, 30)
    field_info = (
        ('reserved_1', SHORT),
        ('queue', SHORTSTR),
        ('no_wait', BIT),
    )
    synchronous = True


class QueuePurgeOK(BaseMethod):
    """This method confirms the purge of a queue.

    Arguments:
        message_count: LONG
    """
    method_type = (50, 31)
    field_info = (
        ('message_count', LONG),
    )
    synchronous = True


class QueueDelete(BaseMethod):
    """This method deletes a queue. When a queue is deleted any pending
    messages are sent to a dead-letter queue if this is defined in the server
    configuration, and all consumers on the queue are cancelled.

    Arguments:
        reserved_1: SHORT
        queue: SHORTSTR
        if_unused: BIT
        if_empty: BIT
        no_wait: BIT
    """
    method_type = (50, 40)
    field_info = (
        ('reserved_1', SHORT),
        ('queue', SHORTSTR),
        ('if_unused', BIT),
        ('if_empty', BIT),
        ('no_wait', BIT),
    )
    synchronous = True


class QueueDeleteOK(BaseMethod):
    """This method confirms the deletion of a queue.

    Arguments:
        message_count: LONG
    """
    method_type = (50, 41)
    field_info = (
        ('message_count', LONG),
    )
    synchronous = True


class BasicQos(BaseMethod):
    """This method requests a specific quality of service. The QoS can be
    specified for the current channel or for all channels on the connection.
    The particular properties and semantics of a qos method always depend on
    the content class semantics. Though the qos method could in principle apply
    to both peers, it is currently meaningful only for the server.

    Arguments:
        prefetch_size: LONG
        prefetch_count: SHORT
        global: BIT
    """
    method_type = (60, 10)
    field_info = (
        ('prefetch_size', LONG),
        ('prefetch_count', SHORT),
        ('global', BIT),
    )
    synchronous = True


class BasicQosOK(BaseMethod):
    """This method tells the client that the requested QoS levels could be
    handled by the server. The requested QoS applies to all active consumers
    until a new QoS is defined.
    """
    method_type = (60, 11)
    field_info = ()
    synchronous = True


class BasicConsume(BaseMethod):
    """This method asks the server to start a "consumer", which is a transient
    request for messages from a specific queue. Consumers last as long as the
    channel they were declared on, or until the client cancels them.

    Arguments:
        reserved_1: SHORT
        queue: SHORTSTR
        consumer_tag: SHORTSTR
        no_local: BIT
        no_ack: BIT
        exclusive: BIT
        no_wait: BIT
        arguments: TABLE
    """
    method_type = (60, 20)
    field_info = (
        ('reserved_1', SHORT),
        ('queue', SHORTSTR),
        ('consumer_tag', SHORTSTR),
        ('no_local', BIT),
        ('no_ack', BIT),
        ('exclusive', BIT),
        ('no_wait', BIT),
        ('arguments', TABLE),
    )
    synchronous = True


class BasicConsumeOK(BaseMethod):
    """The server provides the client with a consumer tag, which is used by
    the client for methods called on the consumer at a later stage.

    Arguments:
        consumer_tag: SHORTSTR
    """
    method_type = (60, 21)
    field_info = (
        ('consumer_tag', SHORTSTR),
    )
    synchronous = True


class BasicCancel(BaseMethod):
    """This method cancels a consumer. This does not affect already delivered
    messages, but it does mean the server will not send any more messages for
    that consumer. The client may receive an arbitrary number of messages in
    between sending the cancel method and receiving the cancel-ok reply. It may
    also be sent from the server to the client in the event of the consumer
    being unexpectedly cancelled (i.e. cancelled for any reason other than the
    server receiving the corresponding basic.cancel from the client). This
    allows clients to be notified of the loss of consumers due to events such
    as queue deletion. Note that as it is not a MUST for clients to accept this
    method from the client, it is advisable for the broker to be able to
    identify those clients that are capable of accepting the method, through
    some means of capability negotiation.

    Arguments:
        consumer_tag: SHORTSTR
        no_wait: BIT
    """
    method_type = (60, 30)
    field_info = (
        ('consumer_tag', SHORTSTR),
        ('no_wait', BIT),
    )
    synchronous = True


class BasicCancelOK(BaseMethod):
    """This method confirms that the cancellation was completed.

    Arguments:
        consumer_tag: SHORTSTR
    """
    method_type = (60, 31)
    field_info = (
        ('consumer_tag', SHORTSTR),
    )
    synchronous = True


class BasicPublish(BaseMethod):
    """This method publishes a message to a specific exchange. The message
    will be routed to queues as defined by the exchange configuration and
    distributed to any active consumers when the transaction, if any, is
    committed.

    Arguments:
        reserved_1: SHORT
        exchange: SHORTSTR
        routing_key: SHORTSTR
        mandatory: BIT
        immediate: BIT
    """
    method_type = (60, 40)
    field_info = (
        ('reserved_1', SHORT),
        ('exchange', SHORTSTR),
        ('routing_key', SHORTSTR),
        ('mandatory', BIT),
        ('immediate', BIT),
    )
    synchronous = False


class BasicReturn(BaseMethod):
    """This method returns an undeliverable message that was published with
    the "immediate" flag set, or an unroutable message published with the
    "mandatory" flag set. The reply code and text provide information about the
    reason that the message was undeliverable.

    Arguments:
        reply_code: SHORT
        reply_text: SHORTSTR
        exchange: SHORTSTR
        routing_key: SHORTSTR
    """
    method_type = (60, 50)
    field_info = (
        ('reply_code', SHORT),
        ('reply_text', SHORTSTR),
        ('exchange', SHORTSTR),
        ('routing_key', SHORTSTR),
    )
    synchronous = False


class BasicDeliver(BaseMethod):
    """This method delivers a message to the client, via a consumer. In the
    asynchronous message delivery model, the client starts a consumer using the
    Consume method, then the server responds with Deliver methods as and when
    messages arrive for that consumer.

    Arguments:
        consumer_tag: SHORTSTR
        delivery_tag: LONGLONG
        redelivered: BIT
        exchange: SHORTSTR
        routing_key: SHORTSTR
    """
    method_type = (60, 60)
    field_info = (
        ('consumer_tag', SHORTSTR),
        ('delivery_tag', LONGLONG),
        ('redelivered', BIT),
        ('exchange', SHORTSTR),
        ('routing_key', SHORTSTR),
    )
    synchronous = False


class BasicGet(BaseMethod):
    """This method provides a direct access to the messages in a queue using a
    synchronous dialogue that is designed for specific types of application
    where synchronous functionality is more important than performance.

    Arguments:
        reserved_1: SHORT
        queue: SHORTSTR
        no_ack: BIT
    """
    method_type = (60, 70)
    field_info = (
        ('reserved_1', SHORT),
        ('queue', SHORTSTR),
        ('no_ack', BIT),
    )
    synchronous = True


class BasicGetOK(BaseMethod):
    """This method delivers a message to the client following a get method. A
    message delivered by 'get-ok' must be acknowledged unless the no-ack option
    was set in the get method.

    Arguments:
        delivery_tag: LONGLONG
        redelivered: BIT
        exchange: SHORTSTR
        routing_key: SHORTSTR
        message_count: LONG
    """
    method_type = (60, 71)
    field_info = (
        ('delivery_tag', LONGLONG),
        ('redelivered', BIT),
        ('exchange', SHORTSTR),
        ('routing_key', SHORTSTR),
        ('message_count', LONG),
    )
    synchronous = True


class BasicGetEmpty(BaseMethod):
    """This method tells the client that the queue has no messages available
    for the client.

    Arguments:
        reserved_1: SHORTSTR
    """
    method_type = (60, 72)
    field_info = (
        ('reserved_1', SHORTSTR),
    )
    synchronous = True


class BasicAck(BaseMethod):
    """When sent by the client, this method acknowledges one or more messages
    delivered via the Deliver or Get-Ok methods. When sent by server, this
    method acknowledges one or more messages published with the Publish method
    on a channel in confirm mode. The acknowledgement can be for a single
    message or a set of messages up to and including a specific message.

    Arguments:
        delivery_tag: LONGLONG
        multiple: BIT
    """
    method_type = (60, 80)
    field_info = (
        ('delivery_tag', LONGLONG),
        ('multiple', BIT),
    )
    synchronous = False


class BasicReject(BaseMethod):
    """This method allows a client to reject a message. It can be used to
    interrupt and cancel large incoming messages, or return untreatable
    messages to their original queue.

    Arguments:
        delivery_tag: LONGLONG
        requeue: BIT
    """
    method_type = (60, 90)
    field_info = (
        ('delivery_tag', LONGLONG),
        ('requeue', BIT),
    )
    synchronous = False


class BasicRecoverAsync(BaseMethod):
    """This method asks the server to redeliver all unacknowledged messages on
    a specified channel. Zero or more messages may be redelivered. This method
    is deprecated in favour of the synchronous Recover/Recover-Ok.

    Arguments:
        requeue: BIT
    """
    method_type = (60, 100)
    field_info = (
        ('requeue', BIT),
    )
    synchronous = False


class BasicRecover(BaseMethod):
    """This method asks the server to redeliver all unacknowledged messages on
    a specified channel. Zero or more messages may be redelivered. This method
    replaces the asynchronous Recover.

    Arguments:
        requeue: BIT
    """
    method_type = (60, 110)
    field_info = (
        ('requeue', BIT),
    )
    synchronous = False


class BasicRecoverOK(BaseMethod):
    """This method acknowledges a Basic.Recover method.
    """
    method_type = (60, 111)
    field_info = ()
    synchronous = True


class BasicNack(BaseMethod):
    """This method allows a client to reject one or more incoming messages. It
    can be used to interrupt and cancel large incoming messages, or return
    untreatable messages to their original queue. This method is also used by
    the server to inform publishers on channels in confirm mode of unhandled
    messages. If a publisher receives this method, it probably needs to
    republish the offending messages.

    Arguments:
        delivery_tag: LONGLONG
        multiple: BIT
        requeue: BIT
    """
    method_type = (60, 120)
    field_info = (
        ('delivery_tag', LONGLONG),
        ('multiple', BIT),
        ('requeue', BIT),
    )
    synchronous = False


class TxSelect(BaseMethod):
    """This method sets the channel to use standard transactions. The client
    must use this method at least once on a channel before using the Commit or
    Rollback methods.
    """
    method_type = (90, 10)
    field_info = ()
    synchronous = True


class TxSelectOK(BaseMethod):
    """This method confirms to the client that the channel was successfully
    set to use standard transactions.
    """
    method_type = (90, 11)
    field_info = ()
    synchronous = True


class TxCommit(BaseMethod):
    """This method commits all message publications and acknowledgments
    performed in the current transaction. A new transaction starts immediately
    after a commit.
    """
    method_type = (90, 20)
    field_info = ()
    synchronous = True


class TxCommitOK(BaseMethod):
    """This method confirms to the client that the commit succeeded. Note that
    if a commit fails, the server raises a channel exception.
    """
    method_type = (90, 21)
    field_info = ()
    synchronous = True


class TxRollback(BaseMethod):
    """This method abandons all message publications and acknowledgments
    performed in the current transaction. A new transaction starts immediately
    after a rollback. Note that unacked messages will not be automatically
    redelivered by rollback; if that is required an explicit recover call
    should be issued.
    """
    method_type = (90, 30)
    field_info = ()
    synchronous = True


class TxRollbackOK(BaseMethod):
    """This method confirms to the client that the rollback succeeded. Note
    that if an rollback fails, the server raises a channel exception.
    """
    method_type = (90, 31)
    field_info = ()
    synchronous = True


class ConfirmSelect(BaseMethod):
    """This method sets the channel to use publisher acknowledgements. The
    client can only use this method on a non-transactional channel.

    Arguments:
        nowait: BIT
    """
    method_type = (85, 10)
    field_info = (
        ('nowait', BIT),
    )
    synchronous = True


class ConfirmSelectOK(BaseMethod):
    """This method confirms to the client that the channel was successfully
    set to use publisher acknowledgements.
    """
    method_type = (85, 11)
    field_info = ()
    synchronous = True


METHODS = {
    (10, 10): ConnectionStart,
    (10, 11): ConnectionStartOK,
    (10, 20): ConnectionSecure,
    (10, 21): ConnectionSecureOK,
    (10, 30): ConnectionTune,
    (10, 31): ConnectionTuneOK,
    (10, 40): ConnectionOpen,
    (10, 41): ConnectionOpenOK,
    (10, 50): ConnectionClose,
    (10, 51): ConnectionCloseOK,
    (20, 10): ChannelOpen,
    (20, 11): ChannelOpenOK,
    (20, 20): ChannelFlow,
    (20, 21): ChannelFlowOK,
    (20, 40): ChannelClose,
    (20, 41): ChannelCloseOK,
    (40, 10): ExchangeDeclare,
    (40, 11): ExchangeDeclareOK,
    (40, 20): ExchangeDelete,
    (40, 21): ExchangeDeleteOK,
    (40, 30): ExchangeBind,
    (40, 31): ExchangeBindOK,
    (40, 40): ExchangeUnbind,
    (40, 51): ExchangeUnbindOK,
    (50, 10): QueueDeclare,
    (50, 11): QueueDeclareOK,
    (50, 20): QueueBind,
    (50, 21): QueueBindOK,
    (50, 50): QueueUnbind,
    (50, 51): QueueUnbindOK,
    (50, 30): QueuePurge,
    (50, 31): QueuePurgeOK,
    (50, 40): QueueDelete,
    (50, 41): QueueDeleteOK,
    (60, 10): BasicQos,
    (60, 11): BasicQosOK,
    (60, 20): BasicConsume,
    (60, 21): BasicConsumeOK,
    (60, 30): BasicCancel,
    (60, 31): BasicCancelOK,
    (60, 40): BasicPublish,
    (60, 50): BasicReturn,
    (60, 60): BasicDeliver,
    (60, 70): BasicGet,
    (60, 71): BasicGetOK,
    (60, 72): BasicGetEmpty,
    (60, 80): BasicAck,
    (60, 90): BasicReject,
    (60, 100): BasicRecoverAsync,
    (60, 110): BasicRecover,
    (60, 111): BasicRecoverOK,
    (60, 120): BasicNack,
    (90, 10): TxSelect,
    (90, 11): TxSelectOK,
    (90, 20): TxCommit,
    (90, 21): TxCommitOK,
    (90, 30): TxRollback,
    (90, 31): TxRollbackOK,
    (85, 10): ConfirmSelect,
    (85, 11): ConfirmSelectOK,
}

# AMQP constants
FRAME_METHOD = 1
FRAME_HEADER = 2
FRAME_BODY = 3
FRAME_HEARTBEAT = 8
FRAME_MIN_SIZE = 4096
FRAME_END = 206
REPLY_SUCCESS = 200
CONTENT_TOO_LARGE = 311
NO_CONSUMERS = 313
CONNECTION_FORCED = 320
INVALID_PATH = 402
ACCESS_REFUSED = 403
NOT_FOUND = 404
RESOURCE_LOCKED = 405
PRECONDITION_FAILED = 406
FRAME_ERROR = 501
SYNTAX_ERROR = 502
COMMAND_INVALID = 503
CHANNEL_ERROR = 504
UNEXPECTED_FRAME = 505
RESOURCE_ERROR = 506
NOT_ALLOWED = 530
NOT_IMPLEMENTED = 540
INTERNAL_ERROR = 541