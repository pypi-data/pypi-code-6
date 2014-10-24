#coding:utf-8
import datetime
import base64
import hmac
import hashlib
import logging
from xml.parsers import expat

import xmltodict
from geventhttpclient import HTTPClient
from geventhttpclient.url import URL
from scalr_client_core import constant
from scalr_client_core import exception
from scalr_client_core import util


logger = logging.getLogger(__name__)


class APIClient(object):
    def __init__(self, api_url, key_id, key_secret, env_id):
        self.api_url = api_url
        self.api_key = key_id
        self.api_secret = key_secret
        self.environment_id = env_id

    def _request(self, url):
        logger.info("Making API Call to: '%s'", url)
        http = HTTPClient.from_url(url)
        response = http.get(url.request_uri)

        code = response.status_code
        body = response.read()

        http.close()
        logger.info("Response status for '%s': '%s'", url, code)

        return code, body

    def _create_signature(self, api_method, timestamp):
        h = hmac.new(self.api_secret, ":".join([api_method, self.api_key, timestamp]), hashlib.sha256).digest()
        return base64.b64encode(h)

    def _call(self, api_method, api_call_data):
        timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        params = {
            "Action": api_method,
            "EnvID": self.environment_id,
            "Version": constant.API_VERSION,
            "AuthVersion": constant.API_AUTH_VERSION,
            "Timestamp": timestamp,
            "KeyID": self.api_key,
            "Signature": self._create_signature(api_method, timestamp)
        }
        params.update(api_call_data)

        url = URL(self.api_url)

        for k, v in params.items():
            url[k] = v

        return self._request(url)

    def call(self, api_method, api_call_data=None):
        if api_call_data is None:
            api_call_data = {}

        code, body = self._call(api_method, api_call_data)

        if code != 200:
            raise exception.APIError("Received HTTP error. HTTP '{0}': '{1}'".format(code, body))

        try:
            parsed = xmltodict.parse(body)
        except expat.ExpatError:
            raise exception.APIError("Received invalid XML:\n'''{0}'''".format(body))

        if parsed.get("Error") is not None:
            raise exception.APIError("Received API error: '{0}'".format(parsed.get("Error", {}).get("Message", "")))

        try:
            out = parsed["{0}Response".format(api_method)]
        except KeyError:
            raise exception.APIError("Unexpected structure: '{0}'".format(body))

        util.unpack_sets(out)
        return out

