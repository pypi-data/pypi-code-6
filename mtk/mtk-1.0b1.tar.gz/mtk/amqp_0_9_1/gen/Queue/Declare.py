

import struct

from mtk.amqp_0_9_1.frame import Method
from mtk.amqp_0_9_1.table import FieldTable

from DeclareOk import DeclareOk

class Declare(Method):
    """

        This method creates or checks a queue. When creating a new queue the client can
        specify various properties that control the durability of the queue and its
        contents, and the level of sharing for the queue.
      
    """

    SYNCHRONOUS = True

    RESPONSE = []
    RESPONSE.append(DeclareOk)

    def __init__(self, channel=0):
        Method.__init__(self,50,10,channel)

        self.reserved_1 = 0    # short

        self.queue = ""    # shortstr

        # 
        # If set, the server will reply with Declare-Ok if the queue already
        # exists with the same name, and raise an error if not.  The client can
        # use this to check whether a queue exists without modifying the
        # server state.  When set, all other method fields except name and no-wait
        # are ignored.  A declare with both passive and no-wait has no effect.
        # Arguments are compared for semantic equivalence.
        # 
        self.passive = 0    # bit

        # 
        # If set when creating a new queue, the queue will be marked as durable. Durable
        # queues remain active when a server restarts. Non-durable queues (transient
        # queues) are purged if/when a server restarts. Note that durable queues do not
        # necessarily hold persistent messages, although it does not make sense to send
        # persistent messages to a transient queue.
        # 
        self.durable = 0    # bit

        # 
        # Exclusive queues may only be accessed by the current connection, and are
        # deleted when that connection closes.  Passive declaration of an exclusive
        # queue by other connections are not allowed.
        # 
        self.exclusive = 0    # bit

        # 
        # If set, the queue is deleted when all consumers have finished using it.  The last
        # consumer can be cancelled either explicitly or because its channel is closed. If
        # there was no consumer ever on the queue, it won't be deleted.  Applications can
        # explicitly delete auto-delete queues using the Delete method as normal.
        # 
        self.auto_delete = 0    # bit

        self.no_wait = 0    # bit

        # 
        # A set of arguments for the declaration. The syntax and semantics of these
        # arguments depends on the server implementation.
        # 
        self.arguments = FieldTable()    # table


    def __str__(self, indent=""):
        mstr = indent + "Queue.Declare:\n"
        mstr += indent + "    reserved_1: " + str(self.reserved_1) + "\n"
        mstr += indent + "    queue: " + str(self.queue) + "\n"
        mstr += indent + "    passive: " + str(self.passive) + "\n"
        mstr += indent + "    durable: " + str(self.durable) + "\n"
        mstr += indent + "    exclusive: " + str(self.exclusive) + "\n"
        mstr += indent + "    auto_delete: " + str(self.auto_delete) + "\n"
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

        # passive

        # durable

        # exclusive

        # auto_delete

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

        byte = 0
        if self.passive > 0:
            byte = byte | 1 << 0

        if self.durable > 0:
            byte = byte | 1 << 1

        if self.exclusive > 0:
            byte = byte | 1 << 2

        if self.auto_delete > 0:
            byte = byte | 1 << 3

        if self.no_wait > 0:
            byte = byte | 1 << 4
        struct.pack_into("!B",buffer,offset,byte)
        offset += 1

        offset = self.arguments.pack(buffer,offset)

        return offset

    @staticmethod
    def unpackPayload(channel, buffer):
        method = Declare(channel)

        offset = 4    # class_id and method_id are already known

        (method.reserved_1,) = struct.unpack_from("!H",buffer,offset)
        offset += 2

        (strlen,) = struct.unpack_from("!B",buffer,offset)
        offset += 1
        (method.queue,) = struct.unpack_from("!%ds" % strlen,buffer,offset)
        offset += strlen

        (byte,) = struct.unpack_from("!B",buffer,offset)
        if byte & 1 << 0 > 0:
            method.passive = 1
        else:
            method.passive = 0

        (byte,) = struct.unpack_from("!B",buffer,offset)
        if byte & 1 << 1 > 0:
            method.durable = 1
        else:
            method.durable = 0

        (byte,) = struct.unpack_from("!B",buffer,offset)
        if byte & 1 << 2 > 0:
            method.exclusive = 1
        else:
            method.exclusive = 0

        (byte,) = struct.unpack_from("!B",buffer,offset)
        if byte & 1 << 3 > 0:
            method.auto_delete = 1
        else:
            method.auto_delete = 0

        (byte,) = struct.unpack_from("!B",buffer,offset)
        if byte & 1 << 4 > 0:
            method.no_wait = 1
        else:
            method.no_wait = 0
        offset += 1

        method.arguments = FieldTable()
        offset = method.arguments.unpack(buffer,offset)

        return method
