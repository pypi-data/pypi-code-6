

import struct

from mtk.amqp_0_9_1.frame import Method
from mtk.amqp_0_9_1.table import FieldTable


class FlowOk(Method):
    """

        Confirms to the peer that a flow command was received and processed.
      
    """

    SYNCHRONOUS = True

    RESPONSE = []

    def __init__(self, channel=0):
        Method.__init__(self,20,21,channel)

        # 
        # Confirms the setting of the processed flow method: 1 means the peer will start
        # sending or continue to send content frames; 0 means it will not.
        # 
        self.active = 0    # bit


    def __str__(self, indent=""):
        mstr = indent + "Channel.FlowOk:\n"
        mstr += indent + "    active: " + str(self.active) + "\n"
        return mstr


    def payloadSize(self):
        l = 4    # class-id (short), method-id (short)

        # active
        l += 1    # one to eight bits

        return l

    def packPayload(self, buffer):
        struct.pack_into("!HH",buffer,7,self._class_id,self._method_id)
        offset = 7 + 4

        byte = 0
        if self.active > 0:
            byte = byte | 1 << 0
        struct.pack_into("!B",buffer,offset,byte)
        offset += 1

        return offset

    @staticmethod
    def unpackPayload(channel, buffer):
        method = FlowOk(channel)

        offset = 4    # class_id and method_id are already known

        (byte,) = struct.unpack_from("!B",buffer,offset)
        if byte & 1 << 0 > 0:
            method.active = 1
        else:
            method.active = 0
        offset += 1

        return method
