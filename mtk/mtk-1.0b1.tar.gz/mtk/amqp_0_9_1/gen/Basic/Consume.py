

import struct

from mtk.amqp_0_9_1.frame import Method
from mtk.amqp_0_9_1.table import FieldTable

from ConsumeOk import ConsumeOk

class Consume(Method):
    """

        This method asks the server to start a "consumer", which is a transient request for
        messages from a specific queue. Consumers last as long as the channel they were
        declared on, or until the client cancels them.
      
    """

    SYNCHRONOUS = True

    RESPONSE = []
    RESPONSE.append(ConsumeOk)

    def __init__(self, channel=0):
        Method.__init__(self,60,20,channel)

        self.reserved_1 = 0    # short

        # Specifies the name of the queue to consume from.
        self.queue = ""    # shortstr

        # 
        # Specifies the identifier for the consumer. The consumer tag is local to a
        # channel, so two clients can use the same consumer tags. If this field is
        # empty the server will generate a unique tag.
        # 
        self.consumer_tag = ""    # shortstr

        self.no_local = 0    # bit

        self.no_ack = 0    # bit

        # 
        # Request exclusive consumer access, meaning only this consumer can access the
        # queue.
        # 
        self.exclusive = 0    # bit

        self.no_wait = 0    # bit

        # 
        # A set of arguments for the consume. The syntax and semantics of these
        # arguments depends on the server implementation.
        # 
        self.arguments = FieldTable()    # table


    def __str__(self, indent=""):
        mstr = indent + "Basic.Consume:\n"
        mstr += indent + "    reserved_1: " + str(self.reserved_1) + "\n"
        mstr += indent + "    queue: " + str(self.queue) + "\n"
        mstr += indent + "    consumer_tag: " + str(self.consumer_tag) + "\n"
        mstr += indent + "    no_local: " + str(self.no_local) + "\n"
        mstr += indent + "    no_ack: " + str(self.no_ack) + "\n"
        mstr += indent + "    exclusive: " + str(self.exclusive) + "\n"
        mstr += indent + "    no_wait: " + str(self.no_wait) + "\n"
        mstr += indent + "    arguments:\n"
        mstr += self.arguments.__str__(indent+"        ")
        return mstr


    def payloadSize(self):
        l = 4    # class-id (short), method-id (short)

        # reserved_1
        l += 2    # 16-bit integer

        # queue
        l += 1 + len(self.queue)    # short string

        # consumer_tag
        l += 1 + len(self.consumer_tag)    # short string

        # no_local

        # no_ack

        # exclusive

        # no_wait
        l += 1    # one to eight bits

        # arguments
        l += self.arguments.length()

        return l

    def packPayload(self, buffer):
        struct.pack_into("!HH",buffer,7,self._class_id,self._method_id)
        offset = 7 + 4

        struct.pack_into("!H",buffer,offset,self.reserved_1)
        offset += 2

        struct.pack_into("!B",buffer,offset,len(self.queue))
        offset += 1
        struct.pack_into("!%ds" % len(self.queue),buffer,offset,self.queue)
        offset += len(self.queue)

        struct.pack_into("!B",buffer,offset,len(self.consumer_tag))
        offset += 1
        struct.pack_into("!%ds" % len(self.consumer_tag),buffer,offset,self.consumer_tag)
        offset += len(self.consumer_tag)

        byte = 0
        if self.no_local > 0:
            byte = byte | 1 << 0

        if self.no_ack > 0:
            byte = byte | 1 << 1

        if self.exclusive > 0:
            byte = byte | 1 << 2

        if self.no_wait > 0:
            byte = byte | 1 << 3
        struct.pack_into("!B",buffer,offset,byte)
        offset += 1

        offset = self.arguments.pack(buffer,offset)

        return offset

    @staticmethod
    def unpackPayload(channel, buffer):
        method = Consume(channel)

        offset = 4    # class_id and method_id are already known

        (method.reserved_1,) = struct.unpack_from("!H",buffer,offset)
        offset += 2

        (strlen,) = struct.unpack_from("!B",buffer,offset)
        offset += 1
        (method.queue,) = struct.unpack_from("!%ds" % strlen,buffer,offset)
        offset += strlen

        (strlen,) = struct.unpack_from("!B",buffer,offset)
        offset += 1
        (method.consumer_tag,) = struct.unpack_from("!%ds" % strlen,buffer,offset)
        offset += strlen

        (byte,) = struct.unpack_from("!B",buffer,offset)
        if byte & 1 << 0 > 0:
            method.no_local = 1
        else:
            method.no_local = 0

        (byte,) = struct.unpack_from("!B",buffer,offset)
        if byte & 1 << 1 > 0:
            method.no_ack = 1
        else:
            method.no_ack = 0

        (byte,) = struct.unpack_from("!B",buffer,offset)
        if byte & 1 << 2 > 0:
            method.exclusive = 1
        else:
            method.exclusive = 0

        (byte,) = struct.unpack_from("!B",buffer,offset)
        if byte & 1 << 3 > 0:
            method.no_wait = 1
        else:
            method.no_wait = 0
        offset += 1

        method.arguments = FieldTable()
        offset = method.arguments.unpack(buffer,offset)

        return method
