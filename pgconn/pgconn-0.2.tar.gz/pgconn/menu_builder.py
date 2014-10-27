class MenuBuilder:
	"""Menu builder"""
	menu=""
	selection=None

	def __init__(self, logger, items):
		self.logger = logger
		self.logger.name = self.__class__.__name__
		self.items = items

	def display(self):
		index = 1
		self.menu = "Please select a connection:\n"
		for item in self.items:
			self.menu += str(index) + ") " + item.getName() + "\n"
			index+=1

		self.menu += "q) Quit." + "\n"
		self.menu += "Your selection: "
		self.selection = raw_input(self.menu)

	def getSelection(self):
		return self.selection