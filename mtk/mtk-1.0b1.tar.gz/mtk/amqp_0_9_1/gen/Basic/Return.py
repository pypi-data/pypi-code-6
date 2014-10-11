

import struct

from mtk.amqp_0_9_1.frame import Method
from mtk.amqp_0_9_1.table import FieldTable


class Return(Method):
    """

        This method returns an undeliverable message that was published with the "immediate"
        flag set, or an unroutable message published with the "mandatory" flag set. The
        reply code and text provide information about the reason that the message was
        undeliverable.
      
    """

    SYNCHRONOUS = False

    RESPONSE = []

    def __init__(self, channel=0):
        Method.__init__(self,60,50,channel)

        self.reply_code = 0    # short

        self.reply_text = ""    # shortstr

        # 
        # Specifies the name of the exchange that the message was originally published
        # to.  May be empty, meaning the default exchange.
        # 
        self.exchange = ""    # shortstr

        # 
        # Specifies the routing key name specified when the message was published.
        # 
        self.routing_key = ""    # shortstr


    def __str__(self, indent=""):
        mstr = indent + "Basic.Return:\n"
        mstr += indent + "    reply_code: " + str(self.reply_code) + "\n"
        mstr += indent + "    reply_text: " + str(self.reply_text) + "\n"
        mstr += indent + "    exchange: " + str(self.exchange) + "\n"
        mstr += indent + "    routing_key: " + str(self.routing_key) + "\n"
        return mstr


    def payloadSize(self):
        l = 4    # class-id (short), method-id (short)

        # reply_code
        l += 2    # 16-bit integer

        # reply_text
        l += 1 + len(self.reply_text)    # short string

        # exchange
        l += 1 + len(self.exchange)    # short string

        # routing_key
        l += 1 + len(self.routing_key)    # short string

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

        struct.pack_into("!B",buffer,offset,len(self.exchange))
        offset += 1
        struct.pack_into("!%ds" % len(self.exchange),buffer,offset,self.exchange)
        offset += len(self.exchange)

        struct.pack_into("!B",buffer,offset,len(self.routing_key))
        offset += 1
        struct.pack_into("!%ds" % len(self.routing_key),buffer,offset,self.routing_key)
        offset += len(self.routing_key)

        return offset

    @staticmethod
    def unpackPayload(channel, buffer):
        method = Return(channel)

        offset = 4    # class_id and method_id are already known

        (method.reply_code,) = struct.unpack_from("!H",buffer,offset)
        offset += 2

        (strlen,) = struct.unpack_from("!B",buffer,offset)
        offset += 1
        (method.reply_text,) = struct.unpack_from("!%ds" % strlen,buffer,offset)
        offset += strlen

        (strlen,) = struct.unpack_from("!B",buffer,offset)
        offset += 1
        (method.exchange,) = struct.unpack_from("!%ds" % strlen,buffer,offset)
        offset += strlen

        (strlen,) = struct.unpack_from("!B",buffer,offset)
        offset += 1
        (method.routing_key,) = struct.unpack_from("!%ds" % strlen,buffer,offset)
        offset += strlen

        return method
