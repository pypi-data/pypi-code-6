import json
import unittest

from ..exceptions import JSONRPCInvalidRequestException
from ..jsonrpc import JSONRPCRequest, JSONRPCBatchRequest, JSONRPCResponse, JSONRPCBatchResponse


class TestJSONRPCRequest(unittest.TestCase):
    """ Test JSONRPCRequest functionality."""

    def setUp(self):
        self.request_params = {
            "method": "add",
            "params": [1, 2],
            "_id": 1,
        }

    def test_correct_init(self):
        """ Test object is created."""
        JSONRPCRequest(**self.request_params)

    def test_validation_incorrect_no_parameters(self):
        with self.assertRaises(ValueError):
            JSONRPCRequest()

    def test_method_validation_str(self):
        self.request_params.update({"method": "add"})
        JSONRPCRequest(**self.request_params)

    def test_method_validation_not_str(self):
        self.request_params.update({"method": []})
        with self.assertRaises(ValueError):
            JSONRPCRequest(**self.request_params)

        self.request_params.update({"method": {}})
        with self.assertRaises(ValueError):
            JSONRPCRequest(**self.request_params)

    def test_method_validation_str_rpc_prefix(self):
        """ Test method SHOULD NOT starts with rpc. """
        self.request_params.update({"method": "rpc."})
        with self.assertRaises(ValueError):
            JSONRPCRequest(**self.request_params)

        self.request_params.update({"method": "rpc.test"})
        with self.assertRaises(ValueError):
            JSONRPCRequest(**self.request_params)

        self.request_params.update({"method": "rpccorrect"})
        JSONRPCRequest(**self.request_params)

        self.request_params.update({"method": "rpc"})
        JSONRPCRequest(**self.request_params)

    def test_params_validation_list(self):
        self.request_params.update({"params": []})
        JSONRPCRequest(**self.request_params)

        self.request_params.update({"params": [0]})
        JSONRPCRequest(**self.request_params)

    def test_params_validation_tuple(self):
        self.request_params.update({"params": ()})
        JSONRPCRequest(**self.request_params)

        self.request_params.update({"params": tuple([0])})
        JSONRPCRequest(**self.request_params)

    def test_params_validation_dict(self):
        self.request_params.update({"params": {}})
        JSONRPCRequest(**self.request_params)

        self.request_params.update({"params": {"a": 0}})
        JSONRPCRequest(**self.request_params)

    def test_params_validation_none(self):
        self.request_params.update({"params": None})
        JSONRPCRequest(**self.request_params)

    def test_params_validation_incorrect(self):
        self.request_params.update({"params": "str"})
        with self.assertRaises(ValueError):
            JSONRPCRequest(**self.request_params)

    def test_request_args(self):
        self.assertEqual(JSONRPCRequest("add").args, ())
        self.assertEqual(JSONRPCRequest("add", []).args, ())
        self.assertEqual(JSONRPCRequest("add", {"a": 1}).args, ())
        self.assertEqual(JSONRPCRequest("add", [1, 2]).args, (1, 2))

    def test_request_kwargs(self):
        self.assertEqual(JSONRPCRequest("add").kwargs, {})
        self.assertEqual(JSONRPCRequest("add", [1, 2]).kwargs, {})
        self.assertEqual(JSONRPCRequest("add", {}).kwargs, {})
        self.assertEqual(JSONRPCRequest("add", {"a": 1}).kwargs, {"a": 1})

    def test_id_validation_string(self):
        self.request_params.update({"_id": "id"})
        JSONRPCRequest(**self.request_params)

    def test_id_validation_int(self):
        self.request_params.update({"_id": 0})
        JSONRPCRequest(**self.request_params)

    def test_id_validation_null(self):
        self.request_params.update({"_id": "null"})
        JSONRPCRequest(**self.request_params)

    def test_id_validation_none(self):
        self.request_params.update({"_id": None})
        JSONRPCRequest(**self.request_params)

    def test_id_validation_float(self):
        self.request_params.update({"_id": 0.1})
        with self.assertRaises(ValueError):
            JSONRPCRequest(**self.request_params)

    def test_id_validation_incorrect(self):
        self.request_params.update({"_id": []})
        with self.assertRaises(ValueError):
            JSONRPCRequest(**self.request_params)

        self.request_params.update({"_id": ()})
        with self.assertRaises(ValueError):
            JSONRPCRequest(**self.request_params)

    def test_data_method_1(self):
        r = JSONRPCRequest("add")
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
            "id": None,
        })

    def test_data_method_2(self):
        r = JSONRPCRequest(method="add")
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
            "id": None,
        })

    def test_data_method_3(self):
        r = JSONRPCRequest("add", None)
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
            "id": None,
        })

    def test_data_params_1(self):
        r = JSONRPCRequest("add", params=None, _id=None)
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
            "id": None,
        })

    def test_data_params_2(self):
        r = JSONRPCRequest("add", [])
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
            "params": [],
            "id": None,
        })

    def test_data_params_3(self):
        r = JSONRPCRequest("add", ())
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
            "params": [],
            "id": None,
        })

    def test_data_params_4(self):
        r = JSONRPCRequest("add", (1, 2))
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
            "params": [1, 2],
            "id": None,
        })

    def test_data_params_5(self):
        r = JSONRPCRequest("add", {"a": 0})
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
            "params": {"a": 0},
            "id": None,
        })

    def test_data_id_1(self):
        r = JSONRPCRequest("add", _id="null")
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
            "id": "null",
        })

    def test_data_id_1_notification(self):
        r = JSONRPCRequest("add", _id="null", is_notification=True)
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
        })

    def test_data_id_2(self):
        r = JSONRPCRequest("add", _id=None)
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
            "id": None,
        })

    def test_data_id_2_notification(self):
        r = JSONRPCRequest("add", _id=None, is_notification=True)
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
        })

    def test_data_id_3(self):
        r = JSONRPCRequest("add", _id="id")
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
            "id": "id",
        })

    def test_data_id_3_notification(self):
        r = JSONRPCRequest("add", _id="id", is_notification=True)
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
        })

    def test_data_id_4(self):
        r = JSONRPCRequest("add", _id=0)
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
            "id": 0,
        })

    def test_data_id_4_notification(self):
        r = JSONRPCRequest("add", _id=0, is_notification=True)
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
        })

    def test_is_notification(self):
        r = JSONRPCRequest("add")
        self.assertFalse(r.is_notification)

        r = JSONRPCRequest("add", _id=None)
        self.assertFalse(r.is_notification)

        r = JSONRPCRequest("add", _id="null")
        self.assertFalse(r.is_notification)

        r = JSONRPCRequest("add", _id=0)
        self.assertFalse(r.is_notification)

        r = JSONRPCRequest("add", is_notification=True)
        self.assertTrue(r.is_notification)

        r = JSONRPCRequest("add", is_notification=True, _id=None)
        self.assertTrue(r.is_notification)
        self.assertNotIn("id", r.data)

        r = JSONRPCRequest("add", is_notification=True, _id=0)
        self.assertTrue(r.is_notification)
        self.assertNotIn("id", r.data)

    def test_set_unset_notification_keep_id(self):
        r = JSONRPCRequest("add", is_notification=True, _id=0)
        self.assertTrue(r.is_notification)
        self.assertFalse("id" in r.data)

        r.is_notification = False
        self.assertFalse(r.is_notification)
        self.assertTrue("id" in r.data)
        self.assertEqual(r.data["id"], 0)

    def test_serialize_method_1(self):
        r = JSONRPCRequest("add")
        self.assertTrue(
            {
                "jsonrpc": "2.0",
                "method": "add",
                "id": None,
            }, json.loads(r.json))

    def test_serialize_method_2(self):
        r = JSONRPCRequest(method="add")
        self.assertTrue(
            {
                "jsonrpc": "2.0",
                "method": "add",
                "id": None,
            }, json.loads(r.json))

    def test_serialize_method_3(self):
        r = JSONRPCRequest("add", None)
        self.assertTrue(
            {
                "jsonrpc": "2.0",
                "method": "add",
                "id": None,
            }, json.loads(r.json))

    def test_serialize_params_1(self):
        r = JSONRPCRequest("add", params=None, _id=None)
        self.assertTrue(
            {
                "jsonrpc": "2.0",
                "method": "add",
                "id": None,
            }, json.loads(r.json))

    def test_serialize_params_2(self):
        r = JSONRPCRequest("add", [])
        self.assertTrue(
            {
                "jsonrpc": "2.0",
                "method": "add",
                "params": [],
                "id": None,
            }, json.loads(r.json))

    def test_serialize_params_3(self):
        r = JSONRPCRequest("add", ())
        self.assertTrue(
            {
                "jsonrpc": "2.0",
                "method": "add",
                "params": [],
                "id": None,
            }, json.loads(r.json))

    def test_serialize_params_4(self):
        r = JSONRPCRequest("add", (1, 2))
        self.assertTrue(
            {
                "jsonrpc": "2.0",
                "method": "add",
                "params": [1, 2],
                "id": None,
            }, json.loads(r.json))

    def test_serialize_params_5(self):
        r = JSONRPCRequest("add", {"a": 0})
        self.assertTrue(
            {
                "jsonrpc": "2.0",
                "method": "add",
                "params": {"a": 0},
                "id": None,
            }, json.loads(r.json))

    def test_serialize_id_1(self):
        r = JSONRPCRequest("add", _id="null")
        self.assertTrue(
            {
                "jsonrpc": "2.0",
                "method": "add",
                "id": "null",
            }, json.loads(r.json))

    def test_serialize_id_2(self):
        r = JSONRPCRequest("add", _id=None)
        self.assertTrue(
            {
                "jsonrpc": "2.0",
                "method": "add",
                "id": None,
            }, json.loads(r.json))

    def test_serialize_id_3(self):
        r = JSONRPCRequest("add", _id="id")
        self.assertTrue(
            {
                "jsonrpc": "2.0",
                "method": "add",
                "id": "id",
            }, json.loads(r.json))

    def test_serialize_id_4(self):
        r = JSONRPCRequest("add", _id=0)
        self.assertTrue(
            {
                "jsonrpc": "2.0",
                "method": "add",
                "id": 0,
            }, json.loads(r.json))

    def test_from_json_request_no_id(self):
        str_json = json.dumps({
            "method": "add",
            "params": [1, 2],
            "jsonrpc": "2.0",
        })

        request = JSONRPCRequest.from_json(str_json)
        self.assertTrue(isinstance(request, JSONRPCRequest))
        self.assertEqual(request.method, "add")
        self.assertEqual(request.params, [1, 2])
        self.assertEqual(request._id, None)
        self.assertTrue(request.is_notification)

    def test_from_json_request_no_params(self):
        str_json = json.dumps({
            "method": "add",
            "jsonrpc": "2.0",
        })

        request = JSONRPCRequest.from_json(str_json)
        self.assertTrue(isinstance(request, JSONRPCRequest))
        self.assertEqual(request.method, "add")
        self.assertEqual(request.params, None)
        self.assertEqual(request._id, None)
        self.assertTrue(request.is_notification)

    def test_from_json_request_null_id(self):
        str_json = json.dumps({
            "method": "add",
            "jsonrpc": "2.0",
            "id": None,
        })

        request = JSONRPCRequest.from_json(str_json)
        self.assertTrue(isinstance(request, JSONRPCRequest))
        self.assertEqual(request.method, "add")
        self.assertEqual(request.params, None)
        self.assertEqual(request._id, None)
        self.assertFalse(request.is_notification)

    def test_from_json_request(self):
        str_json = json.dumps({
            "method": "add",
            "params": [0, 1],
            "jsonrpc": "2.0",
            "id": "id",
        })

        request = JSONRPCRequest.from_json(str_json)
        self.assertTrue(isinstance(request, JSONRPCRequest))
        self.assertEqual(request.method, "add")
        self.assertEqual(request.params, [0, 1])
        self.assertEqual(request._id, "id")
        self.assertFalse(request.is_notification)

    def test_from_json_invalid_request_jsonrpc(self):
        str_json = json.dumps({
            "method": "add",
        })

        with self.assertRaises(JSONRPCInvalidRequestException):
            JSONRPCRequest.from_json(str_json)

    def test_from_json_invalid_request_method(self):
        str_json = json.dumps({
            "jsonrpc": "2.0",
        })

        with self.assertRaises(JSONRPCInvalidRequestException):
            JSONRPCRequest.from_json(str_json)

    def test_from_json_invalid_request_extra_data(self):
        str_json = json.dumps({
            "jsonrpc": "2.0",
            "method": "add",
            "is_notification": True,
        })

        with self.assertRaises(JSONRPCInvalidRequestException):
            JSONRPCRequest.from_json(str_json)

    def test_data_setter(self):
        request = JSONRPCRequest(**self.request_params)
        with self.assertRaises(ValueError):
            request.data = []

        with self.assertRaises(ValueError):
            request.data = ""

        with self.assertRaises(ValueError):
            request.data = None


