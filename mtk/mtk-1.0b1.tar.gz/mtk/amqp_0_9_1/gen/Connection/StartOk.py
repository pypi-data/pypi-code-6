

import struct

from mtk.amqp_0_9_1.frame import Method
from mtk.amqp_0_9_1.table import FieldTable


class StartOk(Method):
    """

        This method selects a SASL security mechanism.
      
    """

    SYNCHRONOUS = True

    RESPONSE = []

    def __init__(self, channel=0):
        Method.__init__(self,10,11,channel)

        self.client_properties = FieldTable()    # table

        # 
        # A single security mechanisms selected by the client, which must be one of those
        # specified by the server.
        # 
        self.mechanism = ""    # shortstr

        # 
        # A block of opaque data passed to the security mechanism. The contents of this
        # data are defined by the SASL security mechanism.
        # 
        self.response = ""    # longstr

        # 
        # A single message locale selected by the client, which must be one of those
        # specified by the server.
        # 
        self.locale = ""    # shortstr


    def __str__(self, indent=""):
        mstr = indent + "Connection.StartOk:\n"
        mstr += indent + "    client_properties:\n"
        mstr += self.client_properties.__str__(indent+"        ")
        mstr += indent + "    mechanism: " + str(self.mechanism) + "\n"
        mstr += indent + "    response: " + str(self.response) + "\n"
        mstr += indent + "    locale: " + str(self.locale) + "\n"
        return mstr


    def payloadSize(self):
        l = 4    # class-id (short), method-id (short)

        # client_properties
        l += self.client_properties.length()

        # mechanism
        l += 1 + len(self.mechanism)    # short string

        # response
        l += 4 + len(self.response)    # long string

        # locale
        l += 1 + len(self.locale)    # short string

        return l

    def packPayload(self, buffer):
        struct.pack_into("!HH",buffer,7,self._class_id,self._method_id)
        offset = 7 + 4

        offset = self.client_properties.pack(buffer,offset)

        struct.pack_into("!B",buffer,offset,len(self.mechanism))
        offset += 1
        struct.pack_into("!%ds" % len(self.mechanism),buffer,offset,self.mechanism)
        offset += len(self.mechanism)

        struct.pack_into("!I",buffer,offset,len(self.response))
        offset += 4
        struct.pack_into("!%ds" % len(self.response),buffer,offset,self.response)
        offset += len(self.response)

        struct.pack_into("!B",buffer,offset,len(self.locale))
        offset += 1
        struct.pack_into("!%ds" % len(self.locale),buffer,offset,self.locale)
        offset += len(self.locale)

        return offset

    @staticmethod
    def unpackPayload(channel, buffer):
        method = StartOk(channel)

        offset = 4    # class_id and method_id are already known

        method.client_properties = FieldTable()
        offset = method.client_properties.unpack(buffer,offset)

        (strlen,) = struct.unpack_from("!B",buffer,offset)
        offset += 1
        (method.mechanism,) = struct.unpack_from("!%ds" % strlen,buffer,offset)
        offset += strlen

        (strlen,) = struct.unpack_from("!I",buffer,offset)
        offset += 4
        (method.response,) = struct.unpack_from("!%ds" % strlen,buffer,offset)
        offset += strlen

        (strlen,) = struct.unpack_from("!B",buffer,offset)
        offset += 1
        (method.locale,) = struct.unpack_from("!%ds" % strlen,buffer,offset)
        offset += strlen

        return method
