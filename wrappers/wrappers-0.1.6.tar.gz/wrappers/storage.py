class Storage(dict):
	__setattr__ = __setitem__
	__getattr__ = __getitem__