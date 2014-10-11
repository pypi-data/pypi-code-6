
###############################################################################
#   Copyright 2012 Warren Smith                                               #
#                                                                             #
#   Licensed under the Apache License, Version 2.0 (the "License");           #
#   you may not use this file except in compliance with the License.          #
#   You may obtain a copy of the License at                                   #
#                                                                             #
#       http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                             #
#   Unless required by applicable law or agreed to in writing, software       #
#   distributed under the License is distributed on an "AS IS" BASIS,         #
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  #
#   See the License for the specific language governing permissions and       #
#   limitations under the License.                                            #
###############################################################################

import logging
import threading
import traceback
import Queue

from error import *
import gen
from util import bit
from frame import Body
from frame import Header

logger = logging.getLogger(__name__)

#######################################################################################################################

class Channel(object):

    OPENING = "opening"
    OPEN = "open"
    CLOSING = "closing"
    CLOSED = "closed"

    def __init__(self, connection, number=None, callback_threads=1):
        self.connection = connection

        self.number = connection._getChannelNumber(number)
        self.state = Channel.OPENING

        self.connection._addChannel(self)

        self._lock = threading.RLock()  # generally only want 1 method at a time on a channel

        self._response = Queue.Queue(1)
        self.error = None

        self._deliver = None
        self._get = None
        self._header = None
        self._body = []
        self._get_content = Queue.Queue(1)

        self._subscriptions = {}  # consumer_tag -> (no_ack,callback)
        self._callback_queue = Queue.Queue()
        self._callback_threads = []
        for i in range(0,callback_threads):
            thread = _CallbackThread(self)
            self._callback_threads.append(thread)
            thread.start()

        open_ok = self._send(gen.Channel.Open(self.number))

        self.state = Channel.OPEN

    def _checkNotClosed(self):
        if self.state == Channel.CLOSED:
            if self.error is None:
                raise MtkError("channel %d is closed" % self.number)
            else:
                raise MtkError("channel %d is closed: %s" % (self.number,self.error))

    def _send(self, frame):
        with self._lock:
            self._checkNotClosed()

            try:
                self.connection._send(frame)
            except:
                self._close()
                
            if not frame.isRequest():
                return None

            try:
                response = self._response.get(True,self.connection.response_timeout)
            except Queue.Empty:
                self._close()
                raise MtkError("timed out waiting for response")
        
            if isinstance(response,AmqpError):
                raise response
            if isinstance(response,MtkError):
                raise response
            if isinstance(response,gen.Connection.Close):
                self.error = response.reply_text
                raise MtkError(response.reply_text)
            if isinstance(response,gen.Channel.Close):
                self.error = response.reply_text
                raise MtkError(response.reply_text)
            return response

    def _receive(self, frame):
        logger.debug("received on channel")
        if isinstance(frame,gen.Basic.Deliver):
            self._basicDeliver(frame)
        elif isinstance(frame,Header):
            self._contentHeader(frame)
        elif isinstance(frame,Body):
            self._contentBody(frame)
        elif isinstance(frame,gen.Channel.Close):
            self._response.put(frame)
            self._channelClose(frame)
        elif frame.isResponse():
            self._response.put(frame)
        else:
            logger.error("channel %d received unexpected frame:\n%s",self.number,frame)

    def _basicDeliver(self, frame):
        self._deliver = frame

    def _contentHeader(self, frame):
        if self._deliver is None and self._get is None:
            logger.warn("unexpected header on channel %d" % header.channel)
            # should send a connection exception with reply code 505
            return
        self._header = frame

    def _contentBody(self, frame):
        if self._header is None:
            logger.warn("unexpected body on channel %d" % header.channel)
            # should send a connection exception with reply code 505
            return
        self._body.append(frame)

        if reduce(lambda size, body: size + body.payloadSize(),self._body,0) == self._header.body_size:
            #''.join(map(lambda body: body.content))
            content = reduce(lambda buf, body: buf + body.content,self._body,"")
            if self._deliver is not None:
                self._handleDelivery(content)
            elif self._get is not None:
                self._handleGet(content)
            else:
                logger.error("couldn't deliver content: %s",content)
            self._header = None
            self._body = []

    def _handleDelivery(self, content):
        self._callback_queue.put((self._deliver.consumer_tag,
                                  self._deliver.delivery_tag,
                                  self._deliver.exchange,
                                  self._deliver.routing_key,
                                  content))
        self._deliver = None

    def _handleGet(self, content):
        self._get_content.put(content)
        if not self._get.no_ack:
            ack = gen.Basic.Ack(self.number)
            ack.delivery_tag = self._get.delivery_tag
            self._send(ack)
        self._get = None

    def close(self, reply_code=200, reply_text="client done with channel"):
        print("close")
        with self._lock:
            self._checkNotClosed()

            self.state = Channel.CLOSING

            close = gen.Channel.Close(self.number)
            close.reply_code = reply_code
            close.reply_text = reply_text
            try:
                close_ok = self._send(close)
            finally:
                self._close()

    def _channelClose(self, close):
        logger.info("server closed channel:")
        logger.info(str(close))

        self.state = Channel.CLOSING

        close_ok = gen.Channel.CloseOk(self.number)
        self._send(close_ok)

        self._close()

    def _close(self):
        self.connection._removeChannel(self)

        self.state = Channel.CLOSED
        for thread in self._callback_threads:
            thread.join()

    EXCHANGE_TYPES = set(["direct","fanout","topic","headers","system"])

    def exchangeDeclare(self,
                        exchange="",
                        type="direct",
                        passive=False,
                        durable=False):
        if type not in Channel.EXCHANGE_TYPES:
            raise AmqpError("'%s' is not a valid exchange type" % type)

        declare = gen.Exchange.Declare(self.number)
        declare.exchange=exchange
        declare.type = type
        declare.passive = bit(passive)
        declare.durable = bit(durable)

        declare_ok = self._send(declare)

    def exchangeDelete(self,
                       exchange="",
                       if_unused=False):
        delete = gen.Exchange.Delete(self.number)
        delete.exchange=exchange
        delete.if_unused = bit(if_unused)

        delete_ok = self._send(delete)

    def queueDeclare(self,
                     queue="",
                     passive=False,
                     durable=False,
                     exclusive=True,
                     auto_delete=False):
        declare = gen.Queue.Declare(self.number)
        declare.queue = queue
        declare.passive = bit(passive)
        declare.durable = bit(durable)
        declare.exclusive = bit(exclusive)
        declare.auto_delete = bit(auto_delete)

        declare_ok = self._send(declare)

        return declare_ok.queue

    def queueBind(self,
                  queue="",
                  exchange="",
                  routing_key=""):
        bind = gen.Queue.Bind(self.number)
        bind.queue = queue
        bind.exchange = exchange
        bind.routing_key = routing_key

        bind_ok = self._send(bind)

    def queueUnbind(self,
                    queue="",
                    exchange="",
                    routing_key=""):
        unbind = gen.Queue.Unbind(self.number)
        unbind.queue = queue
        unbind.exchange = exchange
        unbind.routing_key = routing_key

        unbind_ok = self._send(unbind)

    def queuePurge(self,
                   queue=""):
        purge = gen.Queue.Purge(self.number)
        purge.queue = queue
        purge_ok = self._send(purge)

    def queueDelete(self,
                    queue="",
                    if_unused=False,
                    if_unempty=False):
        delete = gen.Queue.Delete(self.number)
        delete.queue = queue
        delete.if_unused = bit(if_unused)
        delete.if_unempty = bit(if_unempty)

        delete_ok = self._send(delete)

        return delete_ok.message_count    # number of messages deleted

    def basicConsume(self,
                     callback,
                     queue="",
                     consumer_tag="",
                     no_local=False,
                     no_ack=True,
                     exclusive=True):
        # content could arrive on the Connection thread before the register, so lock
        with self._lock:
            # server will generate a tag if client doesn't provide
            consume = gen.Basic.Consume(self.number)
            consume.queue = queue
            consume.consumer_tag = consumer_tag
            consume.no_local = bit(no_local)
            consume.no_ack = bit(no_ack)
            consume.exclusive = bit(exclusive)

            consume_ok = self._send(consume)
            self._subscriptions[consume_ok.consumer_tag] = (no_ack,callback)
        return consume_ok.consumer_tag

    def basicCancel(self,
                    consumer_tag):
        with self._lock:
            self._checkNotClosed()
            cancel = gen.Basic.Cancel(self.number)
            cancel.consumer_tag = consumer_tag

            cancel_ok = self._send(cancel)
            del self._subscriptions[consumer_tag]

    def basicPublish(self,
                     content,
                     exchange="",
                     routing_key="",
                     mandatory=False,
                     immediate=False):
        with self._lock:
            publish = gen.Basic.Publish(self.number)
            publish.exchange = exchange
            publish.routing_key = routing_key
            publish.mandatory = bit(mandatory)
            publish.immediate = bit(immediate)
            self._send(publish)

            header = Header(self.number, publish._class_id, len(content))
            logger.debug("sending %s",header)
            self._send(header)

            content_max = self.connection.frame_max - 7 - 1 - 1
            index = 0
            while index < len(content):
                content_size = min(len(content)-index,content_max)
                body = Body(self.number,content[index:index+content_size])
                logger.debug("sending body %s",body)
                self._send(body)
                index += content_size

    def basicGet(self,
                 queue="",
                 no_ack=True):
        # content could arrive on the Connection before the register, so lock
        with self._lock:
            get = gen.Basic.Get(self.number)
            get.queue = queue
            get.no_ack = bit(no_ack)

            self._get = get
            get_ok_empty = channel._send(get)
            if isinstance(get_ok_empty,gen.Basic.GetEmpty):
                return (None, 0, None)
            elif isinstance(get_ok_empty,gen.Basic.GetOk):
                content = self._get_content.get()
                return (get_ok_empty.routing_key,get_ok_empty.message_count,content)
            else:
                raise AmqpError("unexpected response to Basic.Get: "+str(get_ok_empty))

    def basicReject(self,
                    delivery_tag,
                    requeue=True):
        reject = gen.Basic.Reject(self.number)
        reject.delivery_tag = delivery_tag
        reject.requeue = bit(requeue)

        self._send(reject)

    def txSelect(self):
        select = gen.Tx.Select(self.number)
        select_ok = self._send(select)

    def txCommit(self):
        commit = gen.Tx.Commit(self.number)
        commit_ok = self._send(commit)

    def txRollback(self):
        rollback = gen.Tx.Rollback(self.number)
        rollback_ok = self._send(rollback)

