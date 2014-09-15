from functools import partial

from asyncio import coroutine

from . import spec
from .frame import FrameHandler
from .message import BasicMessage
from .utils import YieldFromContextManager
from .exceptions import QueueEmpty


class Channel(object):

    def __init__(self, connection, channel_id=None, on_open=None):
        if channel_id:
            connection._claim_channel_id(channel_id)
        else:
            channel_id = connection._get_free_channel_id()

        self.channel_id = channel_id
        self.connection = connection
        self.protocol = connection.protocol
        self.loop = connection.loop

        self.is_open = False
        self.active = True

        self.consumer_callbacks = {}
        self.cancel_callbacks = {}
        self.no_ack_consumers = set()
        self.events = set()

        self._confirm_selected = False

        self.handler = FrameHandler(self)
        self.handle = self.handler.handle

        # In case connection confirms publications
        if connection.confirm_publish:
            self.basic_publish = self.basic_publish_confirm

        self.on_open = on_open
        self.send_method = partial(connection.send_method,
                                   channel_id=channel_id)

        self._setup_callbacks()

    def _setup_callbacks(self):
        self.handler.update({
            spec.ChannelClose: self._on_close,
            spec.ChannelCloseOK: self._on_close_ok,
            spec.ChannelFlow: self._on_flow,
            spec.ChannelOpenOK: self._on_open_ok,
            spec.BasicCancel: self._on_basic_cancel,
            spec.BasicCancelOK: self._on_basic_cancel_ok,
            spec.BasicDeliver: self._on_basic_deliver,
            spec.BasicReturn: self._on_basic_return,
            spec.BasicAck: self._on_basic_ack,
        })

    def open(self):
        return (yield from self._do_open())

    def __enter__(self):
        raise RuntimeError(
            '"yield from" should be used as context manager exception')

    def __exit__(self, *args):
        pass

    def __iter__(self):
        # This is not a coroutine.  It is meant to enable the idiom:
        #
        #     with (yield from chan):
        #         <block>
        #
        # as an alternative to:
        #
        #     yield from chan.open()
        #     try:
        #         <block>
        #     finally:
        #         chan.close()
        yield from self.open()
        return YieldFromContextManager(self)

    @coroutine
    def _on_close(self, reply_code, reply_text, class_id, method_id,
                  method=spec.ChannelCloseOK):
        self.send_method(method, ())
        yield from self.channel._do_revive()
        # raise error_for_code(
        #     reply_code, reply_text, (class_id, method_id), ChannelError,
        # )

    @coroutine
    def _on_close_ok(self):
        self._do_close()
        self.handler.ready()

    @coroutine
    def _on_flow(self, active, method=spec.ChannelFlowOK):
        self.active = active
        self.send_method(method, (active,))

    def _do_open(self, method=spec.ChannelOpen,
                 reply_method=spec.ChannelOpenOK):
        if self.is_open:
            return
        with self.handler.wait_for(reply_method) as fut:
            self.send_method(method, ('',))
            return (yield from fut)

    @coroutine
    def _on_open_ok(self, reserved_1):
        self.is_open = True
        self.on_open and self.on_open(self)
        # AMQP_LOGGER.debug('Channel open')
        self.handler.ready()

    def _on_basic_cancel(self, consumer_tag):
        callback = self._remove_tag(consumer_tag)
        if callback:
            callback(consumer_tag)
        else:
            print('on basic cancel')
            # raise ConsumerCancelled(consumer_tag, spec.Basic.Cancel)

    def _on_basic_cancel_ok(self, consumer_tag):
        self._remove_tag(consumer_tag)
        self.handler.ready()

    def _remove_tag(self, consumer_tag):
        self.consumer_callbacks.pop(consumer_tag, None)
        self.cancel_callbacks.pop(consumer_tag, None)

    def _on_basic_deliver(self, consumer_tag, delivery_tag, redelivered,
                          exchange, routing_key, msg):
        msg.channel = self
        msg.delivery_info = {
            'consumer_tag': consumer_tag,
            'delivery_tag': delivery_tag,
            'redelivered': redelivered,
            'exchange': exchange,
            'routing_key': routing_key,
        }
        try:
            fun = self.consumer_callbacks[consumer_tag]
        except KeyError:
            pass
        else:
            fun(msg)

    def _on_basic_return(self, reply_code, reply_text,
                         exchange, routing_key, message):
        # exc = error_for_code(
        #     reply_code, reply_text, spec.Basic.Return, ChannelError,
        # )
        # TODO work with events
        exc = None
        handlers = self.events.get('basic_return')
        if not handlers:
            raise exc
        for callback in handlers:
            callback(exc, exchange, routing_key, message)

    def _on_basic_ack(self, delivery_tag, multiple):
        for callback in self.events['basic_ack']:
            callback(delivery_tag, multiple)

    def _do_close(self):
        self.is_open = False
        channel_id, self.channel_id = self.channel_id, None
        connection, self.connection = self.connection, None
        if connection:
            connection.channels.pop(channel_id, None)
            connection._available_channel_ids.append(channel_id)

    def _do_revive(self):
        self.is_open = True
        return (yield from self._do_open())

    def close(self, reply_code=0, reply_text='', class_id=0, method_id=0,
              method=spec.ChannelClose, reply_method=spec.ChannelCloseOK):
        if not self.is_open or self.connection is None:
            return
        with self.handler.wait_for(reply_method) as fut:
            self.send_method(
                method,
                (reply_code, reply_text, class_id, method_id),
            )
            res = yield from fut
            self._do_close()
            return res

    def flow(self, active, method=spec.ChannelFlow,
             reply_method=spec.ChannelFlowOK):
        with self.handler.wait_for(reply_method) as fut:
            self.send_method(method, (active,))
            return (yield from fut)

    # Work with Exchanges

    def exchange_declare(self, exchange, type, passive=False, durable=False,
                         auto_delete=False, internal=False, no_wait=False,
                         arguments=None, method=spec.ExchangeDeclare,
                         reply_method=spec.ExchangeDeclareOK):
        arguments = arguments or {}
        reply_method = None if no_wait else reply_method
        with self.handler.wait_for(reply_method) as fut:
            self.send_method(
                method,
                (0, exchange, type, passive, durable, auto_delete,
                 internal, no_wait, arguments),
            )
            return (yield from fut)

    def exchange_delete(self, exchange, if_unused=False, no_wait=False,
                        method=spec.ExchangeDelete,
                        reply_method=spec.ExchangeDeleteOK):
        reply_method = None if no_wait else reply_method
        with self.handler.wait_for(reply_method) as fut:
            self.send_method(method, (0, exchange, if_unused, no_wait))
            return (yield from fut)

    def exchange_bind(self, destination, source='', routing_key='',
                      no_wait=False, arguments=None,
                      method=spec.ExchangeBind,
                      reply_method=spec.ExchangeBindOK):
        arguments = arguments or {}
        reply_method = None if no_wait else reply_method
        with self.handler.wait_for(reply_method) as fut:
            self.send_method(
                method,
                (0, destination, source, routing_key,
                 no_wait, arguments),
            )
            return (yield from fut)

    def exchange_unbind(self, destination, source='', routing_key='',
                        no_wait=False, arguments=None,
                        method=spec.ExchangeUnbind,
                        reply_method=spec.ExchangeUnbindOK):
        arguments = arguments or {}
        reply_method = None if no_wait else reply_method
        with self.handler.wait_for(reply_method) as fut:
            self.send_method(
                method,
                (0, destination, source, routing_key, no_wait, arguments),
            )
            return (yield from fut)

    # Work with Queues

    def queue_bind(self, queue, exchange='', routing_key='', no_wait=False,
                   arguments=None, method=spec.QueueBind,
                   reply_method=spec.QueueBindOK):
        arguments = arguments or {}
        reply_method = None if no_wait else reply_method
        with self.handler.wait_for(reply_method) as fut:
            self.send_method(
                method,
                (0, queue, exchange, routing_key, no_wait, arguments),
            )
            return (yield from fut)

    def queue_unbind(self, queue, exchange='', routing_key='', no_wait=False,
                     arguments=None, method=spec.QueueUnbind,
                     reply_method=spec.QueueUnbindOK):
        arguments = arguments or {}
        reply_method = None if no_wait else reply_method
        with self.handler.wait_for(reply_method) as fut:
            self.send_method(
                method,
                (0, queue, exchange, routing_key, no_wait, arguments),
            )
            return (yield from fut)

    def queue_declare(self, queue, passive=False, durable=False,
                      exclusive=False, auto_delete=True, no_wait=False,
                      arguments=None, method=spec.QueueDeclare,
                      reply_method=spec.QueueDeclareOK):
        arguments = arguments or {}
        reply_method = None if no_wait else reply_method
        with self.handler.wait_for(reply_method) as fut:
            self.send_method(
                method,
                (0, queue, passive, durable, exclusive, auto_delete,
                 no_wait, arguments),
            )
            return (yield from fut)

    def queue_delete(self, queue, if_unused=False, if_empty=False,
                     no_wait=False, method=spec.QueueDelete,
                     reply_method=spec.QueueDeleteOK):
        reply_method = None if no_wait else reply_method
        with self.handler.wait_for(reply_method) as fut:
            self.send_method(method, (0, queue, if_unused, if_empty, no_wait))
            return (yield from fut)

    def queue_purge(self, queue, no_wait=False, method=spec.QueuePurge,
                    reply_method=spec.QueuePurgeOK):
        reply_method = None if no_wait else reply_method
        with self.handler.wait_for(reply_method) as fut:
            self.send_method(method, (0, queue, no_wait))
            return (yield from fut)

    # Work with Basic

    def basic_ack(self, delivery_tag, multiple=False,
                  method=spec.BasicAck):
        self.send_method(method, (delivery_tag, multiple))
        yield

    def basic_cancel(self, consumer_tag, no_wait=False,
                     method=spec.BasicCancel,
                     reply_method=spec.BasicCancelOK):
        reply_method = None if no_wait else reply_method
        with self.handler.wait_for(reply_method) as fut:
            self.send_method(method, (consumer_tag, no_wait))
            return (yield from fut)

    def basic_consume(self, queue, consumer_tag='', no_local=False,
                      no_ack=True, exclusive=False, no_wait=False,
                      arguments=None, consumer_callback=None, on_cancel=None,
                      method=spec.BasicConsume,
                      reply_method=spec.BasicConsumeOK):
        arguments = arguments or {}
        reply_method = None if no_wait else reply_method
        with self.handler.wait_for(reply_method) as fut:
            self.send_method(
                method,
                (0, queue, consumer_tag, no_local, no_ack, exclusive,
                 no_wait, arguments),
            )
            proposed_tag = yield from fut

        # In case consumer_tag was not provided
        if not no_wait and not consumer_tag:
            consumer_tag = proposed_tag

        assert consumer_tag

        self.consumer_callbacks[consumer_tag] = consumer_callback

        if on_cancel:
            self.cancel_callbacks[consumer_tag] = on_cancel
        if no_ack:
            self.no_ack_consumers.add(consumer_tag)
        return consumer_tag

    def basic_get(self, queue, no_ack=True, method=spec.BasicGet,
                  reply_method=(spec.BasicGetOK, spec.BasicGetEmpty)):
        with self.handler.wait_for(*reply_method) as fut:
            self.send_method(method, (0, queue, no_ack))
            res = yield from fut
            if not isinstance(res, BasicMessage):
                raise QueueEmpty('Queue "{}" is empty!')
            return res

    def _basic_publish(self, message, exchange, routing_key, mandatory=False,
                       immediate=False, method=spec.BasicPublish):
        self.send_method(
            method,
            (0, exchange, routing_key, mandatory, immediate),
            message=message,
            frame_size=self.connection.frame_max,
        )
        # This should also be a generator
        yield

    # In case connection does not confirm publications
    basic_publish = _basic_publish

    def basic_publish_confirm(self, *args, reply_method=spec.BasicAck,
                              **kwargs):
        if not self._confirm_selected:
            self._confirm_selected = True
            self.confirm_select()
        with self.handler.wait_for(reply_method) as fut:
            self._basic_publish(*args, **kwargs)
            return (yield from fut)

    def basic_qos(self, prefetch_size, prefetch_count, a_global=False,
                  method=spec.BasicQos):
        self.send_method(method, (prefetch_size, prefetch_count, a_global))

    def basic_recover_async(self, requeue=False,
                            method=spec.BasicRecoverAsync):
        """Deprecated"""
        self.send_method(method, (requeue,))

    def basic_recover(self, requeue=False, method=spec.BasicRecover,
                      reply_method=spec.BasicRecoverOK):
        with self.handler.wait_for(reply_method) as fut:
            self.send_method(method, (requeue,))
            return (yield from fut)

    def basic_reject(self, delivery_tag, requeue=False,
                     method=spec.BasicReject):
        self.send_method(method, (delivery_tag, requeue))

    # Work with transactions

    def tx_select(self, method=spec.TxSelect, reply_method=spec.TxSelectOK):
        with self.handler.wait_for(reply_method) as fut:
            self.send_method(method, ())
            return (yield from fut)

    def tx_commit(self, method=spec.TxCommit, reply_method=spec.TxCommitOK):
        with self.handler.wait_for(reply_method) as fut:
            self.send_method(method, ())
            return (yield from fut)

    def tx_rollback(self, method=spec.TxRollback,
                    reply_method=spec.TxRollbackOK):
        with self.handler.wait_for(reply_method) as fut:
            self.send_method(method, ())
            return (yield from fut)

    def confirm_select(self, nowait=False, method=spec.ConfirmSelect,
                       reply_method=spec.ConfirmSelectOK):
        reply_method = None if nowait else reply_method
        with self.handler.wait_for(reply_method) as fut:
            self.send_method(method, (nowait,))
            return (yield from fut)
