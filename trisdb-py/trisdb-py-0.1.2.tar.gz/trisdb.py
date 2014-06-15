#!/usr/bin/python

import socket, struct, sys
import message_pb2

class TrisDbConnection:
    def __init__(self, host, port = None):
        self.hostname = host
	self.port = port
	try:
	    if port is None:
	        # unix socket
		self.client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		self.client.connect(self.hostname)
	    else:
		# tcp
	    	self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    	    	self.client.connect((self.hostname, self.port))
	except:
	    print "Error connecting to %s" % (self.hostname)
	    sys.exit()

    def get(self, s, p=None, o=None):
        req = message_pb2.QueryRequest()
	if p is None:
	    req.query.append('GET "%s"' % s)
	else:
	    req.query.append('GET "%s" "%s" "%s"' % (s, p, o))
	tmp = self.__sendData(req)
        result = []
        for i in tmp.data:
            result.append({'subject':i.subject, 'predicate':i.predicate, 'object':i.object})
        return result

    def gets(self, s, p, o):
        req = message_pb2.QueryRequest()
        req.query.append('GETS "%s" "%s" "%s"' % (s, p, o))
        tmp = self.__sendData(req)
        result = []
        for i in tmp.data:
            result.append(i.subject)
        return result

    def getp(self, s, p, o):
        req = message_pb2.QueryRequest()
        req.query.append('GETP "%s" "%s" "%s"' % (s, p, o))
        tmp = self.__sendData(req)
        result = []
        for i in tmp.data:
            result.append(i.predicate)
        return result

    def geto(self, s, p, o):
        req = message_pb2.QueryRequest()
        req.query.append('GETO "%s" "%s" "%s"' % (s, p, o))
        tmp = self.__sendData(req)
        result = []
        for i in tmp.data:
            result.append(i.object)
        return result

    def create(self, s, p, o):
        req = message_pb2.QueryRequest()
        q = req.query.append('CREATE "%s" "%s" "%s"' % (s, p, o))
	self.__sendData(req)
        return 'OK'

    def multi(self):
	return Multi()

    def execute(self, multi):
	self.__sendData(multi.request)
        return 'OK'

    def delete(self, s, p, o):
        req = message_pb2.QueryRequest()
        q = req.query.append('DELETE "%s" "%s" "%s"' % (s, p, o))
        self.__sendData(req)
        return 'OK'

    def clear(self):
        req = message_pb2.QueryRequest()
        req.query.append('CLEAR')
	self.__sendData(req)
	return 'OK'

    def close(self):
	self.client.close()

    def __sendData(self, request):
	try:
	    request.timestamp = '123456789'
	    s = request.SerializeToString()
	    # prepend header and send message
	    packed_len = struct.pack('>L', len(s))
            packed_message = packed_len + s
            self.client.send(packed_message)
	    # read header
	    len_buf = self.socket_read_n(4)
            msg_len = struct.unpack('>L', len_buf)[0]
            msg_buf = self.socket_read_n(msg_len)
            res = message_pb2.QueryResponse()
            res.ParseFromString(msg_buf)
	    return res
        except Exception as e:
            print "Connection error: ",e

    def socket_read_n(self, n):
        buf = ''
        while n > 0:
            data = self.client.recv(n)
            if data == '':
                raise RuntimeError('Connection error')
		sys.exit()
            buf += data
            n -= len(data)
        return buf


class Multi:
    def __init__(self):
        self.request = message_pb2.QueryRequest()

    def create(self, s, p, o):
	self.request.query.append('CREATE "%s" "%s" "%s"' % (s, p, o))
