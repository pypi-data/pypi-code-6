

import struct

from mtk.amqp_0_9_1.frame import Method
from mtk.amqp_0_9_1.table import FieldTable

from DeleteOk import DeleteOk

class Delete(Method):
    """

        This method deletes a queue. When a queue is deleted any pending messages are sent
        to a dead-letter queue if this is defined in the server configuration, and all
        consumers on the queue are cancelled.
      
    """

    SYNCHRONOUS = True

    RESPONSE = []
    RESPONSE.append(DeleteOk)

    def __init__(self, channel=0):
        Method.__init__(self,50,40,channel)

        self.reserved_1 = 0    # short

        # Specifies the name of the queue to delete.
        self.queue = ""    # shortstr

        # 
        # If set, the server will only delete the queue if it has no consumers. If the
        # queue has consumers the server does does not delete it but raises a channel
        # exception instead.
        # 
        self.if_unused = 0    # bit

        # 
        # If set, the server will only delete the queue if it has no messages.
        # 
        self.if_empty = 0    # bit

        self.no_wait = 0    # bit


    def __str__(self, indent=""):
        mstr = indent + "Queue.Delete:\n"
        mstr += indent + "    reserved_1: " + str(self.reserved_1) + "\n"
        mstr += indent + "    queue: " + str(self.queue) + "\n"
        mstr += indent + "    if_unused: " + str(self.if_unused) + "\n"
        mstr += indent + "    if_empty: " + str(self.if_empty) + "\n"
        mstr += indent + "    no_wait: " + str(self.no_wait) + "\n"
        return mstr


    def payloadSize(self):
        l = 4    # class-id (short), method-id (short)

        # reserved_1
        l += 2    # 16-bit integer

        # queue
        l += 1 + len(self.queue)    # short string

        # if_unused

        # if_empty

        # no_wait
        l += 1    # one to eight bits

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

        byte = 0
        if self.if_unused > 0:
            byte = byte | 1 << 0

        if self.if_empty > 0:
            byte = byte | 1 << 1

        if self.no_wait > 0:
            byte = byte | 1 << 2
        struct.pack_into("!B",buffer,offset,byte)
        offset += 1

        return offset

    @staticmethod
    def unpackPayload(channel, buffer):
        method = Delete(channel)

        offset = 4    # class_id and method_id are already known

        (method.reserved_1,) = struct.unpack_from("!H",buffer,offset)
        offset += 2

        (strlen,) = struct.unpack_from("!B",buffer,offset)
        offset += 1
        (method.queue,) = struct.unpack_from("!%ds" % strlen,buffer,offset)
        offset += strlen

        (byte,) = struct.unpack_from("!B",buffer,offset)
        if byte & 1 << 0 > 0:
            method.if_unused = 1
        else:
            method.if_unused = 0

        (byte,) = struct.unpack_from("!B",buffer,offset)
        if byte & 1 << 1 > 0:
            method.if_empty = 1
        else:
            method.if_empty = 0

        (byte,) = struct.unpack_from("!B",buffer,offset)
        if byte & 1 << 2 > 0:
            method.no_wait = 1
        else:
            method.no_wait = 0
        offset += 1

        return method
