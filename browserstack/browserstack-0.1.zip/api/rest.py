import requests, json
from requests.auth import HTTPBasicAuth


class REST():
	endpoint = ""
	username = ""
	access_key = ""


	def __init__(self, endpoint, username, access_key):
		self.endpoint = endpoint
		self.username = username
		self.access_key = access_key


	def query(self, resource):
		r = requests.get(self.endpoint + resource, auth = HTTPBasicAuth(self.username, self.access_key))
		if r.status_code/100 == 2:
			return r.text

		print r.text
		raise Exception('REST API GET Error')


	def create(self, resource, data):
		r = requests.post(self.endpoint + resource, data=json.dumps(data), auth = HTTPBasicAuth(self.username, self.access_key), headers = {'Content-type': 'application/json', 'Accept': 'text/plain'})
		if r.status_code/100 == 2:
			return r.text

		print r.text
		raise Exception('REST API POST Error')


	def update(self, resource, data):
		r = requests.put(self.endpoint + resource, data=json.dumps(data), auth = HTTPBasicAuth(self.username, self.access_key), headers = {'Content-type': 'application/json', 'Accept': 'text/plain'})
		if r.status_code/100 == 2:
			return r.text

		print r.text
		raise Exception('REST API PUT Error')


	def delete(self, resource):
		r = requests.delete(self.endpoint + resource, auth = HTTPBasicAuth(self.username, self.access_key))
		if r.status_code/100 == 2:
			return r.text

		print r.text
		raise Exception('REST API DELETE Error')

