from base import Base

class Category(Base):
	
	def __init__(self, apikey):
		Base.__init__(self, apikey)
		self.url = "/".join((self.ENDPOINT, "categorymap"))