

import struct

from mtk.amqp_0_9_1.frame import Method
from mtk.amqp_0_9_1.table import FieldTable

from StartOk import StartOk

class Start(Method):
    """

        This method starts the connection negotiation process by telling the client the
        protocol version that the server proposes, along with a list of security mechanisms
        which the client can use for authentication.
      
    """

    SYNCHRONOUS = True

    RESPONSE = []
    RESPONSE.append(StartOk)

    def __init__(self, channel=0):
        Method.__init__(self,10,10,channel)

        # 
        # The major version number can take any value from 0 to 99 as defined in the
        # AMQP specification.
        # 
        self.version_major = 0    # octet

        # 
        # The minor version number can take any value from 0 to 99 as defined in the
        # AMQP specification.
        # 
        self.version_minor = 0    # octet

        self.server_properties = FieldTable()    # table

        # 
        # A list of the security mechanisms that the server supports, delimited by spaces.
        # 
        self.mechanisms = ""    # longstr

        # 
        # A list of the message locales that the server supports, delimited by spaces. The
        # locale defines the language in which the server will send reply texts.
        # 
        self.locales = ""    # longstr


    def __str__(self, indent=""):
        mstr = indent + "Connection.Start:\n"
        mstr += indent + "    version_major: " + str(self.version_major) + "\n"
        mstr += indent + "    version_minor: " + str(self.version_minor) + "\n"
        mstr += indent + "    server_properties:\n"
        mstr += self.server_properties.__str__(indent+"        ")
        mstr += indent + "    mechanisms: " + str(self.mechanisms) + "\n"
        mstr += indent + "    locales: " + str(self.locales) + "\n"
        return mstr


    def payloadSize(self):
        l = 4    # class-id (short), method-id (short)

        # version_major
        l += 1    # octet

        # version_minor
        l += 1    # octet

        # server_properties
        l += self.server_properties.length()

        # mechanisms
        l += 4 + len(self.mechanisms)    # long string

        # locales
        l += 4 + len(self.locales)    # long string

        return l

    def packPayload(self, buffer):
        struct.pack_into("!HH",buffer,7,self._class_id,self._method_id)
        offset = 7 + 4

        struct.pack_into("!B",buffer,offset,self.version_major)
        offset += 1

        struct.pack_into("!B",buffer,offset,self.version_minor)
        offset += 1

        offset = self.server_properties.pack(buffer,offset)

        struct.pack_into("!I",buffer,offset,len(self.mechanisms))
        offset += 4
        struct.pack_into("!%ds" % len(self.mechanisms),buffer,offset,self.mechanisms)
        offset += len(self.mechanisms)

        struct.pack_into("!I",buffer,offset,len(self.locales))
        offset += 4
        struct.pack_into("!%ds" % len(self.locales),buffer,offset,self.locales)
        offset += len(self.locales)

        return offset

    @staticmethod
    def unpackPayload(channel, buffer):
        method = Start(channel)

        offset = 4    # class_id and method_id are already known

        (method.version_major,) = struct.unpack_from("!B",buffer,offset)
        offset += 1

        (method.version_minor,) = struct.unpack_from("!B",buffer,offset)
        offset += 1

        method.server_properties = FieldTable()
        offset = method.server_properties.unpack(buffer,offset)

        (strlen,) = struct.unpack_from("!I",buffer,offset)
        offset += 4
        (method.mechanisms,) = struct.unpack_from("!%ds" % strlen,buffer,offset)
        offset += strlen

        (strlen,) = struct.unpack_from("!I",buffer,offset)
        offset += 4
        (method.locales,) = struct.unpack_from("!%ds" % strlen,buffer,offset)
        offset += strlen

        return method
