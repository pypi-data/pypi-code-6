
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

import struct

#######################################################################################################################

class FieldTable(object):

    def __init__(self):
        self.rows = []    # change to a set?

    def __str__(self, indent=""):
        ftstr = ""
        for row in self.rows:
            ftstr += row.__str__(indent)
        return ftstr

    def length(self):
        return 4 + self.contentLength()

    def contentLength(self):
        l = 0
        for row in self.rows:
            l += row.length()
        return l

    def pack(self, buffer, offset):
        struct.pack_into("!I",buffer,offset,self.contentLength())
        offset += 4
        for row in self.rows:
            offset = row.pack(buffer,offset)
        return offset

    def unpack(self, buffer, offset):
        self.rows = []

        (len,) = struct.unpack_from("!I",buffer,offset)
        offset += 4

        starting_offset = offset
        while offset < starting_offset + len:
            row = FieldTable.FieldRow()
            offset = row.unpack(buffer,offset)
            self.rows.append(row)

        return offset

    class FieldRow(object):
        def __init__(self):
            self.name = None
            self.type = None
            self.value = None

        def __str__(self, indent=""):
            if self.type == "F":
                return indent + self.name + " (" + self.type + "):\n" + self.value.__str__(indent+"    ")
            else:
                return indent + self.name + " (" + self.type + "): " + str(self.value) + "\n"

        def length(self):
            l = 1 + len(self.name)
            l += 1

            if self.type == "t":    # boolean
                raise Exception("boolean not yet supported")
            elif self.type == "b":  # signed 8-bit
                l += 1
            elif self.type == "s":  # signed 16-bit
                l += 2
            elif self.type == "I":  # signed 32-bit
                l += 4
            elif self.type == "l":  # signed 64-bit
                l += 8
            elif self.type == "f":  # 32-bit float
                l += 4
            elif self.type == "d":  # 64-bit float
                l += 8
            elif self.type == "D":  # Decimal
                raise Exception("decimal not yet supported")
            elif self.type == "S":  # long string
                l += 4 + len(self.value)
            elif self.type == "T":  # timestamp (unsigned 64-bit)
                l += 8
            elif self.type == "F":  # nested table
                l = self.value.length()
            elif self.type == "V":  # void
                pass
            elif self.type == "x":  # byte array
                raise Exception("byte array not yet supported")

            return l

        def pack(self, buffer, offset):
            struct.pack_into("!B",buffer,offset,len(self.name))
            offset += 1
            struct.pack_into("!%ds" % len(self.name),buffer,offset,self.name)
            offset += len(self.name)

            struct.pack_into("!B",buffer,offset,len(self.type))
            offset += 1

            if self.type == "t":    # boolean
                raise Exception("boolean not yet supported")
            elif self.type == "b":  # signed 8-bit
                struct.pack_into("!b",buffer,offset,len(self.value))
                offset += 1
            elif self.type == "s":  # signed 16-bit
                struct.pack_into("!h",buffer,offset,len(self.value))
                offset += 2
            elif self.type == "I":  # signed 32-bit
                struct.pack_into("!i",buffer,offset,len(self.value))
                offset += 4
            elif self.type == "l":  # signed 64-bit
                struct.pack_into("!q",buffer,offset,len(self.value))
                offset += 8
            elif self.type == "f":  # 32-bit float
                struct.pack_into("!f",buffer,offset,len(self.value))
                offset += 4
            elif self.type == "d":  # 64-bit float
                struct.pack_into("!d",buffer,offset,len(self.value))
                offset += 8
            elif self.type == "D":  # Decimal
                raise Exception("decimal not yet supported")
            elif self.type == "S":  # long string
                struct.pack_into("!I",buffer,offset,len(self.value))
                offset += 4
                struct.pack_into("!%ds" % len(self.value),buffer,offset,self.value)
                offset += len(self.value)
            elif self.type == "T":  # timestamp (unsigned 64-bit)
                struct.pack_into("!Q",buffer,offset,len(self.value))
                offset += 8
            elif self.type == "F":  # nested table
                offset = self.value.pack(buffer,offset)
            elif self.type == "V":  # void
                pass
            elif self.type == "x":  # byte array
                raise Exception("byte array not yet supported")
        
            return offset

        def unpack(self, buffer, offset):
            #print("FieldRow.unpack")
            (strlen,) = struct.unpack_from("!B",buffer,offset)
            offset += 1
            #print("  name is of size %d" % strlen)
            #print("  reading at offset of %d into a buffer of size %d" % (offset,len(buffer)))
            (self.name,) = struct.unpack_from("!%ds" % strlen,buffer,offset)
            offset += strlen
            #print("name is "+self.name)

            (self.type,) = struct.unpack_from("!c",buffer,offset)
            offset += 1

            #print("type is "+self.type)

            if self.type == "t":    # boolean
                (value,) = struct.unpack_from("!B",buffer,offset)  # assume it is an unsigned 8-bit
                offset += 1
                if value > 0:
                    self.value = True
                else:
                    self.value = False
            elif self.type == "b":  # signed 8-bit
                (self.value,) = struct.unpack_from("!b",buffer,offset)
                offset += 1
            elif self.type == "s":  # signed 16-bit
                (self.value,) = struct.unpack_from("!h",buffer,offset)
                offset += 2
            elif self.type == "I":  # signed 32-bit
                (self.value,) = struct.unpack_from("!i",buffer,offset)
                offset += 4
            elif self.type == "l":  # signed 64-bit
                (self.value,) = struct.unpack_from("!q",buffer,offset)
                offset += 8
            elif self.type == "f":  # 32-bit float
                (self.value,) = struct.unpack_from("!f",buffer,offset)
                offset += 4
            elif self.type == "d":  # 64-bit float
                (self.value,) = struct.unpack_from("!d",buffer,offset)
                offset += 8
            elif self.type == "D":  # Decimal
                raise Exception("decimal not yet supported")
            elif self.type == "S":  # long string
                (strlen,) = struct.unpack_from("!I",buffer,offset)
                offset += 4
                (self.value,) = struct.unpack_from("!%ds" % strlen,buffer,offset)
                offset += strlen
            elif self.type == "T":  # timestamp (unsigned 64-bit)
                (self.value,) = struct.unpack_from("!Q",buffer,offset)
                offset += 8
            elif self.type == "F":  # nested table
                self.value = FieldTable()
                offset = self.value.unpack(buffer,offset)
            elif self.type == "V":  # void
                pass
            elif self.type == "x":  # byte array
                raise Exception("byte array not yet supported")


            return offset

#######################################################################################################################
