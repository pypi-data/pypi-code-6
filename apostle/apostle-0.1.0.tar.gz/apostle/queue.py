import json

import requests

import apostle
from apostle import exceptions

class Queue(object):
	def __init__(self):
		""" Initializes a new Queue.
        """

		super(Queue, self).__init__()

		self.emails = []

	def add(self, mail):
		""" Adds a mail object to the queue
		:param mail: an Apostle mail object to add to the queue
		"""

		self.emails.append(mail)

	def deliver(self):
		if not apostle.domain_key:
			raise exceptions.UnauthorizedError(
                "Apostle.io requires a Domain Key to function"
                "Please set apostle.domain_key appropriately "
                "apostle.domain_key = 'your_domain_key'"
            )

		results = { "valid": [], "invalid": []}
		payload = { "recipients": {} }

		for mail in self.emails:
			if mail.template_id == None:
				results["invalid"].append(mail)
				mail.set_error("No template id provided")
				next

			if mail.email == None:
				results["invalid"].append(mail)
				mail.set_error("No email address provided")
				next

			results["valid"].append(mail)
			payload["recipients"].update(mail.to_recipient_dict())

		if len(results["invalid"]) > 0:
			raise exceptions.ValidationError(
				"Invalid Emails: {0}".format(len(results["invalid"]))
			)


		headers = {
			"Apostle-Client": "Python/{0}".format(apostle.__version__),
			"Authorization": "Bearer {0}".format(apostle.domain_key),
			"Content-Type": "application/json"
		}
		response = requests.post(apostle.delivery_host, data=json.dumps(payload), headers=headers)

		if response.status_code >= 200 and response.status_code < 300:
			return True
		elif response.status_code == 401:
			raise exceptions.UnauthorizedError("Domain Key invalid")
		elif response.status_code == 403:
			raise exceptions.ForbiddenError("Domain Key does not have permission to do that")
		elif response.status_code == 422:
			raise exceptions.UnprocessableEntityError("Required values were not provided")
		elif response.status_code >= 500:
			raise exceptions.ServerError("An external server error occured")
		else:
			raise exceptions.DeliveryError("A delivery error occured")

