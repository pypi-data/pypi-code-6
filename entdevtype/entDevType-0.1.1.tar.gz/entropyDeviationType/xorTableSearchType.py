
class xorTableSearchType:
	"""
	WARNING: CLASS IS AN ILLUSTRATED EXAMPLE ONLY.

	A class that attempts to find XOR encrypted PE files
	that were encrypted with a single byte key by 
	pre-calculating the possible values of the DOS header magic
	value ('MZ') and the PE header magic ('PE\0\0'). It will
	iterates across a file's data looking for any possible instances
	of the encrypted or plain-text string 'MZ' and if found it will 
	search a customizable offset (defaults to 512 byte) from that 
	string for an encrypted PE header magic that is encrypted with 
	the same key as the DOS header magic value. If found, it will 
	then check the offset within the DOS header that points to the PE
	header magic value and extracts the XOR encrypted value there with 
	the same key as the two magic strings. It then checks to see if 
	this value points to the previously located PE magic string and if 
	so it determines it has found a PE file.

	This is purely a proof of concept class intended to demonstrate 
	that iterating across a file and XOR encrypting every byte is not
	necessary and in turn that attempting to match against variable 
	strings in the DOS stub header which need not be present is faulty.

	There is no reason that this same methodology could not pre-compute
	values for longer keys and practically speaking it could easily 
	extend to the maximum of 4 byte keys (MZ is 2 bytes, PE\0\0 is 4
	and the offset is 4) given enough memory.
	"""	

	def __init__(self, maxoff = 512, base = 10):
		"""
		Takes the parameter 'maxoff' which indicates how far
		after an instance of the string MZ the class should look 
		for the PE header magic value. Defaults to 512, specified in
		base 10 format but is changable via the 'base' parameter
		"""

		if (type(maxoff) == str):
			maxoff = long(maxoff, base)

		self.maxPEOffset 		= maxoff
		self.xorTableSearchType	= edt.xorTableType(self.maxPEOffset)
	
	def openFile(self, name):
		"""
		Opens and reads the file specified by 'name'
		"""

		self.fileName   		= name
		self.fileHand   		= open(self.fileName, 'rb')
		self.data       		= self.fileHand.read()

		self.fileHand.close()
		self.xorTableSearchType.setData(self.data)
	
	def findFirst(self):
		"""
		Attempts to find the first instance of an embedded PE 
		executable within another stream. Returns a native object 
		with the properties 'offset' and 'key' if an encrypted
		PE is found that correlates to the offset that the PE starts 
		at and the key it was encrypted with. Throws a UserWarning() 
		if no executable is found.
		"""

		return self.xorTableSearchType.findFirst()

	def findAll(self):
		"""
		Attempts to find ALL instances of embedded PE files 
		within another stream. Returns a list of native objects 
		with the properties 'offset' and 'key' for each embedded 
		PE that is found. The offset and key refer to the offset 
		within the file that the PE starts at and the key it is 
		encrypted with. Throws a UserWarning() if no executables
		are found.
		"""
		return self.xorTableSearchType.findAll()	
		
