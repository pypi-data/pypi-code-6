

import struct

from mtk.amqp_0_9_1.frame import Method
from mtk.amqp_0_9_1.table import FieldTable

from FlowOk import FlowOk

class Flow(Method):
    """

        This method asks the peer to pause or restart the flow of content data sent by
        a consumer. This is a simple flow-control mechanism that a peer can use to avoid
        overflowing its queues or otherwise finding itself receiving more messages than
        it can process. Note that this method is not intended for window control. It does
        not affect contents returned by Basic.Get-Ok methods.
      
    """

    SYNCHRONOUS = True

    RESPONSE = []
    RESPONSE.append(FlowOk)

    def __init__(self, channel=0):
        Method.__init__(self,20,20,channel)

        # 
        # If 1, the peer starts sending content frames. If 0, the peer stops sending
        # content frames.
        # 
        self.active = 0    # bit


    def __str__(self, indent=""):
        mstr = indent + "Channel.Flow:\n"
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
        method = Flow(channel)

        offset = 4    # class_id and method_id are already known

        (byte,) = struct.unpack_from("!B",buffer,offset)
        if byte & 1 << 0 > 0:
            method.active = 1
        else:
            method.active = 0
        offset += 1

        return method
