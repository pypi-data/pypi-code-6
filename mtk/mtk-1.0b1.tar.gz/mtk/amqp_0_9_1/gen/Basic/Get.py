

import struct

from mtk.amqp_0_9_1.frame import Method
from mtk.amqp_0_9_1.table import FieldTable

from GetOk import GetOk
from GetEmpty import GetEmpty

class Get(Method):
    """

        This method provides a direct access to the messages in a queue using a synchronous
        dialogue that is designed for specific types of application where synchronous
        functionality is more important than performance.
      
    """

    SYNCHRONOUS = True

    RESPONSE = []
    RESPONSE.append(GetOk)
    RESPONSE.append(GetEmpty)

    def __init__(self, channel=0):
        Method.__init__(self,60,70,channel)

        self.reserved_1 = 0    # short

        # Specifies the name of the queue to get a message from.
        self.queue = ""    # shortstr

        self.no_ack = 0    # bit


    def __str__(self, indent=""):
        mstr = indent + "Basic.Get:\n"
        mstr += indent + "    reserved_1: " + str(self.reserved_1) + "\n"
        mstr += indent + "    queue: " + str(self.queue) + "\n"
        mstr += indent + "    no_ack: " + str(self.no_ack) + "\n"
        return mstr


    def payloadSize(self):
        l = 4    # class-id (short), method-id (short)

        # reserved_1
        l += 2    # 16-bit integer

        # queue
        l += 1 + len(self.queue)    # short string

        # no_ack
        l += 1    # one to eight bits

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

        byte = 0
        if self.no_ack > 0:
            byte = byte | 1 << 0
        struct.pack_into("!B",buffer,offset,byte)
        offset += 1

        return offset

    @staticmethod
    def unpackPayload(channel, buffer):
        method = Get(channel)

        offset = 4    # class_id and method_id are already known

        (method.reserved_1,) = struct.unpack_from("!H",buffer,offset)
        offset += 2

        (strlen,) = struct.unpack_from("!B",buffer,offset)
        offset += 1
        (method.queue,) = struct.unpack_from("!%ds" % strlen,buffer,offset)
        offset += strlen

        (byte,) = struct.unpack_from("!B",buffer,offset)
        if byte & 1 << 0 > 0:
            method.no_ack = 1
        else:
            method.no_ack = 0
        offset += 1

        return method
