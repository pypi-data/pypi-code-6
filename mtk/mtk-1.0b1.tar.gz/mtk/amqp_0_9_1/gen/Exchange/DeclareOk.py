

import struct

from mtk.amqp_0_9_1.frame import Method
from mtk.amqp_0_9_1.table import FieldTable


class DeclareOk(Method):
    """

        This method confirms a Declare method and confirms the name of the exchange,
        essential for automatically-named exchanges.
      
    """

    SYNCHRONOUS = True

    RESPONSE = []

    def __init__(self, channel=0):
        Method.__init__(self,40,11,channel)

        pass

    def __str__(self, indent=""):
        mstr = indent + "Exchange.DeclareOk:\n"
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
        method = DeclareOk(channel)

        offset = 4    # class_id and method_id are already known

        return method
