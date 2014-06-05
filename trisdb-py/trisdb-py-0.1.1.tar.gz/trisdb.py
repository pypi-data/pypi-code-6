#!/usr/bin/python

import socket, struct, sys
import message_pb2

class TrisDbConnection:
    def __init__(self, host, port):
        self.hostname = host
	self.port = port
	try:
	    self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    	    self.client.connect((self.hostname, self.port))
	except:
	    print "Error connecting to %s on port %s" % (self.hostname, self.port)
	    sys.exit()

    def get(self, s, p=None, o=None):
        req = message_pb2.QueryRequest()
	if p is None:
	    req.query = 'GET "%s"' % s
	else:
	    req.query = 'GET "%s" "%s" "%s"' % (s, p, o)
	tmp = self.__sendData(req)
        result = []
        for i in tmp.data:
            result.append({'subject':i.subject, 'predicate':i.predicate, 'object':i.object})
        return result

    def gets(self, s, p, o):
        req = message_pb2.QueryRequest()
        req.query = 'GETS "%s" "%s" "%s"' % (s, p, o)
        tmp = self.__sendData(req)
        result = []
        for i in tmp.data:
            result.append(i.subject)
        return result

    def getp(self, s, p, o):
        req = message_pb2.QueryRequest()
        req.query = 'GETP "%s" "%s" "%s"' % (s, p, o)
        tmp = self.__sendData(req)
        result = []
        for i in tmp.data:
            result.append(i.predicate)
        return result

    def geto(self, s, p, o):
        req = message_pb2.QueryRequest()
        req.query = 'GETO "%s" "%s" "%s"' % (s, p, o)
        tmp = self.__sendData(req)
        result = []
        for i in tmp.data:
            result.append(i.object)
        return result

    def create(self, s, p, o):
        req = message_pb2.QueryRequest()
        req.query = 'CREATE "%s" "%s" "%s"' % (s, p, o)
	tmp = self.__sendData(req)
        result = []
        for i in tmp.data:
            result.append({'subject':i.subject, 'predicate':i.predicate, 'object':i.object})
        return result

    def delete(self, s, p, o):
        req = message_pb2.QueryRequest()
        req.query = 'DELETE "%s" "%s" "%s"' % (s, p, o)
        self.__sendData(req)
        return 'OK'

    def clear(self):
        req = message_pb2.QueryRequest()
        req.query = 'CLEAR'
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
