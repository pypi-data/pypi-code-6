

import struct

from mtk.amqp_0_9_1.frame import Method
from mtk.amqp_0_9_1.table import FieldTable

from UnbindOk import UnbindOk

class Unbind(Method):
    """
This method unbinds a queue from an exchange.
    """

    SYNCHRONOUS = True

    RESPONSE = []
    RESPONSE.append(UnbindOk)

    def __init__(self, channel=0):
        Method.__init__(self,50,50,channel)

        self.reserved_1 = 0    # short

        # Specifies the name of the queue to unbind.
        self.queue = ""    # shortstr

        # The name of the exchange to unbind from.
        self.exchange = ""    # shortstr

        # Specifies the routing key of the binding to unbind.
        self.routing_key = ""    # shortstr

        # Specifies the arguments of the binding to unbind.
        self.arguments = FieldTable()    # table


    def __str__(self, indent=""):
        mstr = indent + "Queue.Unbind:\n"
        mstr += indent + "    reserved_1: " + str(self.reserved_1) + "\n"
        mstr += indent + "    queue: " + str(self.queue) + "\n"
        mstr += indent + "    exchange: " + str(self.exchange) + "\n"
        mstr += indent + "    routing_key: " + str(self.routing_key) + "\n"
        mstr += indent + "    arguments:\n"
        mstr += self.arguments.__str__(indent+"        ")
        return mstr


    def payloadSize(self):
        l = 4    # class-id (short), method-id (short)

        # reserved_1
        l += 2    # 16-bit integer

        # queue
        l += 1 + len(self.queue)    # short string

        # exchange
        l += 1 + len(self.exchange)    # short string

        # routing_key
        l += 1 + len(self.routing_key)    # short string

        # arguments
        l += self.arguments.length()

        return l

    def packPayload(self, buffer):
        struct.pack_into("!HH",buffer,7,self._class_id,self._method_id)
        offset = 7 + 4

        struct.pack_into("!H",buffer,offset,self.reserved_1)
        offset += 2

        struct.pack_into("!B",buffer,offset,len(self.queue))
        offset += 1
        struct.pack_into("!%ds" % len(self.queue),buffer,offset,self.queue)
        offset += len(self.queue)

        struct.pack_into("!B",buffer,offset,len(self.exchange))
        offset += 1
        struct.pack_into("!%ds" % len(self.exchange),buffer,offset,self.exchange)
        offset += len(self.exchange)

        struct.pack_into("!B",buffer,offset,len(self.routing_key))
        offset += 1
        struct.pack_into("!%ds" % len(self.routing_key),buffer,offset,self.routing_key)
        offset += len(self.routing_key)

        offset = self.arguments.pack(buffer,offset)

        return offset

    @staticmethod
    def unpackPayload(channel, buffer):
        method = Unbind(channel)

        offset = 4    # class_id and method_id are already known

        (method.reserved_1,) = struct.unpack_from("!H",buffer,offset)
        offset += 2

        (strlen,) = struct.unpack_from("!B",buffer,offset)
        offset += 1
        (method.queue,) = struct.unpack_from("!%ds" % strlen,buffer,offset)
        offset += strlen

        (strlen,) = struct.unpack_from("!B",buffer,offset)
        offset += 1
        (method.exchange,) = struct.unpack_from("!%ds" % strlen,buffer,offset)
        offset += strlen

        (strlen,) = struct.unpack_from("!B",buffer,offset)
        offset += 1
        (method.routing_key,) = struct.unpack_from("!%ds" % strlen,buffer,offset)
        offset += strlen

        method.arguments = FieldTable()
        offset = method.arguments.unpack(buffer,offset)

        return method
