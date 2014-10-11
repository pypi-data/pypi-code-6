

import struct

from mtk.amqp_0_9_1.frame import Method
from mtk.amqp_0_9_1.table import FieldTable


class CommitOk(Method):
    """

        This method confirms to the client that the commit succeeded. Note that if a commit
        fails, the server raises a channel exception.
      
    """

    SYNCHRONOUS = True

    RESPONSE = []

    def __init__(self, channel=0):
        Method.__init__(self,90,21,channel)

        pass

    def __str__(self, indent=""):
        mstr = indent + "Tx.CommitOk:\n"
        return mstr


    def payloadSize(self):
        l = 4    # class-id (short), method-id (short)

        return l

    def packPayload(self, buffer):
        struct.pack_into("!HH",buffer,7,self._class_id,self._method_id)
        offset = 7 + 4

        return offset

    @staticmethod
    def unpackPayload(channel, buffer):
        method = CommitOk(channel)

        offset = 4    # class_id and method_id are already known

        return method
