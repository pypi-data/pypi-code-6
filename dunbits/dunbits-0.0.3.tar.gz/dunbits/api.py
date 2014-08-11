import os
import json
import requests

DEFAULT_API_URL = "http://checkout.dunbits.com/api/"
API_URL = os.getenv("DUNBITS_API_URL", DEFAULT_API_URL)


class Api(object):
    base_url = API_URL

    def __init__(self, key=None):
        self.key = key

    def _get_headers(self):
        headers = {
            'content-type': 'application/json',
        }
        if self.key:
            headers['Authorization'] = 'Token ' + self.key
        return headers

    def _get_url(self, token=None, used=False):
        if token:
            url = self.base_url + "token/" + token
            if used:
                url = url + "/used/"
        else:
            url = self.base_url + "token/"
        return url

    def create_token(self, widget, content):
        headers = self._get_headers()
        url = self._get_url()
        data = {
            "content_code": content,
            "widget": widget
        }
        resp = requests.post(url, data=json.dumps(data), headers=headers)
        if resp.status_code == 201:
            return resp.json()
        else:
            return None

    def create_token_get(self, widget, content):
        headers = self._get_headers()
        url = self._get_url()
        data = {
            "content_code": content,
            "widget": widget
        }
        resp = requests.get(url, params=data, headers=headers)
        if resp.status_code == 201:
            return resp.json()
        else:
            return None

    def get_token(self, token):
        headers = self._get_headers()
        url = self._get_url(token)
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            return resp.json()
        else:
            return None

    def use_token(self, token):
        headers = self._get_headers()
        url = self._get_url(token, used=True)
        resp = requests.post(url, data=json.dumps({}), headers=headers)
        if resp.status_code == 200:
            return json.loads(resp.content)
        else:
            return None
