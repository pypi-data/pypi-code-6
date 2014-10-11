

import struct

from mtk.amqp_0_9_1.frame import Method
from mtk.amqp_0_9_1.table import FieldTable

from DeleteOk import DeleteOk

class Delete(Method):
    """

        This method deletes an exchange. When an exchange is deleted all queue bindings on
        the exchange are cancelled.
      
    """

    SYNCHRONOUS = True

    RESPONSE = []
    RESPONSE.append(DeleteOk)

    def __init__(self, channel=0):
        Method.__init__(self,40,20,channel)

        self.reserved_1 = 0    # short

        self.exchange = ""    # shortstr

        # 
        # If set, the server will only delete the exchange if it has no queue bindings. If
        # the exchange has queue bindings the server does not delete it but raises a
        # channel exception instead.
        # 
        self.if_unused = 0    # bit

        self.no_wait = 0    # bit


    def __str__(self, indent=""):
        mstr = indent + "Exchange.Delete:\n"
        mstr += indent + "    reserved_1: " + str(self.reserved_1) + "\n"
        mstr += indent + "    exchange: " + str(self.exchange) + "\n"
        mstr += indent + "    if_unused: " + str(self.if_unused) + "\n"
        mstr += indent + "    no_wait: " + str(self.no_wait) + "\n"
        return mstr


    def payloadSize(self):
        l = 4    # class-id (short), method-id (short)

        # reserved_1
        l += 2    # 16-bit integer

        # exchange
        l += 1 + len(self.exchange)    # short string

        # if_unused

        # no_wait
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

        byte = 0
        if self.if_unused > 0:
            byte = byte | 1 << 0

        if self.no_wait > 0:
            byte = byte | 1 << 1
        struct.pack_into("!B",buffer,offset,byte)
        offset += 1

        return offset

    @staticmethod
    def unpackPayload(channel, buffer):
        method = Delete(channel)

        offset = 4    # class_id and method_id are already known

        (method.reserved_1,) = struct.unpack_from("!H",buffer,offset)
        offset += 2

        (strlen,) = struct.unpack_from("!B",buffer,offset)
        offset += 1
        (method.exchange,) = struct.unpack_from("!%ds" % strlen,buffer,offset)
        offset += strlen

        (byte,) = struct.unpack_from("!B",buffer,offset)
        if byte & 1 << 0 > 0:
            method.if_unused = 1
        else:
            method.if_unused = 0

        (byte,) = struct.unpack_from("!B",buffer,offset)
        if byte & 1 << 1 > 0:
            method.no_wait = 1
        else:
            method.no_wait = 0
        offset += 1

        return method
