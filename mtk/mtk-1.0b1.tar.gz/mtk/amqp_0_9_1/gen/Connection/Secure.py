

import struct

from mtk.amqp_0_9_1.frame import Method
from mtk.amqp_0_9_1.table import FieldTable

from SecureOk import SecureOk

class Secure(Method):
    """

        The SASL protocol works by exchanging challenges and responses until both peers have
        received sufficient information to authenticate each other. This method challenges
        the client to provide more information.
      
    """

    SYNCHRONOUS = True

    RESPONSE = []
    RESPONSE.append(SecureOk)

    def __init__(self, channel=0):
        Method.__init__(self,10,20,channel)

        # 
        # Challenge information, a block of opaque binary data passed to the security
        # mechanism.
        # 
        self.challenge = ""    # longstr


    def __str__(self, indent=""):
        mstr = indent + "Connection.Secure:\n"
        mstr += indent + "    challenge: " + str(self.challenge) + "\n"
        return mstr


    def payloadSize(self):
        l = 4    # class-id (short), method-id (short)

        # challenge
        l += 4 + len(self.challenge)    # long string

        return l

    def packPayload(self, buffer):
        struct.pack_into("!HH",buffer,7,self._class_id,self._method_id)
        offset = 7 + 4

        struct.pack_into("!I",buffer,offset,len(self.challenge))
        offset += 4
        struct.pack_into("!%ds" % len(self.challenge),buffer,offset,self.challenge)
        offset += len(self.challenge)

        return offset

    @staticmethod
    def unpackPayload(channel, buffer):
        method = Secure(channel)

        offset = 4    # class_id and method_id are already known

        (strlen,) = struct.unpack_from("!I",buffer,offset)
        offset += 4
        (method.challenge,) = struct.unpack_from("!%ds" % strlen,buffer,offset)
        offset += strlen

        return method
