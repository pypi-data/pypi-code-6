import requests
from requests.auth import HTTPBasicAuth
import json

class ComplyAdvantage:

	base_uri = "https://api.complyadvantage.com/v1/"

	def __init__(self, api_key):
		self.auth = HTTPBasicAuth(api_key, 'x')

	def search(self, names):
		response = requests.post(self.base_uri + 'search', data=json.dumps({'names': names}), auth=self.auth, verify=False)
		response.raise_for_status()
		return response.json()