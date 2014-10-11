

import struct

from mtk.amqp_0_9_1.frame import Method
from mtk.amqp_0_9_1.table import FieldTable

from SelectOk import SelectOk

class Select(Method):
    """

        This method sets the channel to use standard transactions. The client must use this
        method at least once on a channel before using the Commit or Rollback methods.
      
    """

    SYNCHRONOUS = True

    RESPONSE = []
    RESPONSE.append(SelectOk)

    def __init__(self, channel=0):
        Method.__init__(self,90,10,channel)

        pass

    def __str__(self, indent=""):
        mstr = indent + "Tx.Select:\n"
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
        method = Select(channel)

        offset = 4    # class_id and method_id are already known

        return method
