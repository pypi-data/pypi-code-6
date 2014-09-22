#!/usr/bin/python

#The MIT License (MIT)
#
#Copyright (c) 2013 Jeff Ciesielski <jeffciesielski@gmail.com>
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

import socket
import multiprocessing
from multiprocessing import Event, Queue
from threading import Thread
import struct
import os
import errno
from time import sleep
import traceback
import netifaces as ni
import traceback
import sys
import logging

logging.debug("")
_log = logging.getLogger('sddcp')
_log.setLevel(logging.INFO)

#TODO: Fix magic numbers

# Protocol definitions
SDDCP_VER = "sddcp1"

SDDCP_TYPE_NONE = None
SDDCP_TYPE_ANNOUNCE = "ann"
SDDCP_TYPE_COMMAND = "cmd"
SDDCP_TYPE_ACK = "ack"
SDDCP_TYPE_NAK = "nak"
SDDCP_TYPE_QUERY = "qry"

SDDCP_MESSAGE_TYPES = [SDDCP_TYPE_ANNOUNCE,
                       SDDCP_TYPE_COMMAND,
                       SDDCP_TYPE_ACK,
                       SDDCP_TYPE_NAK,
                       SDDCP_TYPE_QUERY]

SDDCP_SERVICE_STR = "svc"
SDDCP_COM_STR = "com"
SDDCP_RSP_STR = "rsp"

SDDCP_PAYLOAD_TYPE_MAP = {
    SDDCP_SERVICE_STR:[SDDCP_TYPE_ANNOUNCE, SDDCP_TYPE_QUERY],
    SDDCP_COM_STR:[SDDCP_TYPE_COMMAND]
    }

SDDCP_ALL = "~"

# Server Definitions
SDDCP_SRV_PORT = 55555
SDDCP_SRV_MCAST_ADDR = '239.255.1.2'

def set_log_verbosity(v):
    _log.setLevel(v)

def get_interface_ip(iface = None):
    try:
        if not iface:
            if sys.platform == 'win32':
                iface = ni.interfaces()[0]
            else:
                iface = ni.interfaces()[1]

        return ni.ifaddresses(iface)[2][0]['addr']
    except:
        return None

def get_local_ips():
    return map(get_interface_ip, ni.interfaces())

class attribute:
    def __init__(self, key, value):
        if len(key) > 32 or len(value) > 32:
            raise Exception("Key/Value string len must be <= 32 ")

        self.key = key
        self.value = value

    def __str__(self):
        return "key={} : value={}".format(self.key, self.value)

class payload:
    def __init__(self, type_name, name):
        self.type_name = type_name
        self.name = name
        self.attributes = []

    def __str__(self):
        rst = "~payload~\n{} -- {}\n".format(self.type_name, self.name)
        for attr in self.attributes:
            rst += str(attr)

        return rst
        
    def get_attr_val(self, key):
        val = (x.value for x in self.attributes if x.key == key).next()
        return val

    def get_attr_list(self):
        return list(self.attributes)

    def append_attribute(self, attr):
        if attr.__class__.__name__ != 'attribute':
            print type(attr)
            raise TypeError
        self.attributes.append(attr)

