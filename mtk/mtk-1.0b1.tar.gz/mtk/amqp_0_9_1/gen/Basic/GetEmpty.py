

import struct

from mtk.amqp_0_9_1.frame import Method
from mtk.amqp_0_9_1.table import FieldTable


class GetEmpty(Method):
    """

        This method tells the client that the queue has no messages available for the
        client.
      
    """

    SYNCHRONOUS = True

    RESPONSE = []

    def __init__(self, channel=0):
        Method.__init__(self,60,72,channel)

        self.reserved_1 = ""    # shortstr


    def __str__(self, indent=""):
        mstr = indent + "Basic.GetEmpty:\n"
        mstr += indent + "    reserved_1: " + str(self.reserved_1) + "\n"
        return mstr


    def payloadSize(self):
        l = 4    # class-id (short), method-id (short)

        # reserved_1
        l += 1 + len(self.reserved_1)    # short string

        return l

    def packPayload(self, buffer):
        struct.pack_into("!HH",buffer,7,self._class_id,self._method_id)
        offset = 7 + 4

        struct.pack_into("!B",buffer,offset,len(self.reserved_1))
        offset += 1
        struct.pack_into("!%ds" % len(self.reserved_1),buffer,offset,self.reserved_1)
        offset += len(self.reserved_1)

        return offset

    @staticmethod
    def unpackPayload(channel, buffer):
        method = GetEmpty(channel)

        offset = 4    # class_id and method_id are already known

        (strlen,) = struct.unpack_from("!B",buffer,offset)
        offset += 1
        (method.reserved_1,) = struct.unpack_from("!%ds" % strlen,buffer,offset)
        offset += strlen

        return method
