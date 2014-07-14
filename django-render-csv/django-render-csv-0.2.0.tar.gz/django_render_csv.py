import csv, codecs, cStringIO
from django.http import HttpResponse


class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


def render_csv(data, filename="data.csv"):
	res = HttpResponse(content_type='text/csv')
	res['Content-Disposition'] = 'attachment; filename="%s"' % filename

	writer = UnicodeWriter(res)
	for item in data:
		writer.writerow(item)

	return res


def as_csv(fn=None, filename=None):
	def decorator(fn):
		def _fn(request, *args, **kwargs):
			data = fn(request, *args, **kwargs)
			return render_csv(data, filename=filename)

		return _fn

	return decorator(fn) if fn else decorator