class message(object):
    def __init__(self, msg_type=SDDCP_TYPE_NONE, payload_name = '',
                 from_addr='', to_addr=''):
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.type = msg_type
        pl_type_name = None

        if self.type in  [SDDCP_TYPE_QUERY, SDDCP_TYPE_ANNOUNCE]:
            pl_type_name = SDDCP_SERVICE_STR
        elif self.type == SDDCP_TYPE_COMMAND:
            pl_type_name = SDDCP_COM_STR
        elif self.type in [SDDCP_TYPE_ACK, SDDCP_TYPE_NAK]:
            pl_type_name = SDDCP_RSP_STR

        if msg_type in [SDDCP_TYPE_ANNOUNCE,
                        SDDCP_TYPE_COMMAND, SDDCP_TYPE_QUERY]:
            if not len(payload_name):
                raise Exception("Invalid payload name: {}"\
                                .format(payload_name))

        self.payload = payload(pl_type_name, payload_name)

    def append_payload_attribute(self, attr):
        if attr.__class__.__name__ != 'attribute':
            print type(attr)
            raise TypeError
        self.payload.attributes.append(attr)

    def get_payload_name(self):
        return self.payload.name

    def get_payload_type(self):
        return self.payload.type_name

    def __str__(self):
        if not self.type:
            raise Exception("Invalid type, cannot print")

        retstr = "{"
        retstr += SDDCP_VER + '*' + self.type
        retstr += "({}|{})".format(self.from_addr, self.to_addr)

        retstr += "=<"

        retstr += "{}:{}".format(self.payload.type_name, self.payload.name)

        for attr in self.payload.attributes:
            retstr += "|[{}]:{}".format(attr.key, attr.value)

        retstr += ">}"
        return retstr

    def _validate_addresses(self):
        #a very simple test of IP addresses
        for addr in [self.from_addr, self.to_addr]:
            if addr == '~':
                continue

            socket.inet_aton(addr)

    def from_packet(self, pk_str):

        tmp_str = str(pk_str)

        #Validate that the packet is bookeneded by curly braces and
        #that it isn't too large
        if tmp_str[0] != '{' or tmp_str[-1] != '}':
            raise Exception("Invalid packet")

        if len(tmp_str) > 512:
            raise Exception("Packet is too large to be valid")

        #Strip off the outer brackets
        tmp_str = tmp_str[1:-1]

        #Make sure we understand this version
        if not tmp_str[:7] == "{}*".format(SDDCP_VER):
            raise Exception("Invalid packet")

        #strip off the version
        tmp_str = tmp_str[7:]

        #Make sure that this is a valid message type
        if not tmp_str[:3] in SDDCP_MESSAGE_TYPES:
            raise Exception("Invalid packet")

        self.type = tmp_str[:3]

        # Move to beginning of 'from address'
        tmp_str = tmp_str[3:]

        #Split out and validate the from and to addresses
        addstr = tmp_str.split("=")[0]

        if not addstr[0] == '(' and addstr[-1] == ')':
            raise Exception("Invalid packet")

        tmp_str = tmp_str[len(addstr):]
        addstr = addstr[1:-1]

        self.from_addr = addstr.split('|')[0]
        self.to_addr = addstr.split('|')[1]

        self._validate_addresses()

        #Make sure we ended on a known boundary
        if not tmp_str[0] == '=':
            raise Exception("Invalid packet")

        #Strip out the equals sign
        tmp_str = tmp_str[1:]

        #We've arrived at the payload, ensure that it is bookeneded appropriately
        if tmp_str[0] != '<' or tmp_str[-1] != '>':
            raise Exception("Invalid packet")

        #Strip off the angle brackets
        tmp_str = tmp_str[1:-1]

        #Split the payload into the payload type/name and the payload attributes
        payload = tmp_str.split('|')

        #break out the name and type, then validate
        payload_type = payload[0].split(':')[0]
        payload_name = payload[0].split(':')[1]

        if not payload_name or not payload_type:
            raise Exception("Invalid packet")

        if len(payload_name) > 16 or len(payload_type) > 16:
            raise Exception("invalid packet")

        self.payload.type_name = payload_type
        self.payload.name = payload_name

        if len(payload) == 1:
            return self

        payload = payload[1:]

        #now split out each attribute and add them to the payload as
        #attribute objects
        for attr in payload:
            if len(attr.split(':')) != 2:
                raise Exception("Invalid packet")

            attr_key = attr.split(':')[0]
            attr_value = attr.split(':')[1]

            if not (attr_key[0], attr_key[-1]) == ('[', ']'):
                raise Exception("Invalid packet")

            attr_key = attr_key[1:-1]

            self.append_payload_attribute(attribute(attr_key, attr_value))

        return self

    def send(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        sock.sendto(str(self), (SDDCP_SRV_MCAST_ADDR, SDDCP_SRV_PORT))
        sock.close()

class gateway:
    def __init__(self):
        self._sock = None
        self._shutdown = Event()
        self._qry_handlers = {}
        self._cmd_handlers = {}
        self._ann_handlers = {}
        self._ack_handlers = {}
        self._nak_handlers = {}
        self._listening = False
        self._input_buf = []
        self._current_packet = ""
        self._shutdown.clear()

        self._listen_t = None

    def _post_announcement(self, msg):

        if self._ann_handlers.has_key(msg.get_payload_name()):
            for handler in self._ann_handlers[msg.get_payload_name()]:
                handler(msg)

    def _post_command(self, msg):
        if self._cmd_handlers.has_key(msg.get_payload_name()):
            for handler in self._cmd_handlers[msg.get_payload_name()]:
                handler(msg)

    def _post_query(self, msg):
        if self._qry_handlers.has_key(msg.get_payload_name()):
            for handler in self._qry_handlers[msg.get_payload_name()]:
                handler(msg)

    def _post_ack(self, msg):
        if self._ack_handlers.has_key(msg.get_payload_name()):
            for handler in self._ack_handlers[msg.get_payload_name()]:
                handler(msg)

    def _post_nak(self, msg):
        if self._nak_handlers.has_key(msg.get_payload_name()):
            for handler in self._nak_handlers[msg.get_payload_name()]:
                handler(msg)

    def _handle_packet(self):
        msg = message().from_packet(self._current_packet)

        if not msg.to_addr in get_local_ips() and not msg.to_addr == '~':
            _log.debug("Filtering packet:{}".format(msg))
            return

        if msg.type not in SDDCP_MESSAGE_TYPES:
            _log.debug("Invalid message type")
            return

        if msg.type == SDDCP_TYPE_ANNOUNCE:
            self._post_announcement(msg)
        elif msg.type == SDDCP_TYPE_COMMAND:
            self._post_command(msg)
        elif msg.type == SDDCP_TYPE_QUERY:
            self._post_query(msg)
        elif msg.type == SDDCP_TYPE_ACK:
            self._post_ack(msg)
        elif msg.type == SDDCP_TYPE_NAK:
            self._post_nak(msg)
        else:
            print "unhandled message: {}".format(str(msg))

    # Checks for packet, if a valid packet is in the buffer, slice the
    # buffer and handle
    def _check_for_packet(self):
        if len(self._input_buf) == 0:
            _log.debug("zero length input")
            return

        #make sure we have a frame start
        start_idx = self._input_buf.index('{')

        #If there was no match for the start index, clear the current
        #buffer and return
        if start_idx == 0 and self._input_buf[0] != '{':
            self._input_buf[:] = []
            return

        #Re-frame the packet to start at the beginning of the start index
        self._input_buf = self._input_buf[start_idx:]

        # ensure that there is a sequence of charcters framed by {},
        end_idx = None
        idx = 1
        while idx < len(self._input_buf) and not end_idx:
            #This scans for an unescaped }
            if self._input_buf[idx] == '}' and self._input_buf[idx - 1] != '\\':
                end_idx = idx
            idx += 1

        #no end index in sight
        if not end_idx:
            #make sure the input buffer isn't growing too large, if it
            #is, invalidate the current buffer
            if len(self._input_buf) > 512:
                self._input_buf.pop(0)
            return

        # Set the current packet
        self._current_packet = ''.join(self._input_buf[start_idx:end_idx + 1])

        # advance the input buffer
        self._input_buf = self._input_buf[end_idx + 1:]

        # attempt to handle the current packet
        try:
            self._handle_packet()
        except Exception, err:
            print 60*'-'
            print "Unable to decode packet"
            print self._current_packet
            print 60*'-'
            traceback.print_exc(file=sys.stdout)
            print 60*'='

        #get out of here
        return

    def _listen_thread(self):
        _sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                                   socket.IPPROTO_UDP)

        _sock.setblocking(0)

        _sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        _sock.bind(('', SDDCP_SRV_PORT))
        mreq = struct.pack("=4sl", socket.inet_aton(SDDCP_SRV_MCAST_ADDR),
                           socket.INADDR_ANY)
        _sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        while not self._shutdown.is_set():
            try:
                self._input_buf.extend(_sock.recv(512))
            except socket.error, e:
                err = e.args[0]
                if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                    sleep(1)
                    continue
                else:
                    # a "real" error occurred
                    print e
                    sys.exit(1)
            self._check_for_packet()
        _sock.close()
        _log.debug("Closing receive Socket")

    # Starts the UDP listen thread
    def start(self, allow_loopback = False):
        if self._listen_t :
            raise Exception("Already Listening")


        self._listen_t = Thread(target=self._listen_thread)

        _log.info("Starting sddcp gateway")
        self._listen_t.daemon = True
        self._listen_t.start()

    def stop(self):
        self._shutdown.set()

        self._listen_t.join()

        self._listen_t = None

    def register_message_handler(self, msg_type, pl_type, handler):
        _log.debug("Registering {} handler for: {}".format(msg_type, pl_type))
        if not msg_type in SDDCP_MESSAGE_TYPES:
            raise Exception("Invalid message type")

        msg_handler_map = {
            SDDCP_TYPE_ANNOUNCE : self._ann_handlers,
            SDDCP_TYPE_COMMAND  : self._cmd_handlers,
            SDDCP_TYPE_ACK      : self._ack_handlers,
            SDDCP_TYPE_NAK      : self._nak_handlers,
            SDDCP_TYPE_QUERY    : self._qry_handlers,
            }

        handler_dict = msg_handler_map[msg_type]

        if not handler_dict.has_key(pl_type):
            handler_dict[pl_type] = []

        if not handler in handler_dict[pl_type]:
            handler_dict[pl_type].append(handler)

