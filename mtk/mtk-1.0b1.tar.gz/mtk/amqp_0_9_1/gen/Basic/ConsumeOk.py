

import struct

from mtk.amqp_0_9_1.frame import Method
from mtk.amqp_0_9_1.table import FieldTable


class ConsumeOk(Method):
    """

        The server provides the client with a consumer tag, which is used by the client
        for methods called on the consumer at a later stage.
      
    """

    SYNCHRONOUS = True

    RESPONSE = []

    def __init__(self, channel=0):
        Method.__init__(self,60,21,channel)

        # 
        # Holds the consumer tag specified by the client or provided by the server.
        # 
        self.consumer_tag = ""    # shortstr


    def __str__(self, indent=""):
        mstr = indent + "Basic.ConsumeOk:\n"
        mstr += indent + "    consumer_tag: " + str(self.consumer_tag) + "\n"
        return mstr


    def payloadSize(self):
        l = 4    # class-id (short), method-id (short)

        # consumer_tag
        l += 1 + len(self.consumer_tag)    # short string

        return l

    def packPayload(self, buffer):
        struct.pack_into("!HH",buffer,7,self._class_id,self._method_id)
        offset = 7 + 4

        struct.pack_into("!B",buffer,offset,len(self.consumer_tag))
        offset += 1
        struct.pack_into("!%ds" % len(self.consumer_tag),buffer,offset,self.consumer_tag)
        offset += len(self.consumer_tag)

        return offset

    @staticmethod
    def unpackPayload(channel, buffer):
        method = ConsumeOk(channel)

        offset = 4    # class_id and method_id are already known

        (strlen,) = struct.unpack_from("!B",buffer,offset)
        offset += 1
        (method.consumer_tag,) = struct.unpack_from("!%ds" % strlen,buffer,offset)
        offset += strlen

        return method
