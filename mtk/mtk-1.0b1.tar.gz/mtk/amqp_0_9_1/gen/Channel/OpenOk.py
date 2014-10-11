

import struct

from mtk.amqp_0_9_1.frame import Method
from mtk.amqp_0_9_1.table import FieldTable


class OpenOk(Method):
    """

        This method signals to the client that the channel is ready for use.
      
    """

    SYNCHRONOUS = True

    RESPONSE = []

    def __init__(self, channel=0):
        Method.__init__(self,20,11,channel)

        self.reserved_1 = ""    # longstr


    def __str__(self, indent=""):
        mstr = indent + "Channel.OpenOk:\n"
        mstr += indent + "    reserved_1: " + str(self.reserved_1) + "\n"
        return mstr


    def payloadSize(self):
        l = 4    # class-id (short), method-id (short)

        # reserved_1
        l += 4 + len(self.reserved_1)    # long string

        return l

    def packPayload(self, buffer):
        struct.pack_into("!HH",buffer,7,self._class_id,self._method_id)
        offset = 7 + 4

        struct.pack_into("!I",buffer,offset,len(self.reserved_1))
        offset += 4
        struct.pack_into("!%ds" % len(self.reserved_1),buffer,offset,self.reserved_1)
        offset += len(self.reserved_1)

        return offset

    @staticmethod
    def unpackPayload(channel, buffer):
        method = OpenOk(channel)

        offset = 4    # class_id and method_id are already known

        (strlen,) = struct.unpack_from("!I",buffer,offset)
        offset += 4
        (method.reserved_1,) = struct.unpack_from("!%ds" % strlen,buffer,offset)
        offset += strlen

        return method
