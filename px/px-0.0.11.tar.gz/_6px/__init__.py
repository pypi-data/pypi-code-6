import httplib, json, base64, mimetypes, socket

from .output import Output

from urlparse import urlparse

class PX:
	@staticmethod
	def init(user_id, api_key, api_secret):
		"""
		Factory method to create a new 6px request
		"""

		return PX(user_id, api_key, api_secret)

	"""
	Represents a single 6px request
	"""
	def __init__(self, user_id, api_key, api_secret):
		self.user_id = user_id
		self.api_key = api_key
		self.api_secret = api_secret
		self.images = {}
		self.outputs = []
		self.callback = None
		self.url = None

		self.version = '0.0.8'

	def output(self, refs):
		out = Output(refs)
		self.outputs.append(out)

		return out

	def load(self, name, image):
		"""
		Sets our input image
		"""

		self.images[name] = image

		return self


	def callback(self, url):
		"""
		Set a callback URL for whenever the job is done
		"""

		self.callback = url

		return self


	def type(self, mime):
		"""
		Set the destination mimetype of our image
		"""

		self.type = mime

		return self

	def save(self):
		"""
		Make our call to 6px to proess our job
		"""

		inputs = {}
		for key, value in self.images.iteritems():
			inputs[key] = self.parse_input(value)

		outputs = []
		for output in self.outputs:
			outputs.append(output.export())

		data = {
			'input': inputs,
			'output': outputs
		}

		if self.callback is not None:
			data['callback'] = {
				'url': 'http://6px.io'
			}

		response = self.send(json.dumps(data))

		print response

	def parse_input(self, input):
		"""
		Converts our input to a base64 encoded string
		"""

		o = urlparse(input)

		# its a URL and not a file
		if o.scheme:
			return input

		with open(input, "rb") as image:
		    encoded = base64.b64encode(image.read())
		    return 'data:'+ mimetypes.guess_type(input)[0] + ';base64,' + encoded

	def send(self, data):
		"""
		Makes our HTTP request to 6px
		"""

		conn = httplib.HTTPSConnection('api.6px.io')

		conn.request('POST', '/v1/users/'+ self.user_id + '/jobs?key='+ self.api_key + '&secret='+ self.api_secret, data, {
			'Content-Type': 'application/json',
			'User-Agent': '6px Python SDK '+ self.version
		})

		res = conn.getresponse()

		status = res.status
		reason = res.reason

		r = res.read()

		conn.close()

		return r
