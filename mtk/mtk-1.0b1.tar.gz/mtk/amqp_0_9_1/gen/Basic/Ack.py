

import struct

from mtk.amqp_0_9_1.frame import Method
from mtk.amqp_0_9_1.table import FieldTable


class Ack(Method):
    """

        This method acknowledges one or more messages delivered via the Deliver or Get-Ok
        methods. The client can ask to confirm a single message or a set of messages up to
        and including a specific message.
      
    """

    SYNCHRONOUS = False

    RESPONSE = []

    def __init__(self, channel=0):
        Method.__init__(self,60,80,channel)

        self.delivery_tag = 0    # longlong

        # 
        # If set to 1, the delivery tag is treated as "up to and including", so that the
        # client can acknowledge multiple messages with a single method. If set to zero,
        # the delivery tag refers to a single message. If the multiple field is 1, and the
        # delivery tag is zero, tells the server to acknowledge all outstanding messages.
        # 
        self.multiple = 0    # bit


    def __str__(self, indent=""):
        mstr = indent + "Basic.Ack:\n"
        mstr += indent + "    delivery_tag: " + str(self.delivery_tag) + "\n"
        mstr += indent + "    multiple: " + str(self.multiple) + "\n"
        return mstr


    def payloadSize(self):
        l = 4    # class-id (short), method-id (short)

        # delivery_tag
        l += 8    # 64-bit integer

        # multiple
        l += 1    # one to eight bits

        return l

    def packPayload(self, buffer):
        struct.pack_into("!HH",buffer,7,self._class_id,self._method_id)
        offset = 7 + 4

        struct.pack_into("!Q",buffer,offset,self.delivery_tag)
        offset += 8

        byte = 0
        if self.multiple > 0:
            byte = byte | 1 << 0
        struct.pack_into("!B",buffer,offset,byte)
        offset += 1

        return offset

    @staticmethod
    def unpackPayload(channel, buffer):
        method = Ack(channel)

        offset = 4    # class_id and method_id are already known

        (method.delivery_tag,) = struct.unpack_from("!Q",buffer,offset)
        offset += 8

        (byte,) = struct.unpack_from("!B",buffer,offset)
        if byte & 1 << 0 > 0:
            method.multiple = 1
        else:
            method.multiple = 0
        offset += 1

        return method
