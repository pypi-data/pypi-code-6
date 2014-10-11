

import struct

from mtk.amqp_0_9_1.frame import Method
from mtk.amqp_0_9_1.table import FieldTable


class Deliver(Method):
    """

        This method delivers a message to the client, via a consumer. In the asynchronous
        message delivery model, the client starts a consumer using the Consume method, then
        the server responds with Deliver methods as and when messages arrive for that
        consumer.
      
    """

    SYNCHRONOUS = False

    RESPONSE = []

    def __init__(self, channel=0):
        Method.__init__(self,60,60,channel)

        self.consumer_tag = ""    # shortstr

        self.delivery_tag = 0    # longlong

        self.redelivered = 0    # bit

        # 
        # Specifies the name of the exchange that the message was originally published to.
        # May be empty, indicating the default exchange.
        # 
        self.exchange = ""    # shortstr

        # Specifies the routing key name specified when the message was published.
        self.routing_key = ""    # shortstr


    def __str__(self, indent=""):
        mstr = indent + "Basic.Deliver:\n"
        mstr += indent + "    consumer_tag: " + str(self.consumer_tag) + "\n"
        mstr += indent + "    delivery_tag: " + str(self.delivery_tag) + "\n"
        mstr += indent + "    redelivered: " + str(self.redelivered) + "\n"
        mstr += indent + "    exchange: " + str(self.exchange) + "\n"
        mstr += indent + "    routing_key: " + str(self.routing_key) + "\n"
        return mstr


    def payloadSize(self):
        l = 4    # class-id (short), method-id (short)

        # consumer_tag
        l += 1 + len(self.consumer_tag)    # short string

        # delivery_tag
        l += 8    # 64-bit integer

        # redelivered
        l += 1    # one to eight bits

        # exchange
        l += 1 + len(self.exchange)    # short string

        # routing_key
        l += 1 + len(self.routing_key)    # short string

        return l

    def packPayload(self, buffer):
        struct.pack_into("!HH",buffer,7,self._class_id,self._method_id)
        offset = 7 + 4

        struct.pack_into("!B",buffer,offset,len(self.consumer_tag))
        offset += 1
        struct.pack_into("!%ds" % len(self.consumer_tag),buffer,offset,self.consumer_tag)
        offset += len(self.consumer_tag)

        struct.pack_into("!Q",buffer,offset,self.delivery_tag)
        offset += 8

        byte = 0
        if self.redelivered > 0:
            byte = byte | 1 << 0
        struct.pack_into("!B",buffer,offset,byte)
        offset += 1

        struct.pack_into("!B",buffer,offset,len(self.exchange))
        offset += 1
        struct.pack_into("!%ds" % len(self.exchange),buffer,offset,self.exchange)
        offset += len(self.exchange)

        struct.pack_into("!B",buffer,offset,len(self.routing_key))
        offset += 1
        struct.pack_into("!%ds" % len(self.routing_key),buffer,offset,self.routing_key)
        offset += len(self.routing_key)

        return offset

    @staticmethod
    def unpackPayload(channel, buffer):
        method = Deliver(channel)

        offset = 4    # class_id and method_id are already known

        (strlen,) = struct.unpack_from("!B",buffer,offset)
        offset += 1
        (method.consumer_tag,) = struct.unpack_from("!%ds" % strlen,buffer,offset)
        offset += strlen

        (method.delivery_tag,) = struct.unpack_from("!Q",buffer,offset)
        offset += 8

        (byte,) = struct.unpack_from("!B",buffer,offset)
        if byte & 1 << 0 > 0:
            method.redelivered = 1
        else:
            method.redelivered = 0
        offset += 1

        (strlen,) = struct.unpack_from("!B",buffer,offset)
        offset += 1
        (method.exchange,) = struct.unpack_from("!%ds" % strlen,buffer,offset)
        offset += strlen

        (strlen,) = struct.unpack_from("!B",buffer,offset)
        offset += 1
        (method.routing_key,) = struct.unpack_from("!%ds" % strlen,buffer,offset)
        offset += strlen

        return method
