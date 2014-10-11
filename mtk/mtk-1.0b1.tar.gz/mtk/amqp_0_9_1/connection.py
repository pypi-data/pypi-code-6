
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

import array
import logging
import socket
import ssl
import struct
import sys
import time
import threading
import traceback
import Queue

import asyncore

from channel import Channel
from error import *
from frame import *
from mechanism import PlainMechanism
from util import *
import gen
from gen.methods import methods

logger = logging.getLogger(__name__)

#######################################################################################################################

class Connection(object):

    INITIALIZED = "initialized"
    OPENING = "opening"
    OPEN = "open"
    TUNED = "tuned"
    CLOSING = "closing"
    CLOSED = "closed"

    channel_max = 65535

    def __init__(self,
                 host="localhost",
                 port=5672,
                 virtual_host="/",
                 mechanism=PlainMechanism(),
                 ssl_options=None,
                 heartbeat=0,
                 closed_callback=None,
                 response_timeout=10):
        self.state = Connection.INITIALIZED

        self.host = host
        self.port = port
        self.virtual_host = virtual_host
        self.mechanism = mechanism
        self.ssl_options = ssl_options

        self.heartbeat = HeartBeatThread(self,heartbeat)
        self.closed_callback = closed_callback
        self.response_timeout = response_timeout

        self._response = Queue.Queue()

        self._next_channel = 1
        self._channels = {}
        self._channel_lock = threading.RLock()

        self.frame_max = 1048576

        self.socket_reader = None

        self.error = None

        self.socket = AmqpSocket(host,port,ssl_options,self)
        self._connect()

        self.receiver = ReceiveThread(self,self.socket)
        self.receiver.start()
        
        self.heartbeat.start()

    def _connect(self):
        try:
            self._doConnect()
        except:
            self.state = Connection.CLOSED
            raise

    def _doConnect(self):
        self.state = Connection.OPENING
        self.socket.send(ProtocolHeader())

        # server sends ProtocolHeader or Connection.Start
        frame = self.socket.recv()
        if isinstance(frame,ProtocolHeader):
            self._protocolHeader(frame)
        elif isinstance(frame,gen.Connection.Start):
            self._connectionStart(frame)
        else:
            raise AmqpError("expected to receive protocol header or Connection.Start, not:\n%s" % frame)

        # server sends Connection.Tune
        frame = self.socket.recv()
        if not isinstance(frame,gen.Connection.Tune):
            raise AmqpError("expected to receive Connection.Tune, not:\n%s" % frame)
        self._connectionTune(frame)

        # send Connection.Open
        open = gen.Connection.Open()
        open.virtual_host = self.virtual_host
        open_ok = self.socket.send(open)
        frame = self.socket.recv()
        if isinstance(frame,gen.Connection.OpenOk):
            self.state = Connection.OPEN
        elif isinstance(frame,gen.Connection.Close):
            self._closeConnection(frame)
            raise AmqpError(frame)
        else:
            raise AmqpError("expected to receive Connection.OpenOk or Connection.Close, not:\n%s" % frame)


    def _protocolHeader(self, header):
        self.error = AmqpError("incompatible protocols\n"+
                               "client: "+str(ProtocolHeader())+"\n"+
                               "server: "+str(header))
        self.state = Connection.CLOSED
        
    def _connectionStart(self, start):
        if self.mechanism.type not in start.mechanisms.split():
            # broker doesn't expect Connection.Close
            raise AmqpError("client requested mechanism %s, but server only supports: %s" %
                            (self.mechanism.type,start.mechanisms))
        start_ok = gen.Connection.StartOk()
        self.mechanism.configureStartOk(start_ok)
        start_ok.locale = "en_US"
        self.socket.send(start_ok)

    def _connectionTune(self, tune):
        if tune.channel_max > 0:
            if tune.channel_max < self.channel_max:
                self.channel_max = tune.channel_max

        if tune.frame_max < self.frame_max:
            self.frame_max = tune.frame_max

        if tune.heartbeat > 0:
            if tune.heartbeat < self.heartbeat.interval:
                self.heartbeat.interval = tune.heartbeat

        tune_ok = gen.Connection.TuneOk()
        tune_ok.channel_max = self.channel_max
        tune_ok.frame_max = self.frame_max
        tune_ok.heartbeat = self.heartbeat.interval
        self.socket.send(tune_ok)


    def _send(self, frame):
        if self.state == Connection.CLOSED:
            raise MtkError("can't send, connection is closed")
        self.heartbeat.outgoing()
        self.socket.send(frame)

        if frame.channel != 0:
            return None
        if not frame.isRequest():
            return None

        try:
            response = self._response.get(True,self.response_timeout)
        except Queue.Empty:
            self._close("timeout waiting for response")
            raise MtkError("timeout waiting for response")
        else:
            if isinstance(response,MtkError):
                raise response
            if isinstance(response,gen.Connection.Close):
                raise MtkError(response.reply_text)
            return response
            
    def _receive(self, frame):
        logger.debug("received on connection")
        if frame.isResponse():
            self._response.put(frame)
        elif isinstance(frame,ProtocolHeader):
            self._protocolHeader(frame)
        elif isinstance(frame,gen.Connection.Start):
            self._connectionStart(frame)
        elif isinstance(frame,gen.Connection.Tune):
            self._connectionTune(frame)
        elif isinstance(frame,gen.Connection.Close):
            self._connectionClose(frame)
        elif isinstance(frame,HeartBeat):
            pass
        else:
            logger.error("connection received unexpected frame:\n%s",frame)


    def _error(self):
        (type,self.error,trace) = sys.exc_info()
        logger.warn(traceback.format_exc())
        self.state = Connection.CLOSING
        self._response.put(self.error)
        self._close("%s" % self.error)

    def _connectionClose(self, close):
        logger.info("server closed connection:")
        logger.info("%s",close)

        self.state = Connection.CLOSING

        close_ok = gen.Connection.CloseOk()
        try:
            self._send(close_ok)
        except MtkError:
            # in case the server shuts down without waiting for the CloseOk
            pass

        self._response.put(close)
        if close.reply_text != "":
            self.error = close.reply_text

        self._close(close.reply_text)

    def close(self, reply_code=200, reply_text="client done"):
        if self.state == Connection.CLOSED:
            return
        self.state = Connection.CLOSING

        logger.debug("closing connection...")
        close = gen.Connection.Close()
        close.reply_code = reply_code
        close.reply_text = reply_text
        try:
            close_ok = self._send(close)
        except MtkError:
            pass

        self._close(reply_text)

    def _close(self, reason):
        self.state = Connection.CLOSED
        self.socket.close()

        for channel_number in self._channels.keys():
            self._channels[channel_number]._close()

        if self.closed_callback is not None:
            self.closed_callback(reason)

    def channel(self, number=None):
        return Channel(self,number)

    def _getChannelNumber(self, number):
        with self._channel_lock:
            if number == None:
                # user could be specifing their own channel numbers, so test that _next_channel is ok
                while self._next_channel in self._channels:
                    self._next_channel += 1
                number = self._next_channel
                self._next_channel += 1
            else:
                # user could specify the same number more than once by mistake
                if number in self._channels:
                    raise AmqpError("channel %d has already been created" % number)

        if number > Connection.channel_max:
            raise AmqpError("no more channels can be created on this connection")

        return number

    def _addChannel(self, channel):
        with self._channel_lock:
            self._channels[channel.number] = channel

    def _removeChannel(self, channel):
        with self._channel_lock:
            del self._channels[channel.number]

