"""
    infrastructure.py

    enums, exceptions and validations

    :copyright: (c) Heartland Payment Systems. All rights reserved.
"""

from enum import Enum
from ConfigParser import ConfigParser


class HpsException(Exception):
    def __init__(self, message, inner_exception=None):
        self.message = message
        self.inner_exception = inner_exception


class HpsAuthenticationException(HpsException):
    code = None

    def __init__(self, sdk_code, message):
        self.code = sdk_code
        return super(HpsAuthenticationException, self).__init__(message)


class HpsCheckException(Exception):
    transaction_id = None
    code = None
    details = None

    def __init__(self, transaction_id, details, code, message):
        self.transaction_id = transaction_id
        self.details = details
        self.code = code
        self.message = message


class HpsConfiguration(object):
    secret_api_key = None
    license_id = -1
    site_id = -1
    device_id = -1
    version_number = None
    username = None
    password = None
    developer_id = None
    site_trace = None
    soap_service_uri = None

    def __init__(self):
        self.soap_service_uri = ('https://posgateway.cert.secureexchange.net'
                                 '/Hps.Exchange.PosGateway'
                                 '/PosGatewayService.asmx?wsdl')

        filename = './config.cfg'
        parser = ConfigParser()
        if parser.read(filename) == [filename]:
            try:
                self.secret_api_key = parser.get('Settings', 'secretApiKey')
                self.license_id = parser.get('Settings', 'licenseId')
                self.site_id = parser.get('Settings', 'siteId')
                self.device_id = parser.get('Settings', 'deviceId')
                self.username = parser.get('Settings', 'userName')
                self.password = parser.get('Settings', 'password')
                self.site_trace = parser.get('Settings', 'siteTrace')
                self.developer_id = parser.get('Settings', 'developerId')
                self.version_number = parser.get('Settings', 'versionNbr')
                self.soap_service_uri = parser.get('Settings', 'URL')
            except NoOptionError:
                raise Exception('Could not read config file.')


class HpsCreditException(HpsException):
    transaction_id = None
    code = None
    details = None

    def __init__(self, transaction_id, code, message,
                 issuer_code=None, issuer_message=None,
                 inner_exception=None):
        self.transaction_id = transaction_id
        self.code = code

        if issuer_code is not None and issuer_message is not None:
            details = HpsCreditExceptionDetails()
            details.issuer_response_code = issuer_code
            details.issuer_response_text = issuer_message
            HpsException.__init__(self, message, inner_exception)


class HpsCreditExceptionDetails(object):
    issuer_response_code = None
    issuer_response_text = None


class HpsGatewayException(HpsException):
    code = None
    details = None

    def __init__(
            self, code, message,
            gateway_response_code=None,
            gateway_response_message=None,
            inner_exception=None):
        self.code = code

        if (gateway_response_code is not None or
                gateway_response_message is not None):
            details = HpsGatewayExceptionDetails()
            details.gateway_response_code = gateway_response_code
            details.gateway_response_message = gateway_response_message

        return super(
            HpsGatewayException,
            self).__init__(message, inner_exception)


class HpsGatewayExceptionDetails(object):
    gateway_response_code = None
    gateway_response_message = None


class HpsInvalidRequestException(HpsException):
    code = None
    param_name = None

    def __init__(self, code, message, param_name=None):
        self.code = code
        self.param_name = param_name
        HpsException.__init__(self, message)