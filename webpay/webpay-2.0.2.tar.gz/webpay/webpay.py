from . import charge, customer, token, event, shop, recursion, account, data_types, error, error_response

import requests
import json
import copy


class WebPay:

    """Main interface of webpay.
    """

    _default_headers = {

        'Content-Type': "application/json",

        'Accept': "application/json",

        'User-Agent': "Apipa-webpay/2.0.2 python",

        'Accept-Language': "en",
    }

    _auth = None

    def __init__(self, auth_token, options={}, **kwargs):
        """Instantiate webpay client

        Attributes:
        - auth_token: Authorization information.
        - `options`: Connection options.
        """
        kwargs.update(options)
        self._options = kwargs
        self._headers = copy.copy(self._default_headers)

        self._headers['Authorization'] = 'Bearer ' + auth_token
        self.charge = charge.Charge(self)
        self.customer = customer.Customer(self)
        self.token = token.Token(self)
        self.event = event.Event(self)
        self.shop = shop.Shop(self)
        self.recursion = recursion.Recursion(self)
        self.account = account.Account(self)

    def set_accept_language(self, value):
        self._headers['Accept-Language'] = value

    def _request(self, method, path, paramData):
        try:
            r = requests.request(method, self._options.get('api_base', 'https://api.webpay.jp/v1') + "/" + path,
                                 params=paramData.query_params(),
                                 data=json.dumps(paramData.request_body()),
                                 headers=self._headers,
                                 auth=self._auth)
        except Exception as exc:
            raise error.in_request(exc)
        return self._process_response(r)

    def _process_response(self, r):
        status = r.status_code
        try:
            data = r.json()
        except Exception as exc:
            raise error.invalid_json(exc, r.text)

        if status >= 200 and status < 300:
            return data
        else:
          if  status == 400 :
              raise error_response.InvalidRequestError(status, data)
          if  status == 401 :
              raise error_response.AuthenticationError(status, data)
          if  status == 402 :
              raise error_response.CardError(status, data)
          if  status == 404 :
              raise error_response.InvalidRequestError(status, data)
          if  True :
              raise error_response.ApiError(status, data)
          raise Exception("Unknown error is returned")