class TestJSONRPCBatchRequest(unittest.TestCase):
    """ Test JSONRPCBatchRequest functionality."""

    def test_batch_request(self):
        request = JSONRPCBatchRequest([
            JSONRPCRequest("devide", {"num": 1, "denom": 2}, _id=1),
            JSONRPCRequest("devide", {"num": 3, "denom": 2}, _id=2)
        ])
        self.assertEqual(json.loads(request.json), [
            {"method": "devide", "params": {"num": 1, "denom": 2}, "id": 1,
             "jsonrpc": "2.0"},
            {"method": "devide", "params": {"num": 3, "denom": 2}, "id": 2,
             "jsonrpc": "2.0"},
        ])

    def test_from_json_batch(self):
        str_json = json.dumps([
            {"method": "add", "params": [1, 2], "jsonrpc": "2.0"},
            {"method": "mul", "params": [1, 2], "jsonrpc": "2.0"},
        ])

        requests = JSONRPCBatchRequest.from_json(str_json)
        self.assertTrue(isinstance(requests, JSONRPCBatchRequest))
        for r in requests:
            self.assertTrue(isinstance(r, JSONRPCRequest))
            self.assertTrue(r.method in ["add", "mul"])
            self.assertEqual(r.params, [1, 2])
            self.assertEqual(r._id, None)
            self.assertTrue(r.is_notification)

    def test_from_json_batch_one(self):
        str_json = json.dumps([
            {"method": "add", "params": [1, 2], "jsonrpc": "2.0", "id": None},
        ])

        requests = JSONRPCRequest.from_json(str_json)
        self.assertTrue(isinstance(requests, JSONRPCBatchRequest))
        requests = list(requests)
        self.assertEqual(len(requests), 1)
        r = requests[0]
        self.assertTrue(isinstance(r, JSONRPCRequest))
        self.assertEqual(r.method, "add")
        self.assertEqual(r.params, [1, 2])
        self.assertEqual(r._id, None)
        self.assertFalse(r.is_notification)

    def test_response_iterator(self):
        requests = JSONRPCBatchRequest([
            JSONRPCRequest("devide", {"num": 1, "denom": 2}, _id=1),
            JSONRPCRequest("devide", {"num": 3, "denom": 2}, _id=2),
        ])
        for request in requests:
            self.assertTrue(isinstance(request, JSONRPCRequest))
            self.assertEqual(request.method, "devide")


