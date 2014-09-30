# -*- coding: utf-8 -*-

import urllib3
import logging
import json

logging.basicConfig()
LOG = logging.getLogger("LaaS Client")
LOG.setLevel(logging.DEBUG)


class LaaSClient(object):

    def __init__(self, base_url, username, password):
        LOG.info("Initializing new laas client.")
        self.headers = {}
        self.base_url = base_url
        self.username = username
        self.password = password
        self._add_basic_athentication()

    def _add_basic_athentication(self,):
        LOG.info("Setting up authentication.")
        self.headers.update(urllib3.util.make_headers(basic_auth='{}:{}'.format(self.username, self.password)))

    def _add_content_type_json(self,):
        LOG.info("Setting up \"Content-Type\".")
        self.headers.update({'Content-Type': 'application/json'})

    def _make_request(self, http_verb, endpoint, payload=None,):
        LOG.info("Going to make a request.")

        endpoint = self.base_url + endpoint
        http = urllib3.PoolManager()

        LOG.debug("Requesting {} on {}".format(http_verb, endpoint))

        if http_verb == 'GET':
            response = http.request(method=http_verb, url=endpoint, headers=self.headers)
        else:
            self._add_content_type_json()
            response = http.urlopen(method=http_verb, body=payload, url=endpoint, headers=self.headers)

        LOG.debug("Response {}".format(response.data))

        return response

    def update_data(self, endpoint, payload,):
        LOG.info("Updating data.")
        response = self._make_request(http_verb="POST", endpoint=endpoint, payload=payload)

        



    