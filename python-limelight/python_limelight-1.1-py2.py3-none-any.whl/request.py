# -*- coding: utf-8 -*-

from copy import copy

try:
    # noinspection PyCompatibility
    from urllib.parse import parse_qs
except ImportError:
    # noinspection PyUnresolvedReferences,PyCompatibility
    from urlparse import parse_qs

from requests import post, get, ConnectionError, Timeout
from requests.packages.urllib3.exceptions import ProtocolError

from voluptuous import Schema, MultipleInvalid

from . import utils, errors


class Request(object):
    """
    The superclass of all Lime Light API methods.
    """
    TIMEOUT = 12
    MAX_TRIES = 3
    VERIFY_CERT = True
    preserve_field_labels = None
    http_method = 'POST'
    schema = utils.not_implemented
    endpoint = utils.not_implemented
    error = utils.not_implemented
    handle_errors = utils.func_not_implemented

    def __init__(self, host=None, username=None, password=None, **kwargs):
        self.host = host
        self.username = username
        self.password = password
        try:
            cleaned_data = Schema(self.schema)(kwargs)
        except MultipleInvalid as e:
            raise errors.ValidationError(e)
        self.response = self.__make_request(cleaned_data)
        self.__process_response()
        self.__handle_errors()

    def __preprocess_data(self, unprocessed_data):
        """
        :param unprocessed_data: Data that is about to be send to Lime Light
        :type unprocessed_data: dict
        :return: Data ready to be transmitted
        :rtype: dict
        """
        if unprocessed_data.get('tran_type') and unprocessed_data.get('cvv'):
            unprocessed_data['CVV'] = unprocessed_data.pop('cvv')
        if self.preserve_field_labels is not None:
            data = {}
            for key, value in unprocessed_data.items():
                if key in self.preserve_field_labels:
                    data[key] = value
                else:
                    data[utils.to_camel_case(key)] = value
        else:
            data = copy(unprocessed_data)
        data.update(method=self.__name__,
                    username=self.username,
                    password=self.password)
        return data

    def __make_request(self, request_data, tried=0):
        """
        :param request_data: Data being sent over to Lime Light
        :type request_data: dict
        :param tried: The number of times the request has been tried so far. By default,
                      ``__make_request`` will attempt a request three times before giving up
        :type tried: int
        :return: Lime Light's response
        :rtype: requests.Response
        :raises: limelight.errors.ConnectionError
        """
        data = self.__preprocess_data(request_data)
        try:
            if self.http_method.upper() == 'POST':
                return post(self.endpoint, data=data, timeout=self.TIMEOUT, verify=self.VERIFY_CERT)
            elif self.http_method.upper() == 'GET':
                return get(self.endpoint, params=data, timeout=self.TIMEOUT,
                           verify=self.VERIFY_CERT)
            else:
                msg = '`{cls}.http_method` must be one of `GET` or `POST`'.format(cls=self.__name__)
                raise errors.ImproperlyConfigured(msg)
        except (Timeout, ConnectionError, ProtocolError) as e:
            if tried <= self.MAX_TRIES:
                return self.__make_request(request_data, tried=tried + 1)
            else:
                raise errors.ConnectionError(e)

    def __process_response(self):
        """
        :rtype: None
        """
        try:
            response_data = self.response.json()
        except ValueError:
            response_data = parse_qs(self.response.text)
        for key, value in response_data.items():
            setattr(self, utils.to_underscore(key), utils.to_python(value))

    # noinspection PyUnresolvedReferences
    def __handle_errors(self):
        """Handles generic Lime Light errors"""
        try:
            self.handle_errors()
        except (AttributeError, NotImplementedError):
            if self.error_found:
                response_code = getattr(self, 'response_code', '000')
                error_message = getattr(self, 'error_message',
                                        'An unspecified error occurred, try again.')
                raise errors.LimeLightException("{code}: {message}".format(code=response_code,
                                                                           message=error_message))


class TransactionMethod(Request):
    """
    Superclass of all Transaction API methods
    """
    Declined = errors.TransactionDeclined
    preserve_field_labels = {'click_id', 'preserve_force_gateway', 'thm_session_id',
                             'total_installments', 'alt_pay_token', 'alt_pay_payer_id',
                             'force_subscription_cycle', 'recurring_days', 'subscription_week',
                             'subscription_day', 'master_order_id', 'temp_customer_id',
                             'auth_amount', 'cascade_enabled', 'save_customer', }

    def __init__(self, **kwargs):
        if self.__name__ != 'NewProspect':
            kwargs['tran_type'] = 'Sale'
        super(TransactionMethod, self).__init__(**kwargs)

    # noinspection PyUnresolvedReferences
    def handle_errors(self):
        """
        Raises exceptions for Transaction API-related errors.

        :return:
        """
        if self.error_found:
            if self.response_code == 800:
                raise self.Declined(self.decline_reason)
            else:
                pass

    @property
    def endpoint(self):
        """
        :return: API endpoint
        :rtype: str
        """
        return "https://{host}/admin/transact.php".format(host=self.host)


class MembershipMethod(Request):
    """
    Superclass of all Membership API methods
    """
    @property
    def endpoint(self):
        """
        :return: API endpoint
        :rtype: str
        """
        return "https://{host}/admin/membership.php".format(host=self.host)