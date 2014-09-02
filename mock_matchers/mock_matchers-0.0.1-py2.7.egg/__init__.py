class Matchers(object):
	def __getattribute__(self, item):
		import hamcrest
		if hasattr(hamcrest, item):
			thing = getattr(hamcrest, item)
			if callable(thing):
				return self._wrap(getattr(hamcrest, item))
			return thing
		return object.__getattribute__(self, item)

	def _wrap(self, obj):
		from functools import wraps
		from hamcrest.core.base_matcher import BaseMatcher
		@wraps(obj)
		def __inner(*a, **kwargs):
			resp = obj(*a, **kwargs)
			if isinstance(resp, BaseMatcher):
				meth = lambda s, o: s.matches(o)
				resp.__class__.__eq__ = meth
			return resp
		return __inner

import sys
sys.modules["mock_matchers"] = Matchers()
