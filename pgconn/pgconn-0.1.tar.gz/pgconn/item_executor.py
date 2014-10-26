import os

class ItemExecutor:
	"""Item Executor"""
		
	def __init__(self, logger, items, selection):
		self.logger = logger
		self.logger.name = self.__class__.__name__
		self.selection = selection
		self.items = items

	def execute(self):
		if self.selection != "q":
			self.logger.debug(self.getItem().getExecuteCommand())
			os.system(self.getItem().getExecuteCommand())

	def getItem(self):
		return self.items[int(self.selection)-1]