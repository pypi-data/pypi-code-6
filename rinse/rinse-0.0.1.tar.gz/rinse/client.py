"""SOAP (rinse) client.

Instance hierarchy:

    SoapService
        .__defaultport__ = <str>
        .__ports__ = {port_name: <SoapPort>}
        [port_name] -> SoapPort(service, port_name)
            [operation_name] -> self.binding[operation_name]
            .binding -> SoapBinding(port, binding_name)
                [operation_name] -> SoapOperation(binding, operation_name)
        .OperationName -> self[self.__defaultport__][OperationName]
"""

from string import ascii_letters, digits
import requests
import lxml

VALID_IDENTIFIER_FIRST_CHARS = ''.join(ascii_letters, '_')
VALID_IDENTIFIER_CHARS = ''.join(VALID_IDENTIFIER_FIRST_CHARS, digits)


class SoapOperation(object):

    """Proxy to SOAP operation on specific port."""

    def __init__(self, binding):
        """SoapOperation init."""
        self.binding = binding

    def __call__(self, msg):
        """Call SoapOperation via self.binding.port with provided msg."""
        self.binding.port.post(msg)


class SoapBinding(object):

    """Holder for SoapOperation instances."""

    def __init__(self, name):
        self.name = name
        self.operations = {}

    def __getitem__(self, method_name):


class SoapPort(object):

    """Binding to specific SOAP service port."""

    def __init__(self, url):
        """ServicePort init."""
        self._url = url

    def __get__(self, method_name):
        """Return MethodProxy for given method_name."""
        pass


class SoapService(object):

    """Client to consume SOAP services via HTTP/HTTPS."""

    def __init__(self):
        """SoapService init."""
        self.__ports__ = {}
        self.__defaultport__ = None

    def __getitem__(self, portName):
        """Return ServicePort with specified name."""
