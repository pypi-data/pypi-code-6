"""
    token.py

    The Public API for which you are requesting a token.

    :copyright: (c) Heartland Payment Systems. All rights reserved.
"""

import jsonpickle
import requests
from securesubmit.entities.credit import HpsCreditCard
from securesubmit.serialization import HpsToken


class HpsTokenService(object):
    """The Public API for which you are requesting a token."""

    _public_api_key = None
    _url = None

    def __init__(self, public_api_key):
        self._public_api_key = public_api_key

        if public_api_key is None or public_api_key == "":
            raise TypeError("publicAPIKey")

        components = public_api_key.split("_")
        if len(components) != 3:
            raise TypeError("Public API Key must contain three underscores.",
                            "publicAPIKey")

        env = components[1].lower()
        if env == "prod":
            self._url = (
                "https://api.heartlandportico.com/SecureSubmit.v1/api/token")
        else:
            self._url = (
                "https://posgateway.cert.secureexchange.net/"
                "Hps.Exchange.PosGateway.Hpf.v1/api/token")

    def get_token(self, card_data):
        """Get a token for a given credit card."""
        try:
            data = jsonpickle.encode(HpsToken(card_data), False, False, True)
            data = data.replace("[", "").replace("]", "")

            headers = {'content-type': 'application/json'}
            response = requests.post(self._url,
                                     data=data,
                                     headers=headers,
                                     auth=(self._public_api_key, None))

            token = HpsToken()
            if len(response.content) > 0:
                token = HpsToken.from_dict(jsonpickle.decode(response.content))

            return token
        except Exception, e:
            raise e