# -*- coding: utf-8 -*-
"""
python client for www.checkmy.ws
"""

import requests
import logging
import json

from checkmyws.exception import CheckmywsError

BASE_URL = "http://api.checkmy.ws/api/"


class CheckmywsClient(object):

    def __init__(self):
        self.logger = logging.getLogger("CheckmywsClient")
        self.logger.debug("Initialize")

        self.session = requests.Session()

    def request(self, path, method="GET", params=None, data=None,
                status_code=200):
            """
            Make a http request to API
            """
            url = "{0}/{1}".format(BASE_URL, path)

            if params is None:
                params = {}

            if data is not None and not isinstance(data, str):
                data = json.dumps(data)

            response = self.session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                verify=False
            )

            if response.status_code == status_code:
                return response
            else:
                raise CheckmywsError(response)

    def status(self, check_id):
        path = "/status/{0}".format(check_id)
        response = self.request(path=path, method="GET")

        return response.json()
