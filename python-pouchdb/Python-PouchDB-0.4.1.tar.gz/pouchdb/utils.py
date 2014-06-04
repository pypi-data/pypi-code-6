import contextlib

@contextlib.contextmanager
def suppress(*e):
	try:
		yield
	except e:
		pass

class AttrAccessDict(dict):
	def __getattr__(self, key):
		try:
			return super(AttrAccessDict, self).__getattr__(key)
		except AttributeError:
			try:
				return self[key]
			except KeyError, e:
				raise AttributeError(e)
