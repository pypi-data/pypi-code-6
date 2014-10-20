class Storage(dict):
	__setattr__ = dict.__setitem__
	__getattr__ = dict.__getitem__
	__delattr__ = dict.__delitem__
	__getitem__ = dict.get
	__getattr__ = dict.get
	__copy__ = lambda self: Storage(self) 