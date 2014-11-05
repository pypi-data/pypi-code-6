import mimetypes
from poster.encode import MultipartParam

# add mimetypes not present in Python
mimetypes.add_type('image/svg+xml', '.svg')
mimetypes.add_type('application/json', '.json')

class Source(object):
	def __init__(self, **kwargs):
		self.__dict__.update(kwargs)

	@classmethod
	def from_stream(cls, stream, content_type=None, filename=None):
		source = cls(
			stream = stream,
			content_type = content_type,
			filename = filename,
			)
		return source

	def apply(self, data):
		if hasattr(self, 'code'):
			data['code'] = self.code
			return
		if self.filename and not self.content_type:
			self.content_type, _ = mimetypes.guess_type(self.filename)
		if not self.content_type:
			self.content_type = 'application/octet-stream'
		params = dict(
			fileobj = self.stream,
			filetype = self.content_type,
			)
		if self.filename: params.update(filename=self.filename)
		data['file'] = MultipartParam('file', **params)
