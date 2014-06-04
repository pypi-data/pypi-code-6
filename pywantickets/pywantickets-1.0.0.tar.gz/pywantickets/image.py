from pywantickets import WanticketsModel


class WanticketsImage(WanticketsModel):
	def __init__(self, url=None, type=None):
		self.url = url
		self.type = type