import requests
from requests.auth import HTTPBasicAuth
import json

class Stelapoint:

	base_uri = "https://api.stelapoint.com/v1/"

	def __init__(self, api_key):
		self.auth = HTTPBasicAuth(api_key, 'x')

	def search(self, names):
		response = requests.post(self.base_uri + 'search', data=json.dumps(names), auth=self.auth)
		response.raise_for_status()
		return response.json()