#######################################################################################################################

class _CallbackThread(threading.Thread):
    def __init__(self, channel):
        threading.Thread.__init__(self)
        self.daemon = True
        self.channel = channel

    def run(self):
        while self.channel.state != Channel.CLOSED:
            try:
                (consumer_tag,
                 delivery_tag,
                 exchange,
                 routing_key,
                 content) = self.channel._callback_queue.get(True,1.0)
            except Queue.Empty:
                # no consumer callbacks to make
                continue
            except:
                break

            with self.channel._lock:  # let basicConsume complete before trying to deliver the first message
                try:
                    (no_ack,callback) = self.channel._subscriptions[consumer_tag]
                except KeyError:
                    logger.error("unknown consumer tag: %s",consumer_tag)
                    self.channel.close(500,"unknown consumer tag '%s'" % consumer_tag)
                    break
            try:
                callback(consumer_tag,routing_key,exchange,content)
            except:
                logger.warning("callback exception for %s (not acking): %s",consumer_tag,traceback.format_exc())
                continue  # don't ack if callback raises an exception
            if not no_ack:
                ack = gen.Basic.Ack(self.channel.number)
                ack.delivery_tag = delivery_tag
                try:
                    self.channel._send(ack)
                except MtkError, e:
                    pass  # channel could be closed

#######################################################################################################################
