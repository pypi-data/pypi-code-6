

import struct

from mtk.amqp_0_9_1.frame import Method
from mtk.amqp_0_9_1.table import FieldTable

from CancelOk import CancelOk

class Cancel(Method):
    """

        This method cancels a consumer. This does not affect already delivered
        messages, but it does mean the server will not send any more messages for
        that consumer. The client may receive an arbitrary number of messages in
        between sending the cancel method and receiving the cancel-ok reply.
      
    """

    SYNCHRONOUS = True

    RESPONSE = []
    RESPONSE.append(CancelOk)

    def __init__(self, channel=0):
        Method.__init__(self,60,30,channel)

        self.consumer_tag = ""    # shortstr

        self.no_wait = 0    # bit


    def __str__(self, indent=""):
        mstr = indent + "Basic.Cancel:\n"
        mstr += indent + "    consumer_tag: " + str(self.consumer_tag) + "\n"
        mstr += indent + "    no_wait: " + str(self.no_wait) + "\n"
        return mstr


    def payloadSize(self):
        l = 4    # class-id (short), method-id (short)

        # consumer_tag
        l += 1 + len(self.consumer_tag)    # short string

        # no_wait
        l += 1    # one to eight bits

        return l

    def packPayload(self, buffer):
        struct.pack_into("!HH",buffer,7,self._class_id,self._method_id)
        offset = 7 + 4

        struct.pack_into("!B",buffer,offset,len(self.consumer_tag))
        offset += 1
        struct.pack_into("!%ds" % len(self.consumer_tag),buffer,offset,self.consumer_tag)
        offset += len(self.consumer_tag)

        byte = 0
        if self.no_wait > 0:
            byte = byte | 1 << 0
        struct.pack_into("!B",buffer,offset,byte)
        offset += 1

        return offset

    @staticmethod
    def unpackPayload(channel, buffer):
        method = Cancel(channel)

        offset = 4    # class_id and method_id are already known

        (strlen,) = struct.unpack_from("!B",buffer,offset)
        offset += 1
        (method.consumer_tag,) = struct.unpack_from("!%ds" % strlen,buffer,offset)
        offset += strlen

        (byte,) = struct.unpack_from("!B",buffer,offset)
        if byte & 1 << 0 > 0:
            method.no_wait = 1
        else:
            method.no_wait = 0
        offset += 1

        return method
