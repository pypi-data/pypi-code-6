

import struct

from mtk.amqp_0_9_1.frame import Method
from mtk.amqp_0_9_1.table import FieldTable

from QosOk import QosOk

class Qos(Method):
    """

        This method requests a specific quality of service. The QoS can be specified for the
        current channel or for all channels on the connection. The particular properties and
        semantics of a qos method always depend on the content class semantics. Though the
        qos method could in principle apply to both peers, it is currently meaningful only
        for the server.
      
    """

    SYNCHRONOUS = True

    RESPONSE = []
    RESPONSE.append(QosOk)

    def __init__(self, channel=0):
        Method.__init__(self,60,10,channel)

        # 
        # The client can request that messages be sent in advance so that when the client
        # finishes processing a message, the following message is already held locally,
        # rather than needing to be sent down the channel. Prefetching gives a performance
        # improvement. This field specifies the prefetch window size in octets. The server
        # will send a message in advance if it is equal to or smaller in size than the
        # available prefetch size (and also falls into other prefetch limits). May be set
        # to zero, meaning "no specific limit", although other prefetch limits may still
        # apply. The prefetch-size is ignored if the no-ack option is set.
        # 
        self.prefetch_size = 0    # long

        # 
        # Specifies a prefetch window in terms of whole messages. This field may be used
        # in combination with the prefetch-size field; a message will only be sent in
        # advance if both prefetch windows (and those at the channel and connection level)
        # allow it. The prefetch-count is ignored if the no-ack option is set.
        # 
        self.prefetch_count = 0    # short

        # 
        # By default the QoS settings apply to the current channel only. If this field is
        # set, they are applied to the entire connection.
        # 
        self._global = 0    # bit


    def __str__(self, indent=""):
        mstr = indent + "Basic.Qos:\n"
        mstr += indent + "    prefetch_size: " + str(self.prefetch_size) + "\n"
        mstr += indent + "    prefetch_count: " + str(self.prefetch_count) + "\n"
        mstr += indent + "    _global: " + str(self._global) + "\n"
        return mstr


    def payloadSize(self):
        l = 4    # class-id (short), method-id (short)

        # prefetch_size
        l += 4    # 32-bit integer

        # prefetch_count
        l += 2    # 16-bit integer

        # _global
        l += 1    # one to eight bits

        return l

    def packPayload(self, buffer):
        struct.pack_into("!HH",buffer,7,self._class_id,self._method_id)
        offset = 7 + 4

        struct.pack_into("!I",buffer,offset,self.prefetch_size)
        offset += 4

        struct.pack_into("!H",buffer,offset,self.prefetch_count)
        offset += 2

        byte = 0
        if self._global > 0:
            byte = byte | 1 << 0
        struct.pack_into("!B",buffer,offset,byte)
        offset += 1

        return offset

    @staticmethod
    def unpackPayload(channel, buffer):
        method = Qos(channel)

        offset = 4    # class_id and method_id are already known

        (method.prefetch_size,) = struct.unpack_from("!I",buffer,offset)
        offset += 4

        (method.prefetch_count,) = struct.unpack_from("!H",buffer,offset)
        offset += 2

        (byte,) = struct.unpack_from("!B",buffer,offset)
        if byte & 1 << 0 > 0:
            method._global = 1
        else:
            method._global = 0
        offset += 1

        return method
