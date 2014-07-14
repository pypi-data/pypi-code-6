import csv, codecs, cStringIO
from django.http import HttpResponse
from django.utils.encoding import smart_text


def render_csv(data, filename="data.csv"):
	res = HttpResponse(content_type='text/csv')
	res['Content-Disposition'] = 'attachment; filename="%s"' % filename

	writer = csv.writer(res)
	for item in data:
		writer.writerow(smart_text(item).encode('utf-8')

	return res


def as_csv(fn=None, filename=None):
	def decorator(fn):
		def _fn(request, *args, **kwargs):
			data = fn(request, *args, **kwargs)
			return render_csv(data, filename=filename)

		return _fn

	return decorator(fn) if fn else decorator