class TestJSONRPCResponse(unittest.TestCase):
    """ Test JSONRPCResponse functionality."""

    def setUp(self):
        self.response_success_params = {
            "result": "",
            "_id": 1,
        }
        self.response_error_params = {
            "error": {
                "code": 1,
                "message": "error",
            },
            "_id": 1,
        }

    def test_correct_init(self):
        """ Test object is created."""
        JSONRPCResponse(**self.response_success_params)

    def test_validation_incorrect_no_parameters(self):
        with self.assertRaises(ValueError):
            JSONRPCResponse()

    def test_validation_incorrect_result_and_error(self):
        with self.assertRaises(ValueError):
            JSONRPCResponse(result="", error={"code": 1, "message": ""})

        response = JSONRPCResponse(error={"code": 1, "message": ""})
        with self.assertRaises(ValueError):
            response.result = ""

    def test_validation_error_correct(self):
        JSONRPCResponse(**self.response_error_params)

    def test_validation_error_incorrect(self):
        self.response_error_params["error"].update({"code": "str"})
        with self.assertRaises(ValueError):
            JSONRPCResponse(**self.response_error_params)

    def test_validation_error_incorrect_no_code(self):
        del self.response_error_params["error"]["code"]
        with self.assertRaises(ValueError):
            JSONRPCResponse(**self.response_error_params)

    def test_validation_error_incorrect_no_message(self):
        del self.response_error_params["error"]["message"]
        with self.assertRaises(ValueError):
            JSONRPCResponse(**self.response_error_params)

    def test_validation_error_incorrect_message_not_str(self):
        self.response_error_params["error"].update({"message": 0})
        with self.assertRaises(ValueError):
            JSONRPCResponse(**self.response_error_params)

    def test_validation_id(self):
        response = JSONRPCResponse(**self.response_success_params)
        self.assertEqual(response._id, self.response_success_params["_id"])

    def test_validation_id_incorrect_type(self):
        response = JSONRPCResponse(**self.response_success_params)

        with self.assertRaises(ValueError):
            response._id = []

        with self.assertRaises(ValueError):
            response._id = {}

        with self.assertRaises(ValueError):
            response._id = 0.1

    def test_data_result(self):
        r = JSONRPCResponse(result="")
        self.assertEqual(json.loads(r.json), r.data)
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "result": "",
            "id": None,
        })

    def test_data_result_id_none(self):
        r = JSONRPCResponse(result="", _id=None)
        self.assertEqual(json.loads(r.json), r.data)
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "result": "",
            "id": None,
        })

    def test_data_result_id(self):
        r = JSONRPCResponse(result="", _id=0)
        self.assertEqual(json.loads(r.json), r.data)
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "result": "",
            "id": 0,
        })

    def test_data_error(self):
        r = JSONRPCResponse(error={"code": 0, "message": ""})
        self.assertEqual(json.loads(r.json), r.data)
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "error": {
                "code": 0,
                "message": "",
            },
            "id": None,
        })

    def test_data_error_id_none(self):
        r = JSONRPCResponse(error={"code": 0, "message": ""}, _id=None)
        self.assertEqual(json.loads(r.json), r.data)
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "error": {
                "code": 0,
                "message": "",
            },
            "id": None,
        })

    def test_data_error_id(self):
        r = JSONRPCResponse(error={"code": 0, "message": ""}, _id=0)
        self.assertEqual(json.loads(r.json), r.data)
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "error": {
                "code": 0,
                "message": "",
            },
            "id": 0,
        })

    def test_data_setter(self):
        response = JSONRPCResponse(**self.response_success_params)
        with self.assertRaises(ValueError):
            response.data = []

        with self.assertRaises(ValueError):
            response.data = ""

        with self.assertRaises(ValueError):
            response.data = None


