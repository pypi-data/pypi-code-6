#!/usr/bin/env python
#
# symrange.py
#
# $Id:    $
# $URL: $
#
# Part of the "pydiffract" package
#

import sys

__version__	=	"$Revision: $"
__author__	=	"Jon Tischler, <tischler@aps.anl.gov>" +\
				"Argonne National Laboratory"
__date__	=	"$Date: $"
__id__		=	"$Id: $"


class symrange:
	"""
	symrange class.

	This class provides functions to loop symmetrically outward from 0
	i.e., 0,1,-1,2,-2,3,-3,...
	endVal can only be a positive integer or 0

	EXAMPLE::
		>>> for i in symrange(2): print i
		prints:
		0 1 -1 2 -2 3 -3

		>>> for i in symrange(2,True): print i
		prints:
		0 -1 1 -2 2 -3 3

	NOTE:
		symrange can only contain integers.

	variables and methods that you may be interested in:

	====================    ===========================================================================================
	variables
	====================    ===========================================================================================
	self.endVal             the highest value +/- returned, this is always >= 0
	self.negativeFirst      if True then 0,-1,+1,-2,+2,...   Otherwise 0,+1,-1,+2,-2,...
	self.auto_reset         if True (default), then previous is reset to None at each call to __iter__
	self.length             total number of items in range, you can also get this from len(symrange(n)) or symrange(n).len()
	self.previous           last value returned by the iterator, when previous==None, then a call to next() returns 0
	====================    ===========================================================================================

	====================    ===========================================================================================
	methods
	====================    ===========================================================================================
	next()                  returns next value, updates previous too
	last()                  returns the last number in the range, for self.r="3,5,9-20", self.last() returns 20
	len()                   returns number of points in the range, for self.r="3,5,9-20", self.len() returns 14
	first()                 returns first value of iteration, always returns 0
	after(prev)             returns value that follows prev, without changing the current point in iteration
	index(ipnt)             return the ipntth number from range, first number is ipnt==0, returns None if ipnt negative or too big, same as symrange(2)[ipnt]
	val2index(m)            returns index into range that corresponds to m. e.g. for r='0,-1,1,-2,2', m=1 returns 2.
	list(self)              returns a list where each element is a value in the range, CAUTION this can make a VERY big list if n is large
	====================    ===========================================================================================

	=====================   ======================== ===================================================================
	special methods          command                    result using: syr = symrange(5)
	=====================   ======================== ===================================================================
	__getitem__(n)          print syr[3]                 2
	__len__()               print len(syr)               11
	__str__()               print str(syr)               symrange starting from 0, going to 5, doing positives first, current value = "initialized to start"
	__repr__()              print repr(syr)              symrange[endVal=5, negativeFirst=False, previous=None, len=11, auto_reset=True]
	=====================   ======================== ===================================================================
	"""

	def __init__(self, endVal, negativeFirst=False, auto_reset=True):
		"""
		Initialize the symrange instance.
		If negativeFirst is True, then symrange(2) goes:  0 -1 1 -2 2 -3 3, (negatives first)
		"""
		try:	self.endVal = int(round(endVal))
		except:	raise TypeError('endVal must be an int >= 0, not %r' % endVal)
		if self.endVal<0 or type(endVal) is bool:
			raise ValueError('endVal must be an int >= 0, not %r' % endVal)

		try:	self.negativeFirst = bool(negativeFirst)
		except:	raise TypeError('negativeFirst must be a boolean, not %r' % negativeFirst)

		try:	self.auto_reset = bool(auto_reset)
		except:	raise TypeError("auto_reset must be boolean")

		self.length = (2 * self.endVal + 1)	# number of items in the loop, remember that endVal is positive
		self.previous = None				# flags new iteration, next value will be zero


	def __iter__(self):
		""" The class iterator """
		if self.auto_reset:
			self.previous = None			# flags new iteration, next value will be zero, the default
		return self


	def next(self):
		""" Return the next value in the symrange. """
		if self.previous is None:			# at start
			self.previous = 0
		elif self.negativeFirst and self.previous<0:
			self.previous = -(self.previous)	# neg first & previous negative -> pos previous
		elif self.negativeFirst:
			self.previous = -(self.previous)-1	# neg first & previous positive -> -previous-1
		elif self.previous <= 0:
			self.previous = -(self.previous)+1	# positive first & previous is negative (the <=0 is for item after 0)
		else:
			self.previous = -(self.previous)	# positive first & previous>=0

		if abs(self.previous)>self.endVal:		# end of loop
			raise StopIteration

		return self.previous


	def last(self):
		"""
		Return the value of the last item in the range.
		This method uses but does not change any internal variables, e.g. no self.xxxx
		"""
		if self.negativeFirst:	return self.endVal
		else:					return -self.endVal


	def first(self):
		"""
		Return the value of the first item in the range.
		This is just for completeness, it always returns 0
		"""
		return 0


	def after(self, val):
		""" Return the value of the element that follows after val (which is given). """
		try:	val = int(val)
		except:	raise TypeError('val = %r is not an integer' % val)

		if self.negativeFirst and val<0:	val = -val		# neg first & val negative -> pos val
		elif self.negativeFirst:			val = -val-1	# neg first & val positive -> -val-1
		elif val<=0:						val = -val+1	# positive first & val negative
		else:								val = -val		# positive first & val>=0
		if abs(val)>self.endVal:			val = None		# outside of range
		return val


	def index(self, n):
		"""
		Returns the n-th element from the range, zero based, n==0 is first element.
		This method uses but does not change any internal variables, e.g. no self.xxxx
		This functionality also available by symrange(2)[n], which calles __getitem__() below
		"""
		try:	n = int(n)
		except:	raise TypeError('n = %r is not an integer' % n)
		if n<0:
			val = None
		elif n >= self.length:
			val = None
		else:
			val = (n+1) / 2					# positive value
			isign = n % 2
			if self.negativeFirst and isign:	val = -val
			elif not self.negativeFirst and not isign:	val = -val

		return val


	def __getitem__(self, n):
		""" Return the n-th element in the range. This allows use of the symrange(3)[i] syntax """
		return self.index(n)


	def val2index(self, val):
		"""
		Return the index into the symrange that produces val.
		This method uses but does not change any internal variables, e.g. no self.xxxx

		EXAMPLE::
			>>> sr = symrange(4)
			>>> print sr.val2index(3)
			5
		"""
		try:	val = int(val)
		except:	raise TypeError('val = %r is not an integer' % val)

		n = max(2*abs(val)-1, 0)		# number before
		if abs(val) > self.endVal: n = None
		elif self.negativeFirst and val>0: n += 1
		elif not self.negativeFirst and val<0: n += 1
		return n


	def list(self):
		"""
		Expands the symrange into a standard python list.
		This method uses but does not change any internal variables, e.g. no self.xxxx

		EXAMPLE::
			>>> print symrange(2).list()
			[0, 1, -1, 2, -2]

		CAUTION:
			The following statement::

				>>> symrange(100000).list()

			will produce a list with 200001 elements!

		Max list length for a 32 bit system is (2^32 - 1)/2/4 = 536870912
		on my computer I get a MemoryError for lengths > 1e8, so limit to 1e7
		"""

		lout = [0]
		if self.negativeFirst:
			for i in range(self.endVal):
				lout.append(-i-1)
				lout.append(i+1)
		else:
			for i in range(self.endVal):
				lout.append(i+1)
				lout.append(-i-1)

		return lout


	def __len__(self):
		""" This allows use of   len(symrange(3)) syntax """
		return self.length

	def len(self):
		""" Return the number of items in the symrange. Usage: as symrange(3).len() """
		return self.length


	def __str__(self):
		""" Return string value for symrange. """
		if self.negativeFirst:	sss = 'negatives'
		else:					sss = 'positives'
		if self.previous is None:	current = '"initialized to start"'
		else:					current = str(self.previous)
		return 'symrange starting from 0, going to %d, doing %s first, current value = %s' % (self.endVal, sss, current)

	def __repr__(self):
		""" Return printable representation for a symrange. """
		return 'symrange[endVal=%r, negativeFirst=%r, previous=%r, len=%r, auto_reset=%r]' % (self.endVal, self.negativeFirst, self.previous, self.length, self.auto_reset)

