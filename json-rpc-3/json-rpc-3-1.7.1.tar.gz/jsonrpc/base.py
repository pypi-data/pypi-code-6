from abc import ABCMeta, abstractmethod

from .utils import JSONSerializable


class JSONRPCBaseRequest(JSONSerializable, metaclass=ABCMeta):
    """ Base class for JSON-RPC 2.0 requests."""

    def __init__(self, method=None, params=None, _id=None, is_notification=None):
        """
        :param method: A String containing the name of the method to be
            invoked. Method names that begin with the word rpc followed by a
            period character (U+002E or ASCII 46) are reserved for rpc-internal
            methods and extensions and MUST NOT be used for anything else.
        :type method: str

        :param params: A Structured value that holds the parameter values to be
            used during the invocation of the method. This member MAY be omitted.
        :type params: iterable or dict

        :param _id: An identifier established by the Client that MUST contain a
            String, Number, or NULL value if included. If it is not included it is
            assumed to be a notification. The value SHOULD normally not be Null
            [1] and Numbers SHOULD NOT contain fractional parts [2].
        :type _id: str or int or None

        :param is_notification: Whether request is notification or not. If
            value is True, _id is not included to request. It allows to create
            requests with id = null.
        :type is_notification: bool
        The Server MUST reply with the same value in the Response object if
        included. This member is used to correlate the context between the two
        objects.

        [1] The use of Null as a value for the id member in a Request object is
        discouraged, because this specification uses a value of Null for Responses
        with an unknown id. Also, because JSON-RPC 1.0 uses an id value of Null
        for Notifications this could cause confusion in handling.

        [2] Fractional parts may be problematic, since many decimal fractions
        cannot be represented exactly as binary fractions.

        """
        self._data = {}
        self.method = method
        self.params = params
        self._id = _id
        self.is_notification = is_notification

    @property
    @abstractmethod
    def data(self):
        return self._data

    @data.setter
    @abstractmethod
    def data(self, value):
        pass

    @property
    def args(self):
        """ Method position arguments.

        :return: method position arguments.
        :rtype: tuple
        """
        return tuple(self.params) if isinstance(self.params, list) else ()

    @property
    def kwargs(self):
        """ Method named arguments.

        :return: method named arguments.
        :rtype: dict
        """
        return self.params if isinstance(self.params, dict) else {}

    @property
    def json(self):
        return self.serialize(self.data)


class JSONRPCBaseResponse(JSONSerializable, metaclass=ABCMeta):
    """ Base class for JSON-RPC 2.0 responses."""

    def __init__(self, result=None, error=None, _id=None):
        """
        When a rpc call is made, the Server MUST reply with a Response, except for
        in the case of Notifications. The Response is expressed as a single JSON
        Object, with the following members:

        :param jsonrpc: A String specifying the version of the JSON-RPC
            protocol. MUST be exactly "2.0".
        :type jsonrpc: str

        :param result: This member is REQUIRED on success.
            This member MUST NOT exist if there was an error invoking the method.
            The value of this member is determined by the method invoked on the
            Server.

        :param error: This member is REQUIRED on error.
            This member MUST NOT exist if there was no error triggered during
            invocation. The value for this member MUST be an Object.
        :type error: dict

        :param id: This member is REQUIRED.
            It MUST be the same as the value of the id member in the Request
            Object. If there was an error in detecting the id in the Request
            object (e.g. Parse error/Invalid Request), it MUST be Null.
        :type id: str or int or None

        Either the result member or error member MUST be included, but both
        members MUST NOT be included.
        """

        self._data = {}
        self.result = result
        self.error = error
        self._id = _id

        if self.result is None and self.error is None:
            raise ValueError("Either result or error should be used")

    @property
    @abstractmethod
    def data(self):
        return self._data

    @data.setter
    @abstractmethod
    def data(self, value):
        pass

    @property
    def json(self):
        return self.serialize(self.data)
