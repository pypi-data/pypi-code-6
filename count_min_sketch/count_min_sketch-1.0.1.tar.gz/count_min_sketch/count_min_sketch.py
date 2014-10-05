from numpy import zeros, int32, int16, arange, array
from math import log, e, ceil

class CountMinSketch(object):
	def __init__(self, w, d, bits):
		"""
		CountMinSketch is an implementation of the count min sketch 
		algorithm that probabilistically counts string frequencies.
		
		Parameters
		----------
		w : the number of columns in the count matrix
		d : the number of rows in the count matrix

		bits : The size of the hash output space
		For the full paper on the algorithm, see the paper
		"An improved data stream summary: the count-min sketch and its -
		applications" by Cormode and Muthukrishnan, 2003.
		"""
		
		if 2**bits < w:
			raise Exception("Too few bits for w")

		#Values taken from http://www.isthe.com/chongo/tech/comp/fnv/		
		if bits == 32:
			self.prime = 0x1000193
			self.offset = 0x811c9dc5
		elif bits == 64:
			self.prime = 0x100000001b3
			self.offset = 0xcbf29ce484222325L
		elif bits == 128:
			self.prime = 0x1000000000000000000013bL
			self.offset = 0x6c62272e07bb014262b821756295c58dL
		elif bits == 256:
			self.prime = 0x1000000000000000000000000000000000000000163L
			self.offset = 0xdd268dbcaac550362d98c384c4e576ccc8b1536847b6bbb31023b4c8caee0535L
		elif bits == 512:
			self.prime = 0x100000000000000000000000000000000000000000000000000000000000000000000000000000000000157L
			self.offset = 0xb86db0b1171f4416dca1e50f309990acac87d059c90000000000000000000d21e948f68a34c192f62ea79bc942dbe7ce182036415f56e34bac982aac4afe9fd9L
		elif bits == 1024:
			self.prime = 0x10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000018dL
			self.offset = 0x5f7a76758ecc4d32e56d5a591028b74b29fc4223fdada16c3bf34eda3674da9a21d9000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004c6d7eb6e73802734510a555f256cc005ae556bde8cc9c6a93b21aff4b16c71ee90b3L
		else:
			raise Exception("Bits must be 32, 64, 128, 256, 512, or 1024")
		self.mod = 2**bits-1
		self.bits = bits
		self.w = w
		self.d = d
		self.count = zeros((self.d, self.w), dtype=int32)
		self.rows = arange(self.d)
		self.shift_by = int(ceil(log(w, 2)))
		
	def get_columns(self, a):
		a_string = str(a)
		d = self.d
		w = self.w
		shift_by = self.shift_by
		hashes = zeros(d, dtype=int16)
		
		prime = self.prime
		offset = self.offset
		mod = self.mod
		
		#Hash
		in_bytes = bytearray(a_string)
		h = offset
		for byte in in_bytes:
			h *= prime
			h &= mod
			h ^= byte
		#/Hash
		
		times_hashed = 1
		for i in xrange(d):
			hashes[i] = h % w
			h >>= shift_by
			if h < w and i < d:
				#Hash
				times_hashed += 1
				in_bytes = bytearray(str(i) + a_string)
				h = offset
				for byte in in_bytes:
					h *= prime
					h &= mod
					h ^= byte
				#/Hash
				
		return hashes
		
	def update(self, a, val=1):
		#h, in_cache = self.cache.lookup(a)
		h = self.get_columns(a)
		self.count[self.rows, h] += val
	
	def query(self, a):
		#h, in_cache = self.cache.lookup(a)
		h = self.get_columns(a)
		return self.count[self.rows, h].min()
	
	def __getitem__(self, a):
		return self.query(a)
	
	def __setitem__(self, a, val):
		cur = self.query(a)
		self.update(a, val-cur)