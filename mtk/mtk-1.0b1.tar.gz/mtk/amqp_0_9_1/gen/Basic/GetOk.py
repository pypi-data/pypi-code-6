

import struct

from mtk.amqp_0_9_1.frame import Method
from mtk.amqp_0_9_1.table import FieldTable


class GetOk(Method):
    """

        This method delivers a message to the client following a get method. A message
        delivered by 'get-ok' must be acknowledged unless the no-ack option was set in the
        get method.
      
    """

    SYNCHRONOUS = True

    RESPONSE = []

    def __init__(self, channel=0):
        Method.__init__(self,60,71,channel)

        self.delivery_tag = 0    # longlong

        self.redelivered = 0    # bit

        # 
        # Specifies the name of the exchange that the message was originally published to.
        # If empty, the message was published to the default exchange.
        # 
        self.exchange = ""    # shortstr

        # Specifies the routing key name specified when the message was published.
        self.routing_key = ""    # shortstr

        self.message_count = 0    # long


    def __str__(self, indent=""):
        mstr = indent + "Basic.GetOk:\n"
        mstr += indent + "    delivery_tag: " + str(self.delivery_tag) + "\n"
        mstr += indent + "    redelivered: " + str(self.redelivered) + "\n"
        mstr += indent + "    exchange: " + str(self.exchange) + "\n"
        mstr += indent + "    routing_key: " + str(self.routing_key) + "\n"
        mstr += indent + "    message_count: " + str(self.message_count) + "\n"
        return mstr


    def payloadSize(self):
        l = 4    # class-id (short), method-id (short)

        # delivery_tag
        l += 8    # 64-bit integer

        # redelivered
        l += 1    # one to eight bits

        # exchange
        l += 1 + len(self.exchange)    # short string

        # routing_key
        l += 1 + len(self.routing_key)    # short string

        # message_count
        l += 4    # 32-bit integer

        return l

    def packPayload(self, buffer):
        struct.pack_into("!HH",buffer,7,self._class_id,self._method_id)
        offset = 7 + 4

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

        struct.pack_into("!I",buffer,offset,self.message_count)
        offset += 4

        return offset

    @staticmethod
    def unpackPayload(channel, buffer):
        method = GetOk(channel)

        offset = 4    # class_id and method_id are already known

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

        (method.message_count,) = struct.unpack_from("!I",buffer,offset)
        offset += 4

        return method
