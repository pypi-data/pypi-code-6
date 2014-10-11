

import struct

from mtk.amqp_0_9_1.frame import Method
from mtk.amqp_0_9_1.table import FieldTable


class RecoverOk(Method):
    """

        This method acknowledges a Basic.Recover method.
      
    """

    SYNCHRONOUS = True

    RESPONSE = []

    def __init__(self, channel=0):
        Method.__init__(self,60,111,channel)

        pass

    def __str__(self, indent=""):
        mstr = indent + "Basic.RecoverOk:\n"
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
        method = RecoverOk(channel)

        offset = 4    # class_id and method_id are already known

        return method
