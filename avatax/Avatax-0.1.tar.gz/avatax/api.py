# -*- coding: utf-8 -*-
"""
    api

    API for Avatax

    :copyright: © 2013 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
import json

import requests


DEVELOPMENT_URL = 'https://development.avalara.net'
PRODUCTION_URL = 'https://rest.avalara.net'


class AvataxError(Exception):

    def __init__(self, errors):
        """
        Custom exception to capture

        :param errors: List of dictionary of errors as sent by Avatax
        """
        def build_message_from_error(error):
            message = error.get('Severity', 'Error')
            message += " %s" % error.get('Summary', '')
            if 'Details' in error:
                message += "\n\n%s" % error.get('Details', '')
            return message

        message = '\n'.join(
            [build_message_from_error(error) for error in errors]
        )
        super(Exception, self).__init__(message)


class BaseAPI(object):
    """
    Base API

    :param account_number: This is the account number that needs to be used
                           to authenticate your API call (this is not an
                           Admin Console login). It will be a ten-digit number
                           (e.g. 1100012345)
    :param license_key: This is the license key that needs to be set in the
                        credentials portion of your connector (this is not an
                        Admin Console Password). It will be a 13-character
                        string (e.g. 1A2BC3D4E5F6G7).
    :param url: The URL for the avatax service. If left None, it defaults to
                the development URL. The URL itself is captured instead of a
                flag to choose between development and production URL, since
                avatax requires the application configuration to allow users
                to set the service URL. For convenience, the DEVELOPMENT_URL
                and PRODUCTION_URL are made available as module globals and
                convenience methods :meth:`set_production_url` and
                :meth:`set_development_url` are provided,
    """
    api_version = "1.0"

    def __init__(self, account_number, license_key, url=None):
        self.account_number = account_number
        self.license_key = license_key
        self.url = url or DEVELOPMENT_URL

        if self.url.endswith('/'):
            raise Exception("The URL must not end with '/'")

    def set_production_url(self):
        """
        Sets the URL to use as the production URL
        """
        self.url = PRODUCTION_URL

    def set_development_url(self):
        """
        Sets the URL to use as the developer URL
        """
        self.url = DEVELOPMENT_URL

    def send_request(self, resource, params, method="GET"):
        """
        Send a request to the Avalara web service and return the JSON in the
        response

        :param resource: The Resource URI Component
        :param params: Parameters of data to be sent to avalara
        :param method: "GET" or "POST"
        """
        url = "%s/%s/%s" % (self.url, self.api_version, resource)
        auth = (self.account_number, self.license_key)
        if method == "POST":
            response = requests.post(url, data=json.dumps(params), auth=auth)
        elif method == "GET":
            response = requests.get(url, params=params, auth=auth)

        if response.status_code == requests.codes.ok:
            return response.json()
        else:
            raise AvataxError(response.json()['Messages'])

    def test_connection(self):
        """
        Test the connection settings.

        The SOAP API seems to have a PING method while the REST api
        does not. This may mean that there should be a workaround to
        test the connection.
        """
        address = dict(
            Line1 = '1706 Biscayne Blvd',
            Line2 = '',
            City = 'Miami',
            PostalCode = '33137',
            Region = 'Florida',
            Country = 'USA',
        )
        response = self.get('address/validate', address)
        if 'Address' in response:
            return True
        return False

    def post(self, *args, **kwargs):
        """
        A convenience method that sends a POST request to avalara
        """
        kwargs['method'] = "POST"
        return self.send_request(*args, **kwargs)

    def get(self, *args, **kwargs):
        """
        A convenience method that sends a GET request to avalara
        """
        kwargs['method'] = "GET"
        return self.send_request(*args, **kwargs)


class API(BaseAPI):
    """
    API to Access AvaTax API
    """

    def address_validate(self, **kwargs):
        """
        This operation validates the supplied address, returning canonical
        form and additional delivery details if successfully validated.

        While `Line1` (Address Line 1) is mandatory, other elements are
        optionally required as explained in the address validation
        `documentation <http://developer.avalara.com/api-docs/rest/resources/address-validation/>`_

        Optional Kwargs:

            * `Line1`: Address line 1
            * `Line2`: Address line 2
            * `Line3`: Address line 3
            * `City`: City name (Required when `PostalCode` is not specified.)
            * `Region`: State, province, or region name (Required when
                        `PostalCode` is not specified.)
            * `Country`: Country Code
            * `PostalCode`: Postal or ZIP code (Required when City & Region are
                            not specified)

        No validation is done by the API client and validations are done at the
        end of avalara.
        """
        return self.get('address/validate', kwargs)['Address']

    def tax_get(self, latitude, longitude, sale_amount):
        """
        This operation uses the tax resource to return rate or tax amount
        details based on (at minimum) a geographic location and sale amount.

        More details about the arguments to be sent to this API call can be
        obtained from `Avatax documentation
        <http://developer.avalara.com/api-docs/rest/resources/tax/get/ver-get/>`_

        :param latitude: The latitude of the geographic coordinates to get
                         tax for based on the sale amount
        :param longitude: The longitude of the geographic coordinates to get
                          tax for based on the sale amount
        :param sale_amount: the amount of sale requiring tax calculation, in
                            decimal format
        """
        return self.get(
            'tax/%s,%s/get' % (latitude, longitude),
            {'saleamount': sale_amount}
        )

    def tax_get_detailed(self, **kwargs):
        """
        This operation uses the POST request method with the tax resource to
        return tax rate details for the supplied transactional information,
        including both document header and document line detail.

        Note that GET is also a supported request method, but results in a
        different kind of tax calculation, covered in :meth:`tax_get`.

        More details about the arguments to be sent to this API call can be
        obtained from `Avatax documentation
        <http://developer.avalara.com/api-docs/rest/resources/tax/get/ver-post/>`_
        """
        return self.post('tax/get', kwargs)
