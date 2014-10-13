'''
	File class simply reads text of a given file.
'''

class File:
	def __init__(self, name):
		self.name = name
	def read(self):
		with file(self.name,'r') as f:
			return f.read()
	