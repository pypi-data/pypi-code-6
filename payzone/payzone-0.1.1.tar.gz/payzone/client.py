import json
from requests.auth import HTTPBasicAuth

import requests
from payzone import exceptions


API_BASE = 'https://api.payzone.ma'
PAYMENT_BASE = 'https://paiement.payzone.ma'
PAYMENT_VERSION = '002'


class Customer(object):
    def __init__(self, shopper_id=None, shopper_email=None,
                 ship_to_first_name=None
    ):
        self.shopper_id = shopper_id
        self.shopper_email = shopper_email
        self.ship_to_first_name = ship_to_first_name


class Transaction(object):
    api_base = API_BASE
    endpoint = "/transaction/"
    payment_base = PAYMENT_BASE
    payment_version = PAYMENT_VERSION

    def __init__(self, auth, payment_base=payment_base,
                 payment_version=payment_version):
        self.auth = auth
        self.payment_base = payment_base
        self.payment_version = payment_version

    def _api_post(self, url, **params):
        data = json.dumps(params)
        response = requests.post(url, data=data, auth=self.auth)
        json_response = response.json()

        if not json_response['errorCode'] == '000':
            raise exceptions.PayzoneAPIError(json_response['errorMessage'])
        return json_response

    def _payment_post(self, url, **params):
        data = self._prepare_post_data(**params)
        response = requests.post(url, data=data, auth=self.auth)
        json_response = response.json()

        if json_response['code'] == '401':
            raise exceptions.MissingParameterError(json_response['message'])
        elif not json_response['code'] == '200':
            raise exceptions.PayzoneError(json_response['message'])

        return json_response

    def prepare(self, **params):
        """
        Required fields are:
            * apiVersion
            * customerIP
            * orderID
            * currency
            * amount
            * shippingType : (Physical|Virtual)
            * paymentType
            * ctrlRedirectURL
        """
        url = self.payment_base + self.endpoint + "prepare"
        return self._payment_post(url, **params)

    def capture(self, transaction_id, amount):
        url = self.api_base + self.endpoint + unicode(transaction_id) + "/capture"
        params = {'amount': amount}
        return self._api_post(url, **params)

    def _prepare_post_data(self, **params):
        data = {
            'apiVersion': self.payment_version,
            'currency': 'MAD'
        }
        data.update(params)
        return json.dumps(data)

    def status(self, merchant_token=None, transaction_id=None):
        """
        The two urls returns different responses structure.
        Make sure you pick the right one
        """
        if merchant_token:
            url = self.payment_base + self.endpoint + merchant_token + "/status"
        elif transaction_id:
            url = self.api_base + self.endpoint + str(transaction_id)
        else:
            raise ValueError(
                "You should provide either a merchant_token or a "
                "transaction_id argument"
            )
        return requests.get(url, auth=self.auth).json()

    @classmethod
    def get_dopay_url(cls, customer_token):
        return cls.payment_base + cls.endpoint + customer_token + "/dopay"


class PayZoneClient(object):
    def __init__(self, username, password, payment_base=PAYMENT_BASE,
                 payment_version=PAYMENT_VERSION, api_base=API_BASE):
        self.payment_base = payment_base
        self.payment_version = payment_version
        self.username = username
        self.password = password

    @property
    def transaction(self):
        return Transaction(
            self.auth(),
            payment_base=self.payment_base,
            payment_version=self.payment_version,
        )

    def auth(self):
        return HTTPBasicAuth(self.username, self.password)