from pywantickets import WanticketsModel


class WanticketsPromoter(WanticketsModel):
	def __init__(self, id=None, name=None):
		self.id = id
		self.name = name