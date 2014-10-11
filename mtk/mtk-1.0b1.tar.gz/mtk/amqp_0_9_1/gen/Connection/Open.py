

import struct

from mtk.amqp_0_9_1.frame import Method
from mtk.amqp_0_9_1.table import FieldTable

from OpenOk import OpenOk

class Open(Method):
    """

        This method opens a connection to a virtual host, which is a collection of
        resources, and acts to separate multiple application domains within a server.
        The server may apply arbitrary limits per virtual host, such as the number
        of each type of entity that may be used, per connection and/or in total.
      
    """

    SYNCHRONOUS = True

    RESPONSE = []
    RESPONSE.append(OpenOk)

    def __init__(self, channel=0):
        Method.__init__(self,10,40,channel)

        # 
        # The name of the virtual host to work with.
        # 
        self.virtual_host = ""    # shortstr

        self.reserved_1 = ""    # shortstr

        self.reserved_2 = 0    # bit


    def __str__(self, indent=""):
        mstr = indent + "Connection.Open:\n"
        mstr += indent + "    virtual_host: " + str(self.virtual_host) + "\n"
        mstr += indent + "    reserved_1: " + str(self.reserved_1) + "\n"
        mstr += indent + "    reserved_2: " + str(self.reserved_2) + "\n"
        return mstr


    def payloadSize(self):
        l = 4    # class-id (short), method-id (short)

        # virtual_host
        l += 1 + len(self.virtual_host)    # short string

        # reserved_1
        l += 1 + len(self.reserved_1)    # short string

        # reserved_2
        l += 1    # one to eight bits

        return l

    def packPayload(self, buffer):
        struct.pack_into("!HH",buffer,7,self._class_id,self._method_id)
        offset = 7 + 4

        struct.pack_into("!B",buffer,offset,len(self.virtual_host))
        offset += 1
        struct.pack_into("!%ds" % len(self.virtual_host),buffer,offset,self.virtual_host)
        offset += len(self.virtual_host)

        struct.pack_into("!B",buffer,offset,len(self.reserved_1))
        offset += 1
        struct.pack_into("!%ds" % len(self.reserved_1),buffer,offset,self.reserved_1)
        offset += len(self.reserved_1)

        byte = 0
        if self.reserved_2 > 0:
            byte = byte | 1 << 0
        struct.pack_into("!B",buffer,offset,byte)
        offset += 1

        return offset

    @staticmethod
    def unpackPayload(channel, buffer):
        method = Open(channel)

        offset = 4    # class_id and method_id are already known

        (strlen,) = struct.unpack_from("!B",buffer,offset)
        offset += 1
        (method.virtual_host,) = struct.unpack_from("!%ds" % strlen,buffer,offset)
        offset += strlen

        (strlen,) = struct.unpack_from("!B",buffer,offset)
        offset += 1
        (method.reserved_1,) = struct.unpack_from("!%ds" % strlen,buffer,offset)
        offset += strlen

        (byte,) = struct.unpack_from("!B",buffer,offset)
        if byte & 1 << 0 > 0:
            method.reserved_2 = 1
        else:
            method.reserved_2 = 0
        offset += 1

        return method
