import socket
import re
import sys
import tld
import can_get

OK = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'

class Query:
	def __init__(self, domain):
		self._raw_socket = ""
		self._domain = domain
		self._tld = ""
		self._tldURL = ""
		self._detail_array = {}
		self._error_check = 1

		regex = re.compile('.+\..+')
		match = regex.search(self._domain)
		if not match:
			# Invalid domain
			self._display_fail("Invalil domain")
			return

		# Divice TLD
		regex = re.compile('\..+')
		match = regex.search(self._domain)
		if match:
			self._tld = match.group()
		else:
			self._display_safe("Not found TLD")
			return

		# Get TLD List
		tld_list = tld.get_tld_list()
		if not tld_list.has_key( self._tld ):
			self._display_fail("Not Found TLD whois server")
			return
		
		self._tldURL = tld_list.get( self._tld ) 

		self._raw_socket = self._get_raw_socket( self._tldURL , self._domain, 43)
		#print self._raw_socket

		self._error_check = 0
	
	# check whether possible to acquire domain
	def get_vacant_bool(self):
		return can_get.check(self._raw_socket, self._tldURL)

		'''
		if self._error_check == 1:
			self._display_fail("Failed to get WHOIS DATA")
			return -1
		
		regex = re.compile("No match for \"%s\"\." % self._domain.upper())
		match = regex.search(self._raw_socket)
		if match:
			self._display_safe("Yes can Get")
			return 1
		
		self._display_fail("No can Get")
		return 0
		'''
	
	# Get Raw whois data
	def get_raw_data(self):
		return self._raw_socket

	'''
	def get_detail(self):
		if self._error_check == 1:
			return self._detail_array

		for match in re.finditer(".+:.*", self._raw_socket, re.MULTILINE):
			row_str = match.group()
			option_index = row_str.split(':')[0]
			option_value = row_str.split(':')[1]
			#print "%s:%s" % (option_index, option_value)
			self._detail_array.update( {option_index : option_value} )
		
		
		return self._detail_array
	'''



	# Get raw data method
	def _get_raw_socket(self, server, msg, port=43):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect( ( server, port) )
		sock.send("%s\r\n" % msg)
		buf = ""
		while True:
			data = sock.recv(1024)
			if len(data) == 0:
				break
			buf += data
		return buf

	# Display method
	def _display_fail(self, msg):
		sys.stdout.write('\033[91m')
		sys.stdout.write("%s\n" % msg)
		sys.stdout.write('\033[0m')

	def _display_safe(self, msg):
		sys.stdout.write('\033[92m')
		sys.stdout.write("%s\n" % msg)
		sys.stdout.write('\033[0m')

