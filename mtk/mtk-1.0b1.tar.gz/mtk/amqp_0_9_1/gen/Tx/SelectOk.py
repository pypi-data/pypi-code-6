

import struct

from mtk.amqp_0_9_1.frame import Method
from mtk.amqp_0_9_1.table import FieldTable


class SelectOk(Method):
    """

        This method confirms to the client that the channel was successfully set to use
        standard transactions.
      
    """

    SYNCHRONOUS = True

    RESPONSE = []

    def __init__(self, channel=0):
        Method.__init__(self,90,11,channel)

        pass

    def __str__(self, indent=""):
        mstr = indent + "Tx.SelectOk:\n"
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
        method = SelectOk(channel)

        offset = 4    # class_id and method_id are already known

        return method
