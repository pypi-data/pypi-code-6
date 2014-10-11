

import struct

from mtk.amqp_0_9_1.frame import Method
from mtk.amqp_0_9_1.table import FieldTable

from RollbackOk import RollbackOk

class Rollback(Method):
    """

        This method abandons all message publications and acknowledgments performed in
        the current transaction. A new transaction starts immediately after a rollback.
        Note that unacked messages will not be automatically redelivered by rollback;
        if that is required an explicit recover call should be issued.
      
    """

    SYNCHRONOUS = True

    RESPONSE = []
    RESPONSE.append(RollbackOk)

    def __init__(self, channel=0):
        Method.__init__(self,90,30,channel)

        pass

    def __str__(self, indent=""):
        mstr = indent + "Tx.Rollback:\n"
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
        method = Rollback(channel)

        offset = 4    # class_id and method_id are already known

        return method
