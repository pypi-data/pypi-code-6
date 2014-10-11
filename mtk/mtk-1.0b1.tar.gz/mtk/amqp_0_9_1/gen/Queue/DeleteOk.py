

import struct

from mtk.amqp_0_9_1.frame import Method
from mtk.amqp_0_9_1.table import FieldTable


class DeleteOk(Method):
    """
This method confirms the deletion of a queue.
    """

    SYNCHRONOUS = True

    RESPONSE = []

    def __init__(self, channel=0):
        Method.__init__(self,50,41,channel)

        # Reports the number of messages deleted.
        self.message_count = 0    # long


    def __str__(self, indent=""):
        mstr = indent + "Queue.DeleteOk:\n"
        mstr += indent + "    message_count: " + str(self.message_count) + "\n"
        return mstr


    def payloadSize(self):
        l = 4    # class-id (short), method-id (short)

        # message_count
        l += 4    # 32-bit integer

        return l

    def packPayload(self, buffer):
        struct.pack_into("!HH",buffer,7,self._class_id,self._method_id)
        offset = 7 + 4

        struct.pack_into("!I",buffer,offset,self.message_count)
        offset += 4

        return offset

    @staticmethod
    def unpackPayload(channel, buffer):
        method = DeleteOk(channel)

        offset = 4    # class_id and method_id are already known

        (method.message_count,) = struct.unpack_from("!I",buffer,offset)
        offset += 4

        return method
