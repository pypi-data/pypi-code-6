import logging

from .exceptions import (
    JSONRPCInvalidParams,
    JSONRPCInvalidRequest,
    JSONRPCInvalidRequestException,
    JSONRPCMethodNotFound,
    JSONRPCParseError,
    JSONRPCServerError,
)
from .jsonrpc import JSONRPCBatchRequest, JSONRPCBatchResponse, JSONRPCResponse, JSONRPCRequest


logger = logging.getLogger(__name__)


class JSONRPCResponseManager:
    """ JSON-RPC response manager. """

    def __init__(self, json_object_hook=None):
        self.json_object_hook = json_object_hook

    def handle(self, request_str, dispatcher):
        """
        Method brings syntactic sugar into library.
        Given dispatcher it handles request (both single and batch) and handles errors.
        Request could be handled in parallel, it is server responsibility.

        :param request_str: JSON string.
            Will be converted into JSONRPCRequest or JSONRPCBatchRequest
        :type request_str: str
        :type dispatcher: Dispatcher or dict
        :rtype: JSONRPCResponse or JSONRPCBatchResponse
        """

        try:
            request = JSONRPCRequest.from_json(request_str, object_hook=self.json_object_hook)
        except (TypeError, ValueError):
            return JSONRPCParseError().as_response()
        except JSONRPCInvalidRequestException:
            return JSONRPCInvalidRequest().as_response()

        if isinstance(request, JSONRPCBatchRequest):
            rs = request
        else:
            rs = [request]

        responses = [r for r in self._get_responses(rs, dispatcher) if r is not None]

        # notifications
        if not responses:
            return

        if isinstance(request, JSONRPCBatchRequest):
            return JSONRPCBatchResponse(responses)
        else:
            return responses[0]

    @classmethod
    def _get_responses(cls, requests, dispatcher):
        """ Response to each single JSON-RPC Request.

        :type dispatcher: Dispatcher
        :type requests: iterator(JSONRPCRequest)
        :return iterator(JSONRPCResponse):

        """
        for request in requests:
            try:
                method = dispatcher[request.method]
            except KeyError:
                output = JSONRPCMethodNotFound().as_response(_id=request._id)
            else:
                try:
                    result = method(*request.args, **request.kwargs)
                except TypeError:
                    output = JSONRPCInvalidParams().as_response(_id=request._id)
                except Exception as e:
                    data = {
                        "type": e.__class__.__name__,
                        "args": e.args,
                        "message": str(e),
                    }
                    logger.exception("API Exception: {0}".format(data))
                    output = JSONRPCServerError(data=data).as_response(_id=request._id)
                else:
                    output = JSONRPCResponse(_id=request._id, result=result)
            finally:
                if not request.is_notification:
                    yield output
