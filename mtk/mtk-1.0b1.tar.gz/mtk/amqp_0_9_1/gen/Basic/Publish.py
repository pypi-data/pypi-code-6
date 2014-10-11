

import struct

from mtk.amqp_0_9_1.frame import Method
from mtk.amqp_0_9_1.table import FieldTable


class Publish(Method):
    """

        This method publishes a message to a specific exchange. The message will be routed
        to queues as defined by the exchange configuration and distributed to any active
        consumers when the transaction, if any, is committed.
      
    """

    SYNCHRONOUS = False

    RESPONSE = []

    def __init__(self, channel=0):
        Method.__init__(self,60,40,channel)

        self.reserved_1 = 0    # short

        # 
        # Specifies the name of the exchange to publish to. The exchange name can be
        # empty, meaning the default exchange. If the exchange name is specified, and that
        # exchange does not exist, the server will raise a channel exception.
        # 
        self.exchange = ""    # shortstr

        # 
        # Specifies the routing key for the message. The routing key is used for routing
        # messages depending on the exchange configuration.
        # 
        self.routing_key = ""    # shortstr

        # 
        # This flag tells the server how to react if the message cannot be routed to a
        # queue. If this flag is set, the server will return an unroutable message with a
        # Return method. If this flag is zero, the server silently drops the message.
        # 
        self.mandatory = 0    # bit

        # 
        # This flag tells the server how to react if the message cannot be routed to a
        # queue consumer immediately. If this flag is set, the server will return an
        # undeliverable message with a Return method. If this flag is zero, the server
        # will queue the message, but with no guarantee that it will ever be consumed.
        # 
        self.immediate = 0    # bit


    def __str__(self, indent=""):
        mstr = indent + "Basic.Publish:\n"
        mstr += indent + "    reserved_1: " + str(self.reserved_1) + "\n"
        mstr += indent + "    exchange: " + str(self.exchange) + "\n"
        mstr += indent + "    routing_key: " + str(self.routing_key) + "\n"
        mstr += indent + "    mandatory: " + str(self.mandatory) + "\n"
        mstr += indent + "    immediate: " + str(self.immediate) + "\n"
        return mstr


    def payloadSize(self):
        l = 4    # class-id (short), method-id (short)

        # reserved_1
        l += 2    # 16-bit integer

        # exchange
        l += 1 + len(self.exchange)    # short string

        # routing_key
        l += 1 + len(self.routing_key)    # short string

        # mandatory

        # immediate
        l += 1    # one to eight bits

        return l

    def packPayload(self, buffer):
        struct.pack_into("!HH",buffer,7,self._class_id,self._method_id)
        offset = 7 + 4

        struct.pack_into("!H",buffer,offset,self.reserved_1)
        offset += 2

        struct.pack_into("!B",buffer,offset,len(self.exchange))
        offset += 1
        struct.pack_into("!%ds" % len(self.exchange),buffer,offset,self.exchange)
        offset += len(self.exchange)

        struct.pack_into("!B",buffer,offset,len(self.routing_key))
        offset += 1
        struct.pack_into("!%ds" % len(self.routing_key),buffer,offset,self.routing_key)
        offset += len(self.routing_key)

        byte = 0
        if self.mandatory > 0:
            byte = byte | 1 << 0

        if self.immediate > 0:
            byte = byte | 1 << 1
        struct.pack_into("!B",buffer,offset,byte)
        offset += 1

        return offset

    @staticmethod
    def unpackPayload(channel, buffer):
        method = Publish(channel)

        offset = 4    # class_id and method_id are already known

        (method.reserved_1,) = struct.unpack_from("!H",buffer,offset)
        offset += 2

        (strlen,) = struct.unpack_from("!B",buffer,offset)
        offset += 1
        (method.exchange,) = struct.unpack_from("!%ds" % strlen,buffer,offset)
        offset += strlen

        (strlen,) = struct.unpack_from("!B",buffer,offset)
        offset += 1
        (method.routing_key,) = struct.unpack_from("!%ds" % strlen,buffer,offset)
        offset += strlen

        (byte,) = struct.unpack_from("!B",buffer,offset)
        if byte & 1 << 0 > 0:
            method.mandatory = 1
        else:
            method.mandatory = 0

        (byte,) = struct.unpack_from("!B",buffer,offset)
        if byte & 1 << 1 > 0:
            method.immediate = 1
        else:
            method.immediate = 0
        offset += 1

        return method
