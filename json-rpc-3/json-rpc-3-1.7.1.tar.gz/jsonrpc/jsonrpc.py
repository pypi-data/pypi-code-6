""" JSON-RPC wrappers for version 1.0 and 2.0.

Objects diring init operation try to choose JSON-RPC 2.0 and in case of error JSON-RPC 1.0.
from_json methods could decide what format is it by presence of 'jsonrpc' attribute.
"""

import json

from .exceptions import JSONRPCError, JSONRPCInvalidRequestException
from .base import JSONRPCBaseRequest, JSONRPCBaseResponse


class JSONRPCRequest(JSONRPCBaseRequest):
    """A rpc call is represented by sending a Request object to a Server."""

    REQUIRED_FIELDS = {"jsonrpc", "method"}
    POSSIBLE_FIELDS = {"jsonrpc", "method", "params", "id"}

    @property
    def data(self):
        data = {k: v for k, v in self._data.items()
                if not (k == "id" and self.is_notification)}
        data["jsonrpc"] = "2.0"
        return data

    @data.setter
    def data(self, value):
        if not isinstance(value, dict):
            raise ValueError("data should be dict")

        self._data = value

    @property
    def method(self):
        return self._data.get("method")

    @method.setter
    def method(self, value):
        if not isinstance(value, str):
            raise ValueError("Method should be string")

        if value.startswith("rpc."):
            raise ValueError(
                "Method names that begin with the word rpc followed by a "
                "period character (U+002E or ASCII 46) are reserved for "
                "rpc-internal methods and extensions and MUST NOT be used "
                "for anything else.")

        self._data["method"] = str(value)

    @property
    def params(self):
        return self._data.get("params")

    @params.setter
    def params(self, value):
        if value is not None and not isinstance(value, (list, tuple, dict)):
            raise ValueError("Incorrect params {0}".format(value))

        if isinstance(value, tuple):
            value = list(value)

        if value is not None:
            self._data["params"] = value

    @property
    def _id(self):
        return self._data.get("id")

    @_id.setter
    def _id(self, value):
        if value is not None and not isinstance(value, (str, int)):
            raise ValueError("id should be string or integer")

        self._data["id"] = value

    @classmethod
    def from_json(cls, json_str, object_hook=None):
        data = cls.deserialize(json_str, object_hook=object_hook)

        is_batch = isinstance(data, list)
        data = data if is_batch else [data]

        if not data:
            raise JSONRPCInvalidRequestException("[] value is not accepted")

        if not all(isinstance(d, dict) for d in data):
            raise JSONRPCInvalidRequestException("Each request should be an object (dict)")

        result = []
        for d in data:
            if not cls.REQUIRED_FIELDS <= set(d.keys()) <= cls.POSSIBLE_FIELDS:
                extra = set(d.keys()) - cls.POSSIBLE_FIELDS
                missed = cls.REQUIRED_FIELDS - set(d.keys())
                msg = "Invalid request. Extra fields: {0}, Missed fields: {1}"
                raise JSONRPCInvalidRequestException(msg.format(extra, missed))

            try:
                result.append(JSONRPCRequest(
                    method=d["method"], params=d.get("params"),
                    _id=d.get("id"), is_notification="id" not in d,
                ))
            except ValueError as e:
                raise JSONRPCInvalidRequestException(str(e))

        return JSONRPCBatchRequest(result) if is_batch else result[0]


class JSONRPCBatchRequest:
    """ Batch JSON-RPC 2.0 Request. """

    def __init__(self, requests):
        """
        :param requests: requests
        :type requests: iterable(JSONRPCRequest)
        """
        self.requests = requests

    @classmethod
    def from_json(cls, json_str):
        return JSONRPCRequest.from_json(json_str)

    @property
    def json(self):
        return json.dumps([r.data for r in self.requests])

    def __iter__(self):
        return iter(self.requests)


class JSONRPCResponse(JSONRPCBaseResponse):
    """ JSON-RPC response object to JSONRPCRequest. """

    @property
    def data(self):
        data = {k: v for k, v in self._data.items()}
        data["jsonrpc"] = "2.0"
        return data

    @data.setter
    def data(self, value):
        if not isinstance(value, dict):
            raise ValueError("data should be dict")

        self._data = value

    @property
    def result(self):
        return self._data.get("result")

    @result.setter
    def result(self, value):
        if value is not None:
            if self.error is not None:
                raise ValueError("Either result or error should be used")

            self._data["result"] = value

    @property
    def error(self):
        return self._data.get("error")

    @error.setter
    def error(self, value):
        if value is not None:
            if self.result is not None:
                raise ValueError("Either result or error should be used")

            JSONRPCError(**value)
            self._data["error"] = value

    @property
    def _id(self):
        return self._data.get("id")

    @_id.setter
    def _id(self, value):
        if value is not None and not isinstance(value, (str, int)):
            raise ValueError("id should be string or integer")

        self._data["id"] = value


class JSONRPCBatchResponse:
    def __init__(self, responses):
        self.responses = responses

    @property
    def data(self):
        return [r.data for r in self.responses]

    @property
    def json(self):
        return json.dumps(self.data)

    def __iter__(self):
        return iter(self.responses)
