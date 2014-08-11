import entDevType as edt

class entropyDeviationType:
	"""
	A class that provides an interface to Chi-Square distribution 
	testing, Shannon Entropy Analysis and Monte Carlo Pi Approximation 
	for the purposes of analyzing entropy in unknown binary stream to 
	locate hidden or encrypted data with a primary intended focus on
	XOR encrypted PE files hidden in Office, PDF, et cetera documents
	"""


	def __init__(self, bs = 8192):
		"""
		Takes a parameter, 'bs' that represents the block size 
		represented in byte to be used. The default value is 
		8192 or 8KB
		"""
		self.block_size = bs
		self.edt 		= edt.entDevType(long(bs))

	def openFile(self, name, whole = False):
		"""
		Opens and reads the file specified by 'name'
		performs whole file analysis if 'whole' is True
		"""	

		self.fileName 	= name
		self.fileHand 	= open(self.fileName, 'rb')
		self.data		= self.fileHand.read()

		self.fileHand.close()
		self.edt.setData(self.data, long(self.block_size), whole)
		self.edt.calculate()

	def getBlockCount(self):
		"""
		Returns the number of blocks in a file
		"""

		return self.edt.count()

	def isValidBlockNumber(self, idx, base = 16):
		"""
		Checks that a given index, 'idx' is within the range of 
		valid blocks; defaults to base 16 format, modified by the
		'base' parameter. Returns True if the index is valid.
		"""

		if type(idx) == str:
			idx = long(idx, base)

		if self.edt.maxIndex() < idx:
			return False

		else:
			return True

	def isValidBlockRange(self, low, high, base = 16):
		"""
		Checks that a given range of indices demarked by 'low' and
		'high' are valid; defaults to base 16 format and modified by 
		the 'base' parameter. Returns True if the range is valid
		"""

		if self.isValidBlockNumber(low, base) and self.isValidBlockNumber(high, base):
			return True
	
		return False

	def getScore(self, idx, base = 16):
		"""
		Gets the Chi, Shannon and Pi approximation score 
		for a given block indicated by 'idx', which by 
		default is specified in base 16 format but can be
		changed via the 'base' parameter. Returns a 
		native object with the properties 'chi_square',
		'shannon' and 'estimate' and 'error' for the Chi, 
		Shannon Entropy and Monte Carli Pi approximation
		respectively. Throws a ValueError() if the index is
		invalid
		"""

		if not self.isValidBlockNumber(idx, base):
			raise ValueError("Invalid block number")

		return self.edt.getScore(idx)

	def getAllScores(self):
		"""Retrieves the Chi, Shannon and Pi approximation scores  
		for all blocks in the file. Returns a list() of native
		objects with 'chi_square', 'shannon', 'estimate' and 
		'error' properties for the Chi, Shannon and Pi approximation 
		values respectively"""
 
		return self.edt.getAllScores()

	def getWholeFileScore(self):
		"""
		Retrieves the Chi, Shannon and Pi approximation scores 
		for the entire file. Returns a native object with 
		'chi_square', 'shannon', 'estimate' and 'error' properties 
		for the Chi, Shannon and Pi approximation values respectively
		"""
		
		return self.edt.getWholeScore()

	def getXYDeviation(self, x, y, base = 16):
		"""
		Retrieves the Chi, Shannon and Pi approximation 
		deviation scores between two blocks indicated by 
		the parameters 'x' and 'y', which by default are 
		specified in base 16 format but is changable via 
		the 'base' parameter. Returns a native object
		With 'chi_square', 'shannon', 'estimate' and 
		'error' properties that indicate the deviation
		between the two blocks. Throws a ValueError()
		if the specified range is invalid.
		"""

		if type(x) == str:
			x = long(x, base)

		if type(y) == str:
			y = long(y, base)

		if self.isValidBlockRange(x, y, base):
			return self.edt.getDeviation(x, y)
	
		raise ValueError("Invalid XY range")

	def getBlockAllDeviation(self, x, base = 16):
		"""
		Retrieves the Chi, Shannon and Pi approximation 
		deviations between all blocks in a file against
		the block specified by the parameter 'x', which 
		by default is specified in base 16 format, but is
		changable via the 'base' parameter. 
		Returns a list() of native objects with 'chi_square', 
		'shannon', 'estimate' and 'error' properties for the 
		Chi, Shannon and Pi approximation values respectively. 
		Throws a ValueError() if the specified index is invalid
		"""
		if self.isValidBlockNumber(x, base):
			return self.edt.getAllDeviations(x)

		raise ValueError("Invalid block number")

	def getWholeFileDeviation(self, x, base = 16):
		"""
			Returns the Chi, Shannon and Pi approximation 
			deviations for a block indicated by the parameter 
			'x' relative to the entire file. The index is specified 
			in base 16 by default, however that is customizable via 
			'base' parameter. The returned native object has 
			properties named 'chi_square', 'shannon', 'estimate' and 
			'error' for the Chi, Shannon and Pi approximation values
			respectively. If the index specified is invalid then a
			ValueError() is thrown.
		"""
		if self.isValidBlockNumber(x, base):
			return ed.getWholeFileDeviation(x)

		raise ValueError("Invalid block number")

	def getSequentialDeviation(self, x = 0, y = 0, base = 16):
		"""
			Calculates the deviation for sequential blocks, both
			prior and following within a range of blocks that is 
			specified by the 'x' and 'y' parameters or every block 
			in the file by default. The x and y parameters by default 
			are specified in base 16 format however this is 
			customizable via the 'base' parameter.
			Returns a list() of dict() objects with the keys 
			'prior', 'next', 'index' and 'dev' for the prior block 
			number, next block number, the block the deviations 
			are relative to, and the native object respectively.
			Only one of the 'prior' and 'next' keys will be valid 
			in any given list element. The other will have a value
			of None. The object stored at the key 'dev' will 
			contain the properties 'chi_square', 'shannon', 
			'estimate' and 'error' for the Chi, Shannon and Pi
			approximation values respectively.
			Throws a ValueError() if the index range specified is 
			invalid.
		"""
		ret = list() 

		if 0 == x and 0 == y:
			x = 0
			y = self.edt.maxIndex()

		if x > y:
			raise ValueError("Invalid block range specified (x > y)")

		if not self.isValidBlockRange(x, y, base):
			raise ValueError("Invalid block range specified")

		for idx in range(x, y, 2):
			if (0 != idx):
				ret.append(dict({'prior': idx-1, 
						'next': None, 
						'index': idx, 
						'dev': self.edt.getDeviation(idx-1, idx)}))

			if self.edt.maxIndex()-1 != idx:
				ret.append(dict({'prior': None, 
						'next': idx+1, 
						'index': idx, 
						'dev': self.edt.getDeviation(idx, idx+1)}))

		return ret
	
	def findHighDeviation(self, c = 100, s = 20, e = 1):
		"""
		THIS METHOD IS AN ILLUSTRATED EXAMPLE ONLY.
		Attempts to find blocks with high deviation values relative to 
		the blocks around it. What constitutes high deviation is 
		specified by the 'c', 's' and 'e' parameters that denote the 
		Chi Square, Shannon and Pi approximation Estimate respectively
		Returns a list of native objects for any blocks that match, or
		an empty list if none do. The returned native objects have the
		properties 'chi_square', 'shannon', 'estimate' and 'error' for 
		the Chi, Shannon and Pi approximation deviation values 
		respectively.
		"""
		ret 	= list()
		items 	= self.getSequentialDeviation(0, self.edt.maxIndex()) 

		for item in items:
			dev = item['dev']

			if dev.chi_square > c and dev.shannon > s and dev.estimate > e:
				ret.append(item)

		return ret

	def getBlocksAverage(self, ilist):
		"""
		Averages the Chi, Shannon and Pi approximation values in a list()
		specified by the 'ilist' parameter.
		Returns a dict() object with 'chi_square', 'shannon', 
		'estimate' and 'error' keys containing the averaged Chi,
		Shannon and Pi approxmation values. Throws a ValueError()
		if passed an empty list() as a parameter
		"""
			
    		ret = dict({'chi_square': 0.0, 'shannon': 0.0, 'estimate': 0.0, 'error': 0.0})
    		cnt = len(ilist);
		chi = 0.0
    		sha = 0.0
    		est = 0.0
    		err = 0.0

		if 0 == cnt:
			raise ValueError("An invalid (empty) list was specified")	

    		for item in ilist:
        		chi += item['dev'].chi_square
        		sha += item['dev'].shannon
        		est += item['dev'].estimate
        		err += item['dev'].error

        	ret['chi_square'] = chi/cnt
        	ret['shannon'] = sha/cnt
        	ret['estimate'] = est/cnt
        	ret['error'] = err/cnt

    		return ret

	def isHighAverageChi(self, maxv, chi = 15):
		"""
		WARNING: METHOD IS AN ILLUSTRATED EXAMPLE ONLY.
		Identifies blocks with uniform or near uniform Chi
		distributions for a range between the first block and
		the block specified by 'maxv'. The blocks in that range 
		have their scores averaged and then if the average exceeds 
		a percentage specified by the 'chi' parameter it returns
		true. Otherwise it returns false. The 'maxv' parameter is
		specified in base 16 format and methods called by this
		method can throw a ValueError() when an invalid index is 
		specified.
		"""
		items   = self.getSequentialDeviation(0, maxv)
		avg	= self.getBlocksAverage(items)
				

		if avg['chi_square'] > chi:
			return True

		return False	

	def priorHighAndNextLowShannon(self, idx, high = 20.0, low = 2.5):
		"""
		WARNING: METHOD IS AN ILLUSTRATED EXAMPLE ONLY.
		Attempts to identify the beginning of a significant deviation 
		by attempting to determine if the block denoted by the 
		parameter 'idx' has a high percentage of deviation in its
		Shannon score relative to the prior block and a low percentage 
		of deviation in its Shannon score in the block that follows it.
		The high and low marks are denoted by the parameters 'high' and 
		'low' and default to 20% and 2.5% respectively. These values 
		were chosen based on deviations in a very small sample and will
		result in high false negative and false positive results.
		Returns true if the prior blocks Shannon deviation exceeds 
		'high' and the following blocks is less than 'low', otherwise 
		it returns false. A ValueError() is thrown if the index, 
		index-1 or index+1 are invalid.
		"""
		prv = None
		nxt = None
 
		if (not self.isValidBlockNumber(idx) or 
			not self.isValidBlockNumber(idx-1) or 
			not self.isValidBlockNumber(idx+1)):
				raise ValueError("An invalid index was specified")

		prv = self.getXYDeviation(idx-1, idx)
		nxt = self.getXYDeviation(idx, idx+1)

		if prv.shannon > high and nxt.shannon < low:
			return True

		return False		

	def getSequentialLowShannon(self, idx, low = 1.7):
		"""
		WARNING: METHOD IS AN ILLUSTRATED EXAMPLE ONLY.
		Attempts to identify sequential blocks of deviant 
		data by looking for low Shannon score deviations 
		in sequential blocks. The block to start at is 
		specified by the 'idx' parameter, which is specified 
		in base 16 format. What exactly constitutes a low percentage 
		of deviation is specified by the parameter 'low', which 
		defaults to 1.7%. This value was chosen based on analysis of 
		a very small set of samples and is likely to result in high 
		amounts of false positive and false negatives as a result.
		Returns the index of the highest block following 'idx' that
		has a relative Shannon deviation less than 'low', or the index
		specified by 'idx' if the following block does not match.
		Throws a ValueError() if the index specified is invalid.
		"""
		ret = list()

		if not self.isValidBlockNumber(idx):
			raise ValueError("An invalid index was specified")

		for idx in range(idx, self.edt.maxIndex()):
			if not self.isValidBlockNumber(idx+1):
				return idx

			dev = self.getXYDeviation(idx, idx+1)

			if dev.shannon < low:
				continue	
			else:
				return idx

		return idx

	def getSequentialCloseChi(self, lidx, hidx, dmax = 26.0):
		"""
		WARNING: METHOD IS AN ILLUSTRATED EXAMPLE ONLY
		Attempts to identify related deviant blocks between a range 
		specified by the indices 'lidx' and 'hidx' respectively.
		Specifically this method attempts to identify blocks that have 
		Chi Square scores that are within 'dmax' percent of one 
		another, which defaults to 26%. This value was chosen based on 
		analysis of a very small sample set and is likely to result in 
		high false positive and false negative rates if used as is.
		The theory is based on the observation that the distribution of
		shorter XOR keys varies relatively little.
		Returns the highest index of a block that follows 'lidx' that
		deviates less than 'dmax' percent, or 'lidx' if the block 
		immediately following 'lidx' exceeds 'dmax'%.
		Throws a ValueError() if the index range specified is invalid.
		"""
		ret = 0		
		
		if lidx > hidx or not self.isValidBlockRange(lidx, hidx):
			raise ValueError("An invalid index range was specified")

		ret = lidx

		for idx in range(lidx, hidx):
			dev = self.getXYDeviation(idx, idx+1)

			if dev.chi_square < dmax:
				ret = idx
			else:
				break
		return ret

	def coalesceSequential(self, lst, maxv = 2):
		"""
		Takes a list of tuples in the format of tuple((low, high))
		indicating a start and stop range of blocks and checks to see 
		if sequential list elements have nearly overlapping ranges 
		with a distance less than or equal to 'maxv'.
		The concept behind this method is that once a sequence of 
		suspicious blocks are identified it is not uncommon for a 
		few outlier blocks to cause multiple ranges of suspect blocks 
		that really is a single range of blocks. As such, this method 
		checks to see if that is the case and coalesces the indices 
		into a single range of blocks.
		Returns a list of tuples with high and low ranges.
		"""
		pb 	= None
		ph 	= None
		ret	= list()	

		for itr in lst:
			if None == pb and None == ph:
				pb = itr[0]
				ph = itr[1]
				continue
			elif itr[0] - ph <= maxv:
				ph = itr[1]
				continue
			else:
				ret.append(tuple((pb, ph)))
				pb = itr[0]
				ph = itr[1]

		if len(ret) and ret[-1][0] != pb and ret[-1][1] != ph:
			ret.append(tuple((pb, ph)))

		return ret

	def calculateDistribution(self, x = 0, y = 0, base = 16):
		"""
		Takes a range of block indices denoted by 'x' and 'y', which
		are specified in base 16 format by default and calculates the
		frequency each character occurs in the block range. The idea 
		is that shorter XOR keys across real data tend to encounter the
		value zero a lot, which leaks the key in question. Thus by 
		analyzing the frequency of characters in a block range, we can
		easily spot abnormal sequential frequencies and quickly 
		identify an XOR key as a result.
		Returns a list sorted in descending order of the frequency of
		each character in the block range, yielding a list with a 
		static length of 256. Throws a ValueError() if the range
		specified is invalid.
		"""
		dist = list()

		if 0 == y:
			y = self.edt.maxIndex()

		if not self.isValidBlockRange(x, y):
			raise ValueError("Invalid index range specified")
		
		self.edt.calculateDistribution(x, y)
		dist = self.edt.getDistribution()
		dist = sorted(dist, key=lambda d: d.count)
		dist.reverse()

		return dist