class TestJSONRPCBatchResponse(unittest.TestCase):
    """ Test JSONRPCBatchResponse functionality."""

    def test_batch_response(self):
        response = JSONRPCBatchResponse([
            JSONRPCResponse(result="result", _id=1),
            JSONRPCResponse(error={"code": 0, "message": ""}, _id=2),
        ])
        self.assertEqual(json.loads(response.json), [
            {"result": "result", "id": 1, "jsonrpc": "2.0"},
            {"error": {"code": 0, "message": ""}, "id": 2, "jsonrpc": "2.0"},
        ])

    def test_response_iterator(self):
        responses = JSONRPCBatchResponse([
            JSONRPCResponse(result="result", _id=1),
            JSONRPCResponse(result="result", _id=2),
        ])
        for response in responses:
            self.assertTrue(isinstance(response, JSONRPCResponse))
            self.assertEqual(response.result, "result")

    def test_batch_response_data(self):
        response = JSONRPCBatchResponse([
            JSONRPCResponse(result="result", _id=1),
            JSONRPCResponse(result="result", _id=2),
            JSONRPCResponse(result="result"),
        ])
        self.assertEqual(response.data, [
            {"id": 1, "jsonrpc": "2.0", "result": "result"},
            {"id": 2, "jsonrpc": "2.0", "result": "result"},
            {"id": None, "jsonrpc": "2.0", "result": "result"},
        ])
