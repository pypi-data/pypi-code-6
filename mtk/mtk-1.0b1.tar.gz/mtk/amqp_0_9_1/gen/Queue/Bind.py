

import struct

from mtk.amqp_0_9_1.frame import Method
from mtk.amqp_0_9_1.table import FieldTable

from BindOk import BindOk

class Bind(Method):
    """

        This method binds a queue to an exchange. Until a queue is bound it will not
        receive any messages. In a classic messaging model, store-and-forward queues
        are bound to a direct exchange and subscription queues are bound to a topic
        exchange.
      
    """

    SYNCHRONOUS = True

    RESPONSE = []
    RESPONSE.append(BindOk)

    def __init__(self, channel=0):
        Method.__init__(self,50,20,channel)

        self.reserved_1 = 0    # short

        # Specifies the name of the queue to bind.
        self.queue = ""    # shortstr

        self.exchange = ""    # shortstr

        # 
        # Specifies the routing key for the binding. The routing key is used for routing
        # messages depending on the exchange configuration. Not all exchanges use a
        # routing key - refer to the specific exchange documentation.  If the queue name
        # is empty, the server uses the last queue declared on the channel.  If the
        # routing key is also empty, the server uses this queue name for the routing
        # key as well.  If the queue name is provided but the routing key is empty, the
        # server does the binding with that empty routing key.  The meaning of empty
        # routing keys depends on the exchange implementation.
        # 
        self.routing_key = ""    # shortstr

        self.no_wait = 0    # bit

        # 
        # A set of arguments for the binding. The syntax and semantics of these arguments
        # depends on the exchange class.
        # 
        self.arguments = FieldTable()    # table


    def __str__(self, indent=""):
        mstr = indent + "Queue.Bind:\n"
        mstr += indent + "    reserved_1: " + str(self.reserved_1) + "\n"
        mstr += indent + "    queue: " + str(self.queue) + "\n"
        mstr += indent + "    exchange: " + str(self.exchange) + "\n"
        mstr += indent + "    routing_key: " + str(self.routing_key) + "\n"
        mstr += indent + "    no_wait: " + str(self.no_wait) + "\n"
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

        # no_wait
        l += 1    # one to eight bits

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

        byte = 0
        if self.no_wait > 0:
            byte = byte | 1 << 0
        struct.pack_into("!B",buffer,offset,byte)
        offset += 1

        offset = self.arguments.pack(buffer,offset)

        return offset

    @staticmethod
    def unpackPayload(channel, buffer):
        method = Bind(channel)

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

        (byte,) = struct.unpack_from("!B",buffer,offset)
        if byte & 1 << 0 > 0:
            method.no_wait = 1
        else:
            method.no_wait = 0
        offset += 1

        method.arguments = FieldTable()
        offset = method.arguments.unpack(buffer,offset)

        return method
