

import struct

from mtk.amqp_0_9_1.frame import Method
from mtk.amqp_0_9_1.table import FieldTable


class Reject(Method):
    """

        This method allows a client to reject a message. It can be used to interrupt and
        cancel large incoming messages, or return untreatable messages to their original
        queue.
      
    """

    SYNCHRONOUS = False

    RESPONSE = []

    def __init__(self, channel=0):
        Method.__init__(self,60,90,channel)

        self.delivery_tag = 0    # longlong

        # 
        # If requeue is true, the server will attempt to requeue the message.  If requeue
        # is false or the requeue  attempt fails the messages are discarded or dead-lettered.
        # 
        self.requeue = 0    # bit


    def __str__(self, indent=""):
        mstr = indent + "Basic.Reject:\n"
        mstr += indent + "    delivery_tag: " + str(self.delivery_tag) + "\n"
        mstr += indent + "    requeue: " + str(self.requeue) + "\n"
        return mstr


    def payloadSize(self):
        l = 4    # class-id (short), method-id (short)

        # delivery_tag
        l += 8    # 64-bit integer

        # requeue
        l += 1    # one to eight bits

        return l

    def packPayload(self, buffer):
        struct.pack_into("!HH",buffer,7,self._class_id,self._method_id)
        offset = 7 + 4

        struct.pack_into("!Q",buffer,offset,self.delivery_tag)
        offset += 8

        byte = 0
        if self.requeue > 0:
            byte = byte | 1 << 0
        struct.pack_into("!B",buffer,offset,byte)
        offset += 1

        return offset

    @staticmethod
    def unpackPayload(channel, buffer):
        method = Reject(channel)

        offset = 4    # class_id and method_id are already known

        (method.delivery_tag,) = struct.unpack_from("!Q",buffer,offset)
        offset += 8

        (byte,) = struct.unpack_from("!B",buffer,offset)
        if byte & 1 << 0 > 0:
            method.requeue = 1
        else:
            method.requeue = 0
        offset += 1

        return method
