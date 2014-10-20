import time

__doc__ = """
simple class for measuring elapsed time.
just instantiate c = Clock() and keep calling c.elapsed() or c.split() to get the elapsed time since instantiation. 
"""

class Clock:
	def __init__(self):
		self._start = time.time()
	def elapsed(self):
		return time.time() - self._start
	split = elapsed
