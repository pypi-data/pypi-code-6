#!/usr/bin/env python
# -*- coding: utf-8 -*-
import clientinfo, hubinfo, protocol, socket, ssl, threading, nicklist

class Client:
	
	def __init__(self):
		self.clientinfo = clientinfo.ClientInfo()
		self.hubinfo = hubinfo.HubInfo()
		self.protocol = protocol.ProtocolHandler(self)
		self.nicklist = nicklist.NickList()
		self.sid = ""
		self.isconnected = None
		self.debug = False
		self.events = {}
		
	def sckread(self):
		while 1:
			data = self.sckfile.readline()
			if not data: break
			if data:
				if self.debug:
					print "Receive:> " + data.strip()
				self.protocol.processcommand(data.strip())
	
	def connect(self):
		self.isconnected = False
		self.nicklist.clear()
		self.sckdata = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if self.clientinfo.do_ssl == True:
			self.sckdatassl = ssl.wrap_socket(self.sckdata)
			self.sckdatassl.connect((self.clientinfo.hostname, self.clientinfo.port))
			self.sckfile = self.sckdatassl.makefile()
		else:
			self.sckdata.connect((self.clientinfo.hostname, self.clientinfo.port))
			self.sckfile = self.sckdata.makefile()
		if self.debug:
			print "Debug Mode is Active"
		if 'onconnecting' in self.events:
			self.events['onconnecting'](self.clientinfo.hubaddress())
		self.sendrawmessage("HSUP ADBASE ADTIGR ADALIV ADORLY")
		self.sckthrd = threading.Thread(target=self.sckread)
		self.sckthrd.start()
		
	def disconnect(self):
		if self.clientinfo.do_ssl == True:
			self.sckdatassl.close()
		else:
			self.sckdata.close()
		self.isconnected = False
		self.nicklist.clear()
		
	def sendrawmessage(self, message):
		try:
			if not message.endswith("\n"):
				message += "\n"
			if self.debug:
				print "SEND:> " + message
			if self.clientinfo.do_ssl == True:
				self.sckdatassl.sendall(message)
			else:
				self.sckdata.sendall(message)
		except:
			print "Error trying to send data."
			
	def sendmainchatmessage(self, message):
		if message.endswith("\n"):
			message = message[0:len(message)-1]
		msg = "BMSG {0} {1}\n".format(self.sid, self.protocol.dcencode(message))
		self.sendrawmessage(msg)
	
	def sendprivatemessagebyclass(self, user, message):
		if message.endswith("\n"):
			message = message[0:len(message)-1]
		msg = "EMSG {0} {1} {2} PM{0}\n".format(self.sid, user.sid, self.protocol.dcencode(message))
		self.sendrawmessage(msg)
	
	def sendprivatemessage(self, username, message):
		user = None
		for item in self.nicklist.userlist:
			if item.username == username:
				user = item
		self.sendprivatemessagebyclass(user, message)
	
	def sendprivatemainchatmessagebyclass(self, user, message):
		msg = "DMSG {0} {1} {2}\n".format(self.sid, user.sid, self.protocol.dcencode(message))
		self.sendrawmessage(msg)
	
	def sendprivatemainchatmessage(self, username, message):
		user = None
		for item in self.nicklist.userlist:
			if item.username == username:
				user = item
		self.sendprivatemainchatmessagebyclass(user, message)
	
	def sendalive(self, token):
		msg = "HLIV {0} TO{1}".format(self.SID, token)
		self.sendrawmessage(msg)
	"""
	def sendsearch(self, searchinfo):
		self.sendrawmessage(searchinfo.tostring())
	
	def sendsearchreply(self, username, searchreply):
		msg = "RES {0} {1} {2}\n".format(self.sid, user, searchreply.tostring())
		self.sendrawmessage(msg)
	
	def sendsearchreplybyclass(self, user, searchreply):
		self.sendsearchreply(user.sid, searchreply)
	"""
	def sendconnecttome(self, user):
		msg = "DCTM {0} {1} {2}\n".format(user.SID, self.clientinfo.clientport, user.token)
		self.sendrawmessage(msg)
	
	def sendrevconnecttome(self, user, ssl):
		proto = "ADC/1.0"
		if ssl:
			proto = "ADCS/0.10"
		msg = "DCRM {0} [1} {2} foobar\n".format(self.sid, user.sid, proto)
		self.sendrawmessage(msg)
	
	
	
