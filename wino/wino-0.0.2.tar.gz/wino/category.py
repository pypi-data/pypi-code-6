from base import Base

class Category(Base):
	
    def __init__(self, apikey, response_format):
        Base.__init__(self, apikey, response_format)
        self.url = "/".join((self.ENDPOINT, response_format, "categorymap"))
