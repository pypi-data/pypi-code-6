
from pg_info import PgInfo

class PgPassParser:
	""".pgpass parser"""
	databases = []

	def __init__(self, logger, arguments):
		self.logger = logger
		self.logger.name = self.__class__.__name__
		self.filePath = arguments.getPath()

	def parse(self):
		fileObject = file(self.filePath, 'r')															
		index = 0		
		for line in fileObject:
			if self.isValidData(line):
				pgInfo = PgInfo(self.logger, line)
				pgInfo.parse()
				self.databases.insert(index, pgInfo)
				index = index + 1

	def isValidData(self,data):
		if (data.replace('\n','') == ""):
			return False                
		elif data.startswith('#'):
                        return False
		else:
			return True

	def getDatabases(self):
		return self.databases