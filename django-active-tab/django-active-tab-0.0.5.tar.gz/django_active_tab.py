import sys

def active_tab(tab, sub_tab=None):
	from functools import wraps
	
	def outer_wrapper(func):
		@wraps(func)
		def wrapper(request):
			request.nav = request.nav if hasattr(request, "nav") else {}
			request.nav["tab"] = tab
			if sub_tab is not None:
				request.nav["sub_tab"] = sub_tab
			return func(request)
		return wrapper

	return outer_wrapper

sys.modules[__name__] = active_tab
