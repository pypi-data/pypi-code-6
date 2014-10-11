

import struct

from mtk.amqp_0_9_1.frame import Method
from mtk.amqp_0_9_1.table import FieldTable

from CloseOk import CloseOk

class Close(Method):
    """

        This method indicates that the sender wants to close the connection. This may be
        due to internal conditions (e.g. a forced shut-down) or due to an error handling
        a specific method, i.e. an exception. When a close is due to an exception, the
        sender provides the class and method id of the method which caused the exception.
      
    """

    SYNCHRONOUS = True

    RESPONSE = []
    RESPONSE.append(CloseOk)

    def __init__(self, channel=0):
        Method.__init__(self,10,50,channel)

        self.reply_code = 0    # short

        self.reply_text = ""    # shortstr

        # 
        # When the close is provoked by a method exception, this is the class of the
        # method.
        # 
        self.class_id = 0    # short

        # 
        # When the close is provoked by a method exception, this is the ID of the method.
        # 
        self.method_id = 0    # short


    def __str__(self, indent=""):
        mstr = indent + "Connection.Close:\n"
        mstr += indent + "    reply_code: " + str(self.reply_code) + "\n"
        mstr += indent + "    reply_text: " + str(self.reply_text) + "\n"
        mstr += indent + "    class_id: " + str(self.class_id) + "\n"
        mstr += indent + "    method_id: " + str(self.method_id) + "\n"
        return mstr


    def payloadSize(self):
        l = 4    # class-id (short), method-id (short)

        # reply_code
        l += 2    # 16-bit integer

        # reply_text
        l += 1 + len(self.reply_text)    # short string

        # class_id
        l += 2    # 16-bit integer

        # method_id
        l += 2    # 16-bit integer

        return l

    def packPayload(self, buffer):
        struct.pack_into("!HH",buffer,7,self._class_id,self._method_id)
        offset = 7 + 4

        struct.pack_into("!H",buffer,offset,self.reply_code)
        offset += 2

        struct.pack_into("!B",buffer,offset,len(self.reply_text))
        offset += 1
        struct.pack_into("!%ds" % len(self.reply_text),buffer,offset,self.reply_text)
        offset += len(self.reply_text)

        struct.pack_into("!H",buffer,offset,self.class_id)
        offset += 2

        struct.pack_into("!H",buffer,offset,self.method_id)
        offset += 2

        return offset

    @staticmethod
    def unpackPayload(channel, buffer):
        method = Close(channel)

        offset = 4    # class_id and method_id are already known

        (method.reply_code,) = struct.unpack_from("!H",buffer,offset)
        offset += 2

        (strlen,) = struct.unpack_from("!B",buffer,offset)
        offset += 1
        (method.reply_text,) = struct.unpack_from("!%ds" % strlen,buffer,offset)
        offset += strlen

        (method.class_id,) = struct.unpack_from("!H",buffer,offset)
        offset += 2

        (method.method_id,) = struct.unpack_from("!H",buffer,offset)
        offset += 2

        return method
