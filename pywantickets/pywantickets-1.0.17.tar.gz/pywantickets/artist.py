from pywantickets import WanticketsModel

class WanticketsArtist(WanticketsModel):
    def __init__(self, **kwargs):
	    for p in kwargs:
	        setattr(self, p, kwargs[p])