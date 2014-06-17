import json


class JSONRPCException(Exception):
    """ JSON-RPC Exception."""
    pass


class JSONRPCInvalidRequestException(JSONRPCException):
    """ Request is not valid."""
    pass


class JSONRPCError:
    """
    Error for JSON-RPC communication.

    When a rpc call encounters an error, the Response Object MUST contain the
    error member with a value that is a Object with the following members:

    :param int code: A Number that indicates the error type that occurred.
        This MUST be an integer.

    :param str message: A String providing a short description of the error.
        The message SHOULD be limited to a concise single sentence.

    :param data: A Primitive or Structured value that contains additional
        information about the error.
        This may be omitted.
        The value of this member is defined by the Server (e.g. detailed error
        information, nested errors etc.).

    :type data: None or int or str or dict or list

    The error codes from and including -32768 to -32000 are reserved for
    pre-defined errors. Any code within this range, but not defined explicitly
    below is reserved for future use. The error codes are nearly the same as
    those suggested for XML-RPC at the following
    url: http://xmlrpc-epi.sourceforge.net/specs/rfc.fault_codes.php
    """

    serialize = staticmethod(json.dumps)
    deserialize = staticmethod(json.loads)

    def __init__(self, code=None, message=None, data=None):
        self._data = {}
        self.code = getattr(self.__class__, "CODE", code)
        self.message = getattr(self.__class__, "MESSAGE", message)
        self.data = data

    @property
    def code(self):
        return self._data["code"]

    @code.setter
    def code(self, value):
        if not isinstance(value, int):
            raise ValueError("Error code should be integer")

        self._data["code"] = value

    @property
    def message(self):
        return self._data["message"]

    @message.setter
    def message(self, value):
        if not isinstance(value, str):
            raise ValueError("Error message should be string")
        self._data["message"] = value

    @property
    def data(self):
        return self._data.get("data")

    @data.setter
    def data(self, value):
        if value is not None:
            self._data["data"] = value

    @classmethod
    def from_json(cls, json_str):
        data = cls.deserialize(json_str)
        return cls(code=data["code"], message=data["message"], data=data.get("data"))

    @property
    def json(self):
        return self.serialize(self._data)

    def as_response(self, _id=None):
        import jsonrpc

        return jsonrpc.JSONRPCResponse(error=self._data, _id=_id)


class JSONRPCParseError(JSONRPCError):
    """ Parse Error.

    Invalid JSON was received by the server.
    An error occurred on the server while parsing the JSON text.
    """

    CODE = -32700
    MESSAGE = "Parse error"


class JSONRPCInvalidRequest(JSONRPCError):
    """ Invalid Request.

    The JSON sent is not a valid Request object.
    """

    CODE = -32600
    MESSAGE = "Invalid Request"


class JSONRPCMethodNotFound(JSONRPCError):
    """ Method not found.

    The method does not exist / is not available.
    """

    CODE = -32601
    MESSAGE = "Method not found"


class JSONRPCInvalidParams(JSONRPCError):
    """ Invalid params.

    Invalid method parameter(s).
    """

    CODE = -32602
    MESSAGE = "Invalid params"


class JSONRPCInternalError(JSONRPCError):
    """ Internal error.

    Internal JSON-RPC error.
    """

    CODE = -32603
    MESSAGE = "Internal error"


class JSONRPCServerError(JSONRPCError):
    """ Server error.

    Reserved for implementation-defined server-errors.
    """

    CODE = -32000
    MESSAGE = "Server error"
