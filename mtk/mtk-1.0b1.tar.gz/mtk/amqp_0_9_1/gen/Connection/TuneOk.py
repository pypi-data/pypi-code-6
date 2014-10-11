

import struct

from mtk.amqp_0_9_1.frame import Method
from mtk.amqp_0_9_1.table import FieldTable


class TuneOk(Method):
    """

        This method sends the client's connection tuning parameters to the server.
        Certain fields are negotiated, others provide capability information.
      
    """

    SYNCHRONOUS = True

    RESPONSE = []

    def __init__(self, channel=0):
        Method.__init__(self,10,31,channel)

        # 
        # The maximum total number of channels that the client will use per connection.
        # 
        self.channel_max = 0    # short

        # 
        # The largest frame size that the client and server will use for the connection.
        # Zero means that the client does not impose any specific limit but may reject
        # very large frames if it cannot allocate resources for them. Note that the
        # frame-max limit applies principally to content frames, where large contents can
        # be broken into frames of arbitrary size.
        # 
        self.frame_max = 0    # long

        # 
        # The delay, in seconds, of the connection heartbeat that the client wants. Zero
        # means the client does not want a heartbeat.
        # 
        self.heartbeat = 0    # short


    def __str__(self, indent=""):
        mstr = indent + "Connection.TuneOk:\n"
        mstr += indent + "    channel_max: " + str(self.channel_max) + "\n"
        mstr += indent + "    frame_max: " + str(self.frame_max) + "\n"
        mstr += indent + "    heartbeat: " + str(self.heartbeat) + "\n"
        return mstr


    def payloadSize(self):
        l = 4    # class-id (short), method-id (short)

        # channel_max
        l += 2    # 16-bit integer

        # frame_max
        l += 4    # 32-bit integer

        # heartbeat
        l += 2    # 16-bit integer

        return l

    def packPayload(self, buffer):
        struct.pack_into("!HH",buffer,7,self._class_id,self._method_id)
        offset = 7 + 4

        struct.pack_into("!H",buffer,offset,self.channel_max)
        offset += 2

        struct.pack_into("!I",buffer,offset,self.frame_max)
        offset += 4

        struct.pack_into("!H",buffer,offset,self.heartbeat)
        offset += 2

        return offset

    @staticmethod
    def unpackPayload(channel, buffer):
        method = TuneOk(channel)

        offset = 4    # class_id and method_id are already known

        (method.channel_max,) = struct.unpack_from("!H",buffer,offset)
        offset += 2

        (method.frame_max,) = struct.unpack_from("!I",buffer,offset)
        offset += 4

        (method.heartbeat,) = struct.unpack_from("!H",buffer,offset)
        offset += 2

        return method
