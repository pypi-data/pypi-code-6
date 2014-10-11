

import struct

from mtk.amqp_0_9_1.frame import Method
from mtk.amqp_0_9_1.table import FieldTable


class Recover(Method):
    """

        This method asks the server to redeliver all unacknowledged messages on a
        specified channel. Zero or more messages may be redelivered.  This method
        replaces the asynchronous Recover.
      
    """

    SYNCHRONOUS = False

    RESPONSE = []

    def __init__(self, channel=0):
        Method.__init__(self,60,110,channel)

        # 
        # If this field is zero, the message will be redelivered to the original
        # recipient. If this bit is 1, the server will attempt to requeue the message,
        # potentially then delivering it to an alternative subscriber.
        # 
        self.requeue = 0    # bit


    def __str__(self, indent=""):
        mstr = indent + "Basic.Recover:\n"
        mstr += indent + "    requeue: " + str(self.requeue) + "\n"
        return mstr


    def payloadSize(self):
        l = 4    # class-id (short), method-id (short)

        # requeue
        l += 1    # one to eight bits

        return l

    def packPayload(self, buffer):
        struct.pack_into("!HH",buffer,7,self._class_id,self._method_id)
        offset = 7 + 4

        byte = 0
        if self.requeue > 0:
            byte = byte | 1 << 0
        struct.pack_into("!B",buffer,offset,byte)
        offset += 1

        return offset

    @staticmethod
    def unpackPayload(channel, buffer):
        method = Recover(channel)

        offset = 4    # class_id and method_id are already known

        (byte,) = struct.unpack_from("!B",buffer,offset)
        if byte & 1 << 0 > 0:
            method.requeue = 1
        else:
            method.requeue = 0
        offset += 1

        return method
