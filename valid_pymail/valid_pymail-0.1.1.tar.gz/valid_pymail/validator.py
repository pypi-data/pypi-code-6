#!/usr/bin/python

"""
python-mailgun-validator

A small pure Python wrapper for the Mailgun email validator API
(http://documentation.mailgun.com/api-email-validation.html#email-validation)
"""

import requests

__author__ = "Michael Malocha <https://github.com/mjm159>"
__version__ = "0.1"


class MailgunAPIException(Exception):
    pass


class MailgunEmailValidator:
    def __init__(self, api_key):
        """
        Parameters:
            api_key: String with your Mailgun public API that authenticates your requests
                e.g.: 'pubkey-1a2b3d4e5f67d8dc8a76c1bee5e1ef9c'
        """
        self.base_url = "https://api.mailgun.net/v2/address/validate"
        self.api_key = api_key

    def validate_email(self, address):
        """
        Validates an email address

        Parameters:
            address: String with an email address to be validated

        Returns:
            dict: Response in json format
        """
        response = requests.get(self.base_url, auth=('api', self.api_key), params={"address": address})
        json_results = response.json()
        if response.ok:
            return json_results
        else:
            raise MailgunAPIException("[{}] {}".format(response.status_code, json_results['message']))
