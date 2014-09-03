import json


class Mail(object):
	"""
	An object that represents a single email to be sent via Apostle.io

	Arbitrary attributes can be added at runtime and will be sent as
	the 'data' key to Apostle.io
	"""

	# The template slug to be sent
	template_id = None

	# The email address to be sent to
	email = None

	# Any extra data that the template requires
	data = {}

	# Overrides the template's from address
	from_address = None

	# Additional headers to be sent to Apostle.io
	headers = {}

	# Override the default template layout
	layout_id = None

	# The name of the recipient
	name = None

	# Reply To address
	reply_to = None

	# In the event of an error, the message will be stored here
	_error_message = None

	def __init__(self, template_id, options):
		""" Initializes a new Mail object

		:param template_id: The Apostle.io template slug
		:param options: A hash of template data
		"""

		super(Mail, self).__init__()

		# Reset Instance attributes
		self.template_id = None
		self.email = None
		self.data = {}
		self.from_address = None
		self.headers = {}
		self.layout_id = None
		self.name = None
		self.reply_to = None
		self._error_message = None

		self.template_id = template_id

		if options:
			for name, value in options.items():
				self.__setattr__(name, value)

	def __setattr__(self, name, value):
		if hasattr(self, name):
			self.__dict__[name] = value
		else:
			self.data[name] = value

	def set_error(self, message):
		self._error_message = message

	def to_recipient_dict(self):
		recipient_dict = {
			'data': self.data,
			'from': self.from_address,
			'headers': self.headers,
			'layout_id': self.layout_id,
			'name': self.name,
			'reply_to': self.reply_to,
			'template_id': self.template_id
		}
		for key in list(recipient_dict.keys()):
			val = recipient_dict[key]
			if val == None or val == {}:
				del recipient_dict[key]

		return { self.email: recipient_dict }

