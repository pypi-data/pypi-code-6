

import struct

from mtk.amqp_0_9_1.frame import Method
from mtk.amqp_0_9_1.table import FieldTable

from DeclareOk import DeclareOk

class Declare(Method):
    """

        This method creates an exchange if it does not already exist, and if the exchange
        exists, verifies that it is of the correct and expected class.
      
    """

    SYNCHRONOUS = True

    RESPONSE = []
    RESPONSE.append(DeclareOk)

    def __init__(self, channel=0):
        Method.__init__(self,40,10,channel)

        self.reserved_1 = 0    # short

        self.exchange = ""    # shortstr

        # 
        # Each exchange belongs to one of a set of exchange types implemented by the
        # server. The exchange types define the functionality of the exchange - i.e. how
        # messages are routed through it. It is not valid or meaningful to attempt to
        # change the type of an existing exchange.
        # 
        self.type = ""    # shortstr

        # 
        # If set, the server will reply with Declare-Ok if the exchange already
        # exists with the same name, and raise an error if not.  The client can
        # use this to check whether an exchange exists without modifying the
        # server state. When set, all other method fields except name and no-wait
        # are ignored.  A declare with both passive and no-wait has no effect.
        # Arguments are compared for semantic equivalence.
        # 
        self.passive = 0    # bit

        # 
        # If set when creating a new exchange, the exchange will be marked as durable.
        # Durable exchanges remain active when a server restarts. Non-durable exchanges
        # (transient exchanges) are purged if/when a server restarts.
        # 
        self.durable = 0    # bit

        self.reserved_2 = 0    # bit

        self.reserved_3 = 0    # bit

        self.no_wait = 0    # bit

        # 
        # A set of arguments for the declaration. The syntax and semantics of these
        # arguments depends on the server implementation.
        # 
        self.arguments = FieldTable()    # table


    def __str__(self, indent=""):
        mstr = indent + "Exchange.Declare:\n"
        mstr += indent + "    reserved_1: " + str(self.reserved_1) + "\n"
        mstr += indent + "    exchange: " + str(self.exchange) + "\n"
        mstr += indent + "    type: " + str(self.type) + "\n"
        mstr += indent + "    passive: " + str(self.passive) + "\n"
        mstr += indent + "    durable: " + str(self.durable) + "\n"
        mstr += indent + "    reserved_2: " + str(self.reserved_2) + "\n"
        mstr += indent + "    reserved_3: " + str(self.reserved_3) + "\n"
        mstr += indent + "    no_wait: " + str(self.no_wait) + "\n"
        mstr += indent + "    arguments:\n"
        mstr += self.arguments.__str__(indent+"        ")
        return mstr


    def payloadSize(self):
        l = 4    # class-id (short), method-id (short)

        # reserved_1
        l += 2    # 16-bit integer

        # exchange
        l += 1 + len(self.exchange)    # short string

        # type
        l += 1 + len(self.type)    # short string

        # passive

        # durable

        # reserved_2

        # reserved_3

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

        struct.pack_into("!B",buffer,offset,len(self.exchange))
        offset += 1
        struct.pack_into("!%ds" % len(self.exchange),buffer,offset,self.exchange)
        offset += len(self.exchange)

        struct.pack_into("!B",buffer,offset,len(self.type))
        offset += 1
        struct.pack_into("!%ds" % len(self.type),buffer,offset,self.type)
        offset += len(self.type)

        byte = 0
        if self.passive > 0:
            byte = byte | 1 << 0

        if self.durable > 0:
            byte = byte | 1 << 1

        if self.reserved_2 > 0:
            byte = byte | 1 << 2

        if self.reserved_3 > 0:
            byte = byte | 1 << 3

        if self.no_wait > 0:
            byte = byte | 1 << 4
        struct.pack_into("!B",buffer,offset,byte)
        offset += 1

        offset = self.arguments.pack(buffer,offset)

        return offset

    @staticmethod
    def unpackPayload(channel, buffer):
        method = Declare(channel)

        offset = 4    # class_id and method_id are already known

        (method.reserved_1,) = struct.unpack_from("!H",buffer,offset)
        offset += 2

        (strlen,) = struct.unpack_from("!B",buffer,offset)
        offset += 1
        (method.exchange,) = struct.unpack_from("!%ds" % strlen,buffer,offset)
        offset += strlen

        (strlen,) = struct.unpack_from("!B",buffer,offset)
        offset += 1
        (method.type,) = struct.unpack_from("!%ds" % strlen,buffer,offset)
        offset += strlen

        (byte,) = struct.unpack_from("!B",buffer,offset)
        if byte & 1 << 0 > 0:
            method.passive = 1
        else:
            method.passive = 0

        (byte,) = struct.unpack_from("!B",buffer,offset)
        if byte & 1 << 1 > 0:
            method.durable = 1
        else:
            method.durable = 0

        (byte,) = struct.unpack_from("!B",buffer,offset)
        if byte & 1 << 2 > 0:
            method.reserved_2 = 1
        else:
            method.reserved_2 = 0

        (byte,) = struct.unpack_from("!B",buffer,offset)
        if byte & 1 << 3 > 0:
            method.reserved_3 = 1
        else:
            method.reserved_3 = 0

        (byte,) = struct.unpack_from("!B",buffer,offset)
        if byte & 1 << 4 > 0:
            method.no_wait = 1
        else:
            method.no_wait = 0
        offset += 1

        method.arguments = FieldTable()
        offset = method.arguments.unpack(buffer,offset)

        return method
