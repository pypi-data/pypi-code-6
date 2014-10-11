
###############################################################################
#   Copyright 2012 Warren Smith                                               #
#                                                                             #
#   Licensed under the Apache License, Version 2.0 (the "License");           #
#   you may not use this file except in compliance with the License.          #
#   You may obtain a copy of the License at                                   #
#                                                                             #
#       http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                             #
#   Unless required by applicable law or agreed to in writing, software       #
#   distributed under the License is distributed on an "AS IS" BASIS,         #
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  #
#   See the License for the specific language governing permissions and       #
#   limitations under the License.                                            #
###############################################################################

import array
import struct

import gen
from gen import constants

#######################################################################################################################

class Frame(object):

    SYNCHRONOUS = False
    RESPONSE = []

    def __init__(self, frame_type, channel):
        self.frame_type = frame_type    # octet
        self.channel = channel          # short

    def isRequest(self):
        if self.SYNCHRONOUS and len(self.RESPONSE) > 0:
            return True
        return False

    def isResponse(self):
        if self.SYNCHRONOUS and len(self.RESPONSE) == 0:
            return True
        return False

    def pack(self):
        size = self.payloadSize()
        arr = array.array('c','\0' * (7+size+1))
        struct.pack_into("!BHI",arr,0,self.frame_type,self.channel,size)
        self.packPayload(arr)
        struct.pack_into("!B",arr,7+size,constants.FRAME_END)
        return arr

    def payloadSize(self):
        raise NotImplementedError("subclasses need to override")

    def packPayload(self, arr):
        # payload starts at byte 7 of the array
        raise NotImplementedError("subclasses need to override")

    @staticmethod
    def unpackPayload(channel, payload):
        # payload starts at byte 0 of the string
        raise NotImplementedError("subclasses need to override")

#######################################################################################################################

class Method(Frame):
    def __init__(self, class_id, method_id, channel):
        Frame.__init__(self,constants.FRAME_METHOD,channel)
        # at least one method has class_id and method_id fields
        self._class_id = class_id    # short
        self._method_id = method_id   # short

    def payloadSize(self):
        raise NotImplementedError("subclasses need to override")

    def packPayload(self, arr):
        raise NotImplementedError("subclasses need to override")

    @staticmethod
    def unpackPayload(channel, str):
        raise NotImplementedError("subclasses need to override")

#######################################################################################################################

class HeartBeat(Frame):
    def __init__(self, channel=0):
        Frame.__init__(self,constants.FRAME_HEARTBEAT,channel)

    def __str__(self, indent=""):
        return indent + "HeartBeat:\n"

    def payloadSize(self):
        return 0

    def packPayload(self, arr):
        pass

    @staticmethod
    def unpackPayload(channel, payload):
        return HeartBeat(channel)

#######################################################################################################################

class Header(Frame):
    def __init__(self, channel, class_id=None, body_size=None):
        Frame.__init__(self,constants.FRAME_HEADER,channel)
        self.class_id = class_id
        self.weight = 0
        self.body_size = body_size
        self.property_flags = []
        self.property_values = []

    def __str__(self, indent=""):
        bstr = indent + "Header\n"
        bstr += ("%s  channel: %d\n" % (indent,self.channel))
        bstr += ("%s  class_id: %d\n" % (indent,self.class_id))
        bstr += ("%s  weight: %d\n" % (indent,self.weight))
        bstr += ("%s  body size: %d\n" % (indent,self.body_size))
        return bstr

    def payloadSize(self):
        # class id, weight, body size, flags, properties
        # assumes no properties to send
        return 2 + 2 + 8 + 2

    def packPayload(self, arr):
        struct.pack_into("!HHQH",arr,7,self.class_id,self.weight,self.body_size,0)

    @staticmethod
    def unpackPayload(channel, str):
        header = Header(channel)

        #print("content header on channel %d" % channel)
        (header.class_id,header.weight,header.body_size) = struct.unpack_from("!HHQ",str,0)
        # ignoring property flags
        #offset = 12
        #(property_flags,) = struct.unpack_from("!H",payload,offset)
        #offset += 2
        #while property_flags & 0x0001:
        #     = struct.unpack_from("!H",payload,offset)
        #    offset += 2

        return header

#######################################################################################################################

class Body(Frame):
    def __init__(self, channel, content):
        Frame.__init__(self,constants.FRAME_BODY,channel)
        self.content = content

    def __str__(self, indent=""):
        bstr = indent + "Body\n"
        bstr += ("%s  channel: %d\n" % (indent,self.channel))
        bstr += ("%s  content: %s\n" % (indent,self.content))
        return bstr

    def payloadSize(self):
        return len(self.content)

    def packPayload(self, arr):
        struct.pack_into("!%ds" % len(self.content),arr,7,self.content)

    @staticmethod
    def unpackPayload(channel, str):
        body = Body(channel,str)
        return body

#######################################################################################################################

class ProtocolHeader(object):

    SYNCHRONOUS = True

    RESPONSE = []
    #RESPONSE.append(ProtocolHeader)  - problems doing it this way (class isn't defined yet)
    #RESPONSE.append(gen.Connection.StartOk)

    def __init__(self):
        self.major = constants.PROTOCOL_MAJOR
        self.minor = constants.PROTOCOL_MINOR
        self.revision = constants.PROTOCOL_REVISION

        # hack
        if len(ProtocolHeader.RESPONSE) == 0:
            ProtocolHeader.RESPONSE.append(ProtocolHeader)
            ProtocolHeader.RESPONSE.append(gen.Connection.Start)

    def isRequest(self):
        return False

    def isResponse(self):
        return False

    def __str__(self):
        return "protocol header: AMQP %d.%d.%d" % (self.major,self.minor,self.revision)

    def pack(self):
        arr = array.array('c','\0' * 8)
        struct.pack_into("!4sBBBB",arr,0,"AMQP",0,self.major,self.minor,self.revision)
        return arr

    def unpack(self, buffer):
        (protocol,zero,self.major,self.minor,self.revision) = struct.unpack("!4sbbbb",buffer)

#######################################################################################################################
