class PgInfo:
	"""pg connection details"""
	delimiter=":"

	def __init__(self, logger, rawInfo):
		self.logger = logger
		self.rawInfo = rawInfo
		self.logger.name = self.__class__.__name__

	def parse(self):
		data = self.rawInfo.replace('\n','').split(self.delimiter)
		self.logger.debug(data)
		self.host = data[0]
		self.port = data[1]
		self.dbname = data[2]
		self.username = data[3]
		self.password = data[4]

	def getName(self):
		return self.host+self.delimiter+self.port+self.delimiter+self.dbname+self.delimiter+self.username

	def getExecuteCommand(self):
		return "psql -h "+ self.host +" " + self.dbname + " -U " + self.username + " -p " + self.port