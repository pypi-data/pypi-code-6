

import struct

from mtk.amqp_0_9_1.frame import Method
from mtk.amqp_0_9_1.table import FieldTable


class SecureOk(Method):
    """

        This method attempts to authenticate, passing a block of SASL data for the security
        mechanism at the server side.
      
    """

    SYNCHRONOUS = True

    RESPONSE = []

    def __init__(self, channel=0):
        Method.__init__(self,10,21,channel)

        # 
        # A block of opaque data passed to the security mechanism. The contents of this
        # data are defined by the SASL security mechanism.
        # 
        self.response = ""    # longstr


    def __str__(self, indent=""):
        mstr = indent + "Connection.SecureOk:\n"
        mstr += indent + "    response: " + str(self.response) + "\n"
        return mstr


    def payloadSize(self):
        l = 4    # class-id (short), method-id (short)

        # response
        l += 4 + len(self.response)    # long string

        return l

    def packPayload(self, buffer):
        struct.pack_into("!HH",buffer,7,self._class_id,self._method_id)
        offset = 7 + 4

        struct.pack_into("!I",buffer,offset,len(self.response))
        offset += 4
        struct.pack_into("!%ds" % len(self.response),buffer,offset,self.response)
        offset += len(self.response)

        return offset

    @staticmethod
    def unpackPayload(channel, buffer):
        method = SecureOk(channel)

        offset = 4    # class_id and method_id are already known

        (strlen,) = struct.unpack_from("!I",buffer,offset)
        offset += 4
        (method.response,) = struct.unpack_from("!%ds" % strlen,buffer,offset)
        offset += strlen

        return method