#######################################################################################################################

class HeartBeatThread(threading.Thread):
    def __init__(self, connection, interval=0):
        threading.Thread.__init__(self)
        self.daemon = True
        self.connection = connection
        self.interval = interval
        self.last_outgoing = time.time()
        self.last_incoming = time.time()
        
    def outgoing(self):
        self.last_outgoing = time.time()

    def incoming(self):
        self.last_incoming = time.time()

    def run(self):
        while self.connection.state != Connection.CLOSING and self.connection.state != Connection.CLOSED:
            if self.interval == 0:
                pass
            else:
                cur_time = time.time()
                if cur_time - self.last_outgoing > self.interval:
                    self.connection._send(HeartBeat())
                if cur_time - self.last_incoming > self.interval * 2:
                    try:
                        raise AmqpError("haven't heard from peer in %d seconds" % int(cur_time-self.last_incoming))
                    except:
                        self.connection._error()
                    self.keep_running = False
            time.sleep(1)

#######################################################################################################################

class ReceiveThread(threading.Thread):
    def __init__(self, connection, socket):
        threading.Thread.__init__(self)
        self.daemon = True
        self.connection = connection
        self.socket = socket

    def run(self):
        while(self.socket.state != AmqpSocket.CLOSED):
            try:
                frame = self.socket.recv()
            except MtkError, e:
                self.connection._error()
            else:
                self.connection.heartbeat.incoming()
                if frame.channel != 0:
                    try:
                        self.connection._channels[frame.channel]._receive(frame)
                    except KeyError:
                        logger.error("connection received frame for unknown channel %s:\n%s",frame.channel,frame)
                else:
                    self.connection._receive(frame)