def test_encoding():
    # A simple test of funcionality
    ann = "{sddcp1*ann(192.168.32.1|~)=<svc:mqtt|[data]:temperature>}"
    qry = "{sddcp1*qry(192.168.32.1|~)=<svc:tftp>}"
    cmd = "{sddcp1*cmd(192.168.32.1|192.168.32.2)=<com:mqtt_st|[port]:1334>}"
    ack = "{sddcp1*ack(192.168.32.1|192.168.32.2)=<rsp:mqtt>}"
    nak = "{sddcp1*nak(192.168.32.1|192.168.32.1)=<rsp:mqtt>}"

    print "Announce Packet:"
    ann_msg = message().from_packet(ann)
    print '-', ann_msg, '\n', 40*'-'

    print "Query Packet:"
    qry_msg = message().from_packet(qry)
    print '-', qry_msg, '\n', 40*'-'

    print "Command Packet:"
    cmd_msg = message().from_packet(cmd)
    print '-', cmd_msg, '\n', 40*'-'

    print "Ack Packet:"
    ack_msg = message().from_packet(ack)
    print '-', ack_msg, '\n', 40*'-'

    print "Nak Packet:"
    nak_msg = message().from_packet(nak)
    print '-', nak_msg, '\n', 40*'-'

def _announce_handler(msg):
    print "Node: {} has announced service:".format(msg.from_addr)
    print "<{}>".format(msg.get_payload_name())

    for attr in msg.payload.get_attr_list():
        print '- [{}]: {}'.format(attr.key, attr.value)

def _ack_handler(msg):
    print "Node: {} has ACK'd service:".format(msg.from_addr)
    print "<{}>".format(msg.get_payload_name())

def test_gateway():
    print "Testing gateway functionality"
    ann = message(msg_type=SDDCP_TYPE_ANNOUNCE,
                  payload_name='mqtt',
                  from_addr=SDDCP_ALL,
                  to_addr=SDDCP_ALL)
    ann.append_payload_attribute(attribute(key='data', value='temperature'))
    ack = message(msg_type=SDDCP_TYPE_ACK,
                  payload_name='mqtt',
                  from_addr=SDDCP_ALL,
                  to_addr=SDDCP_ALL)
    
    ann.from_addr = get_interface_ip()
    ack.from_addr = get_interface_ip()
    
    gate = gateway()

    gate.register_message_handler(SDDCP_TYPE_ANNOUNCE, 'mqtt',
                                  _announce_handler)
    gate.register_message_handler(SDDCP_TYPE_ACK, 'mqtt',
                                  _ack_handler)
    
    gate.start()
    sleep(1)
    ann.send()
    sleep(1)
    ack.send()
    sleep(10)
    gate.stop()

if __name__ == "__main__":
    test_encoding()
    test_gateway()

