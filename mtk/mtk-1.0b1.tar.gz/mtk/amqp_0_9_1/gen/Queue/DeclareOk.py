

import struct

from mtk.amqp_0_9_1.frame import Method
from mtk.amqp_0_9_1.table import FieldTable


class DeclareOk(Method):
    """

        This method confirms a Declare method and confirms the name of the queue, essential
        for automatically-named queues.
      
    """

    SYNCHRONOUS = True

    RESPONSE = []

    def __init__(self, channel=0):
        Method.__init__(self,50,11,channel)

        # 
        # Reports the name of the queue. If the server generated a queue name, this field
        # contains that name.
        # 
        self.queue = ""    # shortstr

        self.message_count = 0    # long

        # 
        # Reports the number of active consumers for the queue. Note that consumers can
        # suspend activity (Channel.Flow) in which case they do not appear in this count.
        # 
        self.consumer_count = 0    # long


    def __str__(self, indent=""):
        mstr = indent + "Queue.DeclareOk:\n"
        mstr += indent + "    queue: " + str(self.queue) + "\n"
        mstr += indent + "    message_count: " + str(self.message_count) + "\n"
        mstr += indent + "    consumer_count: " + str(self.consumer_count) + "\n"
        return mstr


    def payloadSize(self):
        l = 4    # class-id (short), method-id (short)

        # queue
        l += 1 + len(self.queue)    # short string

        # message_count
        l += 4    # 32-bit integer

        # consumer_count
        l += 4    # 32-bit integer

        return l

    def packPayload(self, buffer):
        struct.pack_into("!HH",buffer,7,self._class_id,self._method_id)
        offset = 7 + 4

        struct.pack_into("!B",buffer,offset,len(self.queue))
        offset += 1
        struct.pack_into("!%ds" % len(self.queue),buffer,offset,self.queue)
        offset += len(self.queue)

        struct.pack_into("!I",buffer,offset,self.message_count)
        offset += 4

        struct.pack_into("!I",buffer,offset,self.consumer_count)
        offset += 4

        return offset

    @staticmethod
    def unpackPayload(channel, buffer):
        method = DeclareOk(channel)

        offset = 4    # class_id and method_id are already known

        (strlen,) = struct.unpack_from("!B",buffer,offset)
        offset += 1
        (method.queue,) = struct.unpack_from("!%ds" % strlen,buffer,offset)
        offset += strlen

        (method.message_count,) = struct.unpack_from("!I",buffer,offset)
        offset += 4

        (method.consumer_count,) = struct.unpack_from("!I",buffer,offset)
        offset += 4

        return method