#######################################################################################################################

class AmqpSocket():

    OPEN = "open"
    CLOSED = "closed"

    def __init__(self, host, port, ssl_options, connection):
        self.state = AmqpSocket.CLOSED
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        if ssl_options is not None:
            self.socket = ssl.wrap_socket(self.socket,**ssl_options)
        self.socket.settimeout(connection.response_timeout)
        try:
            self.socket.connect((host,port))
        except socket.error, e:
            raise MtkError("socket connect failed: %s" % e)
        self.socket.settimeout(None)       

        self.state = AmqpSocket.OPEN

        self.connection = connection

    def close(self):
        self.socket.close()
        self.state = AmqpSocket.CLOSED

    def send(self, frame):
        if self.state == AmqpSocket.CLOSED:
            raise MtkError("socket is closed")
        logger.debug("sending %s",frame)
        try:
            self.socket.sendall(frame.pack())
        except socket.error, e:
            self.state = AmqpSocket.CLOSED
            raise MtkError("failed to send frame: %s" % e)
    
    def recv(self):
        if self.state == AmqpSocket.CLOSED:
            raise MtkError("socket is closed")
        incoming = self._recv(1)
        if incoming[0] == 'A':
            incoming += self._recv(4-len(incoming))
            if incoming != "AMQP":
                self.close()
                raise AmqpError("bad start of content header: "+amqp)
            incoming = self._recv(4)
            ph = ProtocolHeader()
            (zero,ph.major,ph.minor,ph.revision) = struct.unpack("!BBBB",incoming)
            logger.debug("received %s",ph)
            return ph
        else:
            incoming += self._recv(7-len(incoming))
            (frame_type,channel,size) = struct.unpack("!BHI",incoming)
            if size == 0:
                incoming = ""
            else:
                incoming = self._recv(size)
            frame = self._unpackFrame(frame_type, channel, incoming)
            incoming = self._recv(1)
            (end,) = struct.unpack("!B",incoming)
            if end != gen.constants.FRAME_END:
                raise AmqpError("didn't find frame_end")
            logger.debug("received %s",frame)
            return frame

    def _recv(self, num_bytes):
        buf = ""
        try:
            while (self.state == AmqpSocket.OPEN) and (len(buf) != num_bytes):
                buf += self.socket.recv(num_bytes-len(buf))
        except socket.error,e:
            self.state = AmqpSocket.CLOSED
            raise MtkError("failed to receive: %s" % e)
        if len(buf) < num_bytes:
            raise MtkError("only received %d bytes (expected %d)" % (len(buf),num_bytes))
        return buf

    def _unpackFrame(self, frame_type, channel, payload):
        if frame_type == gen.constants.FRAME_METHOD:
            (class_id,method_id) = struct.unpack_from("!HH",payload,0)
            #logger.debug("method frame %d.%d",class_id,method_id)
            if not (class_id,method_id) in methods:
                raise AmqpError("unknown method %d in class %d" % (method_id,class_id))
            return methods[(class_id,method_id)].unpackPayload(channel,payload)
        elif frame_type == gen.constants.FRAME_HEADER:
            return Header.unpackPayload(channel,payload)
        elif frame_type == gen.constants.FRAME_BODY:
            return Body.unpackPayload(channel,payload)
        elif frame_type == gen.constants.FRAME_HEARTBEAT:
            return HeartBeat.unpackPayload(channel,payload)
        else:
            raise AmqpError("ignoring unknown frame type: %d",frame_type)

#######################################################################################################################
