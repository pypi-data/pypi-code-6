from numpy import zeros, int32, int16, arange, array
from math import log, e, ceil

class CountMinSketch(object):
	def __init__(self, w=None, d=None, delta=None, epsilon=None):#,
							#cache_size=0):
		"""
		CountMinSketch is an implementation of the count min sketch 
		algorithm that probabilistically counts string frequencies.
		
		Parameters
		----------
		w : the number of columns in the count matrix
		d : the number of rows in the count matrix

		For the full paper on the algorithm, see the paper
		"An improved data stream summary: the count-min sketch and its -
		applications" by Cormode and Muthukrishnan, 2003.
		"""
		
		self.w = w
		self.d = d
		self.count = zeros((self.d, self.w), dtype=int32)
		self.rows = arange(self.d)
		self.shift_by = int(ceil(log(w, 2)))
	
	def fnv64(self, a_string):
		in_bytes = bytearray(a_string)
		h = 0xcbf29ce484222325
		for byte in in_bytes:
			h *= 0x100000001b3
			h &= 0xffffffffffffffff
			h ^= byte
		return h
		
	def get_columns(self, a):
		a_string = str(a)
		d = self.d
		hashes = zeros(d, dtype=int16)
		fnv64 = self.fnv64
		h = fnv64(a_string)
		w = self.w
		shift_by = self.shift_by
		for i in xrange(d):
			hashes[i] = h % w
			h >>= shift_by
			if h < w and i < d:
				h = fnv64(str(i) + a_string)
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