# coding=UTF-8
#
#	Copyright 2013-2014, Marten de Vries
#
#	Licensed under the Apache License, Version 2.0 (the "License");
#	you may not use this file except in compliance with the License.
#	You may obtain a copy of the License at
#
#	http://www.apache.org/licenses/LICENSE-2.0
#
#	Unless required by applicable law or agreed to in writing, software
#	distributed under the License is distributed on an "AS IS" BASIS,
#	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#	See the License for the specific language governing permissions and
#	limitations under the License.

from pouchdb.tests.utils import (
	SyncPouchDBTestCaseWithDB,
	SyncPouchDBTestCaseWithDBAndDoc,
	SyncPouchDBTestCaseWithDBAndAttachment,
	SyncPouchDBHTTPTestCase,

	AsyncPouchDBTestCaseWithDB,

	BASE_URL,
	FAST_ONLY,
	alt_setup,
)

import pouchdb
import pouchdb.context
import json
import base64
import unittest
import collections

ONLY_TEST_VALIDATION_DOC = {
	"_id": "_design/test",
	"validate_doc_update": """function (newDoc, oldDoc, userCtx, secObj) {
		if (newDoc._id !== "test") {
			throw({forbidden: "only a document named 'test' is allowed."});
		}
	}""",
}

SHOW_DOCUMENT = {
	"_id": "_design/test",
	"shows": {
		"myshow": """function (doc, req) {
			if (!doc) {
				return {body: "no doc"}
			} else {
				return {body: doc.description}
			}
		};\n""",
		"args": """function (doc, req) {
			return toJSON({args: [doc, req]});
		}""",
		"usingProviders": """function (doc, req) {
			provides("json", function () {
				return toJSON({message: "Hello World!"});
			});
			provides("html", function () {
				log({"type": "is", "html": "for", "this": "func"})
				return "<h1>Hello World!</h1>";
			});
			provides("css", function () {
				return 'body {content: "Hello World!"}';
			});
			registerType("ascii-binary", "application/octet-stream; charset=ascii")
			provides("ascii-binary", function () {
				return {
					"base64": "SGVsbG8gV29ybGQh"
				};
			})
		}""",
		"oldStyleJson": """function (doc, req) {
			return {
				json: {
					old_style: "json"
				}
			};
		}""",
		"empty": """function (doc, req) {}""",
		"nofunc": """'Hello World!'""",
		"invalidsyntax": """function (doc, req)) {}""",
		"invalidReturnTypeAndProvides": """function (doc, req) {
			provides("html", function () {
				return 42;
			});
		}""",
		"throwingError": """function (doc, req) {
			throw new Error("Hello World!")
		}""",
		"throwingErrorInProvides": """function (doc, req) {
			provides("text", function () {
				throw new Error("Hello World!");
			});
		}""",
		"invalidRespObject": """function (doc, req) {
			return {body: "test", abc: "test"};
		}"""
	}
}

LIST_DOCUMENT = {
	"_id": "_design/test",
	"views": {
		"ids": {
			"map": """function (doc) {
				emit(doc._id, "value");
			}""",
		}
	},
	"lists": {
		"args": """function (head, req) {
			return toJSON({args: [head, req]});
		}""",
		"use-list-api": """function (head, req) {
			start({code: 500});
			send(JSON.stringify(getRow()));
			send("\\n");
			send("test");
			return "Hello World!";
		}""",
		"test-coucheval": """function (head, req) {
			var result = sum([1, 2, 3]);
			return result + " - " + require("lib/thingy").data;
		}"""
	},
	"lib": {
		"thingy": "exports.data = 'Hello World!';"
	}
}

UPDATE_DOCUMENT = {
	"_id": "_design/test",
	"updates": {
		"args": """function (doc, req) {
			return [null, toJSON([doc, req])];
		}""",
		"exception": """function (doc, req) {
			return abc;
		}""",
		"save-adding-date": """function (oldDoc, req) {
			var doc = JSON.parse(req.body);
			doc.updated = new Date();
			return [doc, "Hello World!"];
		}"""
	}
}

REWRITE_DOCUMENT = {
	"_id": "_design/test",
	"rewrites": [
		{
			"from": "/test/all",
			"to": "_list/test/ids",
		},
	],
}

class AlternateSignatureTests(SyncPouchDBTestCaseWithDB):
	"""Tests alternative signatures for the internally developed
	plug-ins that ship with Python-PouchDB. Hard to do via the Python
	interface since that interface uses a fixed JS signature regardless
	of which Python signature is used. (At least mostly)

	"""
	def testShow(self):
		#the fact that dbs are stored in ``objects`` is an
		#implementation detail.
		promise = self._env.context.evalJs("return objects[%s].show('test/test/test', function () {});" % self._db._id)
		self.assertPromise(promise)

	def testList(self):
		promise = self._env.context.evalJs("return objects[%s].list('test/test/test', function () {});" % self._db._id)
		self.assertPromise(promise)

	def testValidatingPost(self):
		promise = self._env.context.evalJs("return objects[%s].validatingPost({}, function () {});" % self._db._id)
		self.assertPromise(promise)

	def testUpdate(self):
		promise = self._env.context.evalJs("return objects[%s].update('test/test/test', function () {});" % self._db._id)
		self.assertPromise(promise)

	def testRewrite(self):
		promise = self._env.context.evalJs("return objects[%s].rewrite('test/test/test', function () {});" % self._db._id)
		self.assertPromise(promise)

@unittest.skipIf(FAST_ONLY, "too slow")
class PluginHTTPTests(SyncPouchDBHTTPTestCase):
	def testShow(self):
		self._db.put(SHOW_DOCUMENT)

		resp = self._db.show("test/args", body="Hello World!", headers={"Content-Type": "text/plain"})
		self.assertEqual(resp["code"], 200)
		self.assertEqual(resp["headers"]["Content-Type"], "text/html; charset=utf-8")

		doc, req = json.loads(resp.body)["args"]

		#test doc - well, the unavailability of it...
		self.assertIsNone(doc)

		#test request object
		self.assertEqual(req["body"], "Hello World!")
		self.assertEqual(req["cookie"], {})
		self.assertEqual(req["form"], {})

		self.assertIn(req["headers"]["Host"], BASE_URL)
		self.assertEqual(req["headers"]["Accept"], "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
		self.assertEqual(req["headers"]["Content-Type"], "text/plain")
		self.assertIn("en", req["headers"]["Accept-Language"])
		self.assertIn("en-us", req["headers"]["Accept-Language"])
		self.assertWebKitUserAgent(req["headers"]["User-Agent"])

		self.assertIsNone(req["id"])
		self.assertEqual(req["info"]["db_name"], "test")
		self.assertIn("update_seq", req["info"])
		self.assertEqual(req["method"], "POST")
		self.assertEqual(req["path"], ["test", "_design", "test", "_show", "args"])
		self.assertEqual(req["peer"], "127.0.0.1")
		self.assertEqual(req["query"], {})
		self.assertEqual(req["raw_path"], "/test/_design/test/_show/args")
		self.assertEqual(req["requested_path"], ["test", "_design", "test", "_show", "args"])
		self.assertEqual(req["secObj"], {})
		self.assertEqual(req["userCtx"]["db"], "test")
		self.assertIn("name", req["userCtx"])
		self.assertUuid(req["uuid"])

	def testList(self):
		self._db.put(LIST_DOCUMENT)

		resp = self._db.list(
			"test/args/ids",
			query={"a": "b"},
		)

		head, req = json.loads(resp.body)["args"]
		self.assertEqual(head["offset"], 0)
		self.assertEqual(head["total_rows"], 0)

		self.assertIsNone(req["id"])
		self.assertEqual(req["raw_path"], "/test/_design/test/_list/args/ids?a=b")
		self.assertEqual(req["requested_path"], ["test", "_design", "test", "_list", "args", "ids?a=b"])
		self.assertEqual(req["path"], ["test", "_design", "test", "_list", "args", "ids"])
		#and one at random, to check if the rest (shared with show) is still ok.
		self.assertEqual(req["peer"], "127.0.0.1")

	def testWrongListContentType(self):
		"""CouchDB only supports application/json here. It's a CouchDB
		restriction: this check is here in case it ever changes. - then
		PouchDB-List's simulation of it can stop.

		"""
		self._db.put(LIST_DOCUMENT)
		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.list("test/args/ids", headers={"Content-Type": "application/x-www-form-urlencoded"}, body="value=hello")
		self.assertEqual(cm.exception["status"], 400)
		self.assertEqual(cm.exception["name"], "bad_request")
		self.assertEqual(cm.exception["message"], "invalid_json")

	def testValidation(self):
		self._db.put(ONLY_TEST_VALIDATION_DOC)

		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.validatingPost({})
		self.assertEqual(cm.exception["status"], 403)
		self.assertEqual(cm.exception["name"], "forbidden")
		self.assertEqual(cm.exception["message"], "only a document named 'test' is allowed.")

		resp = self._db.validatingPut({"_id": "test"})
		self.assertTrue(resp.ok)

	def testUpdate(self):
		self._db.put(UPDATE_DOCUMENT)
		doc, req = json.loads(self._db.update("test/args/my-id").body)
		self.assertIsNone(doc)
		self.assertEqual(req["id"], "my-id")

	def testRewrite(self):
		self._db.put(REWRITE_DOCUMENT)

		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.rewrite("test/test/all")

		self.assertEqual(cm.exception["status"], 404)
		self.assertEqual(cm.exception["name"], "not_found")
		self.assertEqual(cm.exception["message"], "missing_named_view")

class SyncValidationSuccessTests(SyncPouchDBTestCaseWithDB):
	"""Where the other tests just check if the wrappers work and are 
		 barely checking behaviour, the validation tests do more. That is
		 because the other things have JS test suites, and the validation
		 plugin doesn't.

	"""

	def setUp(self):
		super(SyncValidationSuccessTests, self).setUp()

		self._db.put(ONLY_TEST_VALIDATION_DOC)

	def testSuccessfulPut(self):
		doc = self._db.validatingPut({"_id": "test"})
		self.assertTrue(doc["ok"])

	def testSuccessfulPost(self):
		doc = self._db.validatingPost({"_id": "test"})
		self.assertTrue(doc["ok"])

	def testSuccessfulRemove(self):
		info = self._db.put({"_id": "test"})
		rmInfo = self._db.validatingRemove({
			"_id": "test",
			"_rev": info["rev"],
		})
		self.assertTrue(rmInfo.ok)

	def testSuccessfulBulkDocs(self):
		resp = self._db.validatingBulkDocs({
			"docs": [
				{
					"_id": "test",
				},
			],
		})
		self.assertTrue(resp[0].ok)

class AsyncValidationTests(AsyncPouchDBTestCaseWithDB):
	def setUp(self):
		super(AsyncValidationTests, self).setUp()

		def cb(resp):
			pass
		self._db.put(ONLY_TEST_VALIDATION_DOC).then(cb)
		self.waitUntilCalled(cb)

	def testSuccessfulPut(self):
		def cb(err, doc):
			self.assertTrue(doc["ok"])
		self._db.validatingPut({"_id": "test"}, cb)
		self.waitUntilCalled(cb)

	def testSuccessfulPost(self):
		def cb(err, doc):
			self.assertTrue(doc.ok)
		self._db.validatingPost({"_id": "test"}, cb)
		self.waitUntilCalled(cb)

	def testSuccessfulRemove(self):
		def removeCb(err, info):
			self.assertTrue(info["ok"])
		def putCb(info):
			self._db.validatingRemove({
				"_id": "test",
				"_rev": info["rev"],
			}, removeCb)
		info = self._db.put({"_id": "test"}).then(putCb)
		self.waitUntilCalled(removeCb)

	def testSuccessfulBulkDocs(self):
		def cb(err, resp):
			self.assertTrue(resp[0].ok)
		self._db.validatingBulkDocs({
			"docs": [
				{
					"_id": "test",
				},
			],
		}, cb)
		self.waitUntilCalled(cb)

	def testSuccessfulPutAttachment(self):
		def getCb(resp):
			self.assertEqual(resp["data"], b"Hello world!")
		def putCb(err, resp):
			self.assertTrue(resp.ok)
			self._db.getAttachment("test", "test").then(getCb)

		self._db.validatingPutAttachment("test", "test", b"Hello world!", "text/plain", putCb)
		self.waitUntilCalled(getCb)

	def testFailingRemoveAttachment(self):
		def removeCb(err, resp):
			self.assertEqual(err["status"], 403)
			self.assertEqual(err.name, "forbidden")

		#setup - put an attachment
		def putCb(resp):
			#start of the test
			self._db.validatingRemoveAttachment("mytest", "test", resp.rev, removeCb)
		self._db.putAttachment("mytest", "test", b"Hello world!", "text/plain").then(putCb)
		self.waitUntilCalled(removeCb)

class SyncValidationUnauthorizedTests(SyncPouchDBTestCaseWithDBAndDoc):
	"""See the note at the :class:`ValidationSuccessTests` class"""

	def setUp(self):
		super(SyncValidationUnauthorizedTests, self).setUp()

		self._db.put({
			"_id": "_design/test",
			"validate_doc_update": """function (newDoc, oldDoc, userCtx, secObj) {
				if (newDoc._id !== "test") {
					throw({unauthorized: "only a document named 'test' is allowed."});
				}
			}""",
		})

	def _checkException(self, exc):
		self.assertEqual(exc["name"], "unauthorized")
		self.assertEqual(exc["message"], "only a document named 'test' is allowed.")

	def testInvalidPut(self):
		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.validatingPut({"_id": "test_invalid"})
		self._checkException(cm.exception)

	def testInvalidPost(self):
		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.validatingPost({})
		self._checkException(cm.exception)

	def testInvalidRemove(self):
		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.validatingRemove({
				"_id": "mytest",
				"_rev": self.rev,
			})
		self._checkException(cm.exception)

	def testInvalidBulkDocs(self):
		resp = self._db.validatingBulkDocs({
				"docs": [
					{
						"_id": "test_invalid",
					},
				],
			})
		self._checkException(resp[0])

class SyncValidationForbiddenTests(SyncPouchDBTestCaseWithDBAndDoc):
	"""See the note at the :class:`ValidationSuccessTests` class"""

	def setUp(self):
		super(SyncValidationForbiddenTests, self).setUp()

		self._db.put(ONLY_TEST_VALIDATION_DOC)

	def _checkException(self, exc):
		self.assertEqual(exc["name"], "forbidden")
		self.assertEqual(exc["message"], "only a document named 'test' is allowed.")

	def testInvalidPut(self):
		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.validatingPut({"_id": "test_invalid"})
		self._checkException(cm.exception)

	def testInvalidPost(self):
		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.validatingPost({})
		self._checkException(cm.exception)

	def testInvalidRemove(self):
		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.validatingRemove({
				"_id": "mytest",
				"_rev": self.rev,
			})
		self._checkException(cm.exception)

	def testInvalidBulkDocs(self):
		resp = self._db.validatingBulkDocs({
			"docs": [
				{
					"_id": "test_invalid",
				},
				{}
			],
		})
		self._checkException(resp[0])
		self._checkException(resp[1])

	def testDesignDoc(self):
		"""A design doc is always valid, so no matter the
			 validate_doc_update function, the stuff below should succeed.

		"""
		self._db.validatingPut({
			"_id": "_design/mytest",
		})

class SyncValidationCompilationErrorTests(SyncPouchDBTestCaseWithDB):
	"""See the note at the :class:`ValidationSuccessTests` class"""

	def _checkException(self, e):
		self.assertEqual(e["name"], "compilation_error")
		self.assertIn("Expression does not eval to a function.", e["message"])

	def testSyntaxError(self):
		self._db.put({
			"_id": "_design/test",
			"validate_doc_update": """function (newDoc, oldDoc, userCtx, secObj) {
				return;
			}324j3lkl;""",
		})

		with self.assertRaises(pouchdb.PouchDBError) as cm:
			doc = self._db.validatingPut({"_id": "test"})
		self._checkException(cm.exception)

	def testNonFunctionError(self):
		self._db.put({
			"_id": "_design/test",
			"validate_doc_update": "'a string instead of a function'",
		})
		with self.assertRaises(pouchdb.PouchDBError) as cm:
			doc = self._db.validatingPut({"_id": "test"})
		self._checkException(cm.exception)

class SyncValidationExceptionTests(SyncPouchDBTestCaseWithDBAndDoc):
	"""See the note at the :class:`ValidationSuccessTests` class"""

	def setUp(self):
		super(SyncValidationExceptionTests, self).setUp()

		self._db.put({
			"_id": "_design/test",
			"validate_doc_update": """function (newDoc, oldDoc, userCtx, secObj) {
				//reference error
				test;
			}""",
		})

	def testPut(self):
		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.validatingPut({"_id": "test"})

		self.assertEqual(cm.exception["name"], "ReferenceError")
		#'test' is the name of the missing variable.
		self.assertIn("test", cm.exception["message"])

class SyncValidationAttachmentTests(SyncPouchDBTestCaseWithDBAndAttachment):
	def setUp(self):
		super(SyncValidationAttachmentTests, self).setUp()

		self.forbiddenDesignDoc = {
			"_id": "_design/test",
			"validate_doc_update": """function (newDoc, oldDoc, userCtx, secObj) {
				throw({forbidden: JSON.stringify(newDoc)});
			}"""
		}

	def testRemoveAttachmentSuccess(self):
		self._db.validatingRemoveAttachment("attachment_test", "text", self.rev)

	def testRemoveAttachmentWhenForbidden(self):
		self._db.put(self.forbiddenDesignDoc)
		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.validatingRemoveAttachment("attachment_test", "text", self.rev)
		self.assertEqual(cm.exception["name"], "forbidden")
		#checks if the newDoc argument is filled in correctly
		self.assertIn('"_attachments":{}', cm.exception["message"])

	def testPutAttachmentSuccess(self):
		self._db.validatingPutAttachment("attachment_test2", "text", u"tést".encode("UTF-8"), "text/plain")

	def testPutAttachmentWhenForbidden(self):
		self._db.put(self.forbiddenDesignDoc)
		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.validatingPutAttachment("attachment_test2", "text", u"tést".encode("UTF-8"), "text/plain")
		self.assertEqual(cm.exception["name"], "forbidden")
		#checks if the newDoc argument is filled in correctly
		self.assertIn("text/plain", cm.exception["message"])

class SyncValidationArgsTests(SyncPouchDBTestCaseWithDBAndDoc):
	def setUp(self):
		super(SyncValidationArgsTests, self).setUp()

		self._db.put({
			"_id": "_design/test",
			"validate_doc_update": """function (newDoc, oldDoc, userCtx, secObj) {
				throw({forbidden: JSON.stringify([newDoc, oldDoc, userCtx, secObj])});
			}"""
		})

	def testArgsWithNewDoc(self):
		doc = {
			"_id": "test",
		}
		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.validatingPut(doc)
		newDoc, oldDoc, userCtx, secObj = json.loads(cm.exception["message"])
		self.assertEqual(newDoc, doc)
		self.assertIsNone(oldDoc)

		self.assertEqual(userCtx, {
			"db": "test",
			"name": None,
			"roles": ["_admin"]
		})
		self.assertEqual(secObj, {
			"admins": {
				"names": [],
				"roles": [],
			},
			"members": {
				"names": [],
				"roles": [],
			},
		})

	def testArgsWithExistingDoc(self):
		doc = {"_id": "mytest", "_rev": self.rev}
		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.validatingPut(doc)
		newDoc, oldDoc, userCtx, secObj = json.loads(cm.exception["message"])
		self.assertTrue(oldDoc["test"])
		self.assertIn("ids", oldDoc["_revisions"])
		self.assertIn("ids", newDoc["_revisions"])

	def testChangingUserCtx(self):
		theUserCtx = {
			"db": "test",
			"name": "pypouchtest",
			"roles": ["the_boss"]
		}

		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.validatingPost({}, userCtx=theUserCtx)
		newDoc, oldDoc, userCtx, secObj = json.loads(cm.exception["message"])

		self.assertEqual(userCtx, theUserCtx)

	def testChangingSecObj(self):
		theSecObj = {
			"admins": {
				"names": ["the_boss"],
				"roles": [],
			},
			"members": {
				"names": [],
				"roles": [],
			},
		}

		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.validatingPost({}, secObj=theSecObj)
		newDoc, oldDoc, userCtx, secObj = json.loads(cm.exception["message"])

		self.assertEqual(secObj, theSecObj)

class SyncShowTests(SyncPouchDBTestCaseWithDB):
	def setUp(self):
		super(SyncShowTests, self).setUp()

		self._db.put(SHOW_DOCUMENT)

	def testInvalidRespObj(self):
		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.show("test/invalidRespObject")
		self.assertEqual(cm.exception["status"], 500)
		self.assertEqual(cm.exception["name"], "external_response_error")
		self.assertEqual(cm.exception["message"], 'Invalid data from external server: {<<"abc">>,<<"test">>}')

	def testShowWithoutDocAndDifferentEnv(self):
		self._env.context.evalJs("window.theNavigator = window.navigator; window.navigator = undefined;")
		result = self._db.show("test/myshow")
		self.assertEqual(result["code"], 200)
		self._env.context.evalJs("window.navigator = window.theNavigator; delete window.theNavigator;")

	def testInvalidReturnTypeAndProvides(self):
		result = self._db.show("test/invalidReturnTypeAndProvides")
		self.assertEqual(result["code"], 200)
		self.assertEqual(result["body"], "")

	def testThrowingError(self):
		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.show("test/throwingError")
		self.assertEqual(cm.exception["status"], 500)

	def testThrowingErrorInProvides(self):
		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.show("test/throwingErrorInProvides")
		self.assertEqual(cm.exception["status"], 500)

	def testShowWithoutDoc(self):
		result = self._db.show("test/myshow")
		self.assertEqual(result["code"], 200)
		self.assertEqual(result["headers"]["Content-Type"], "text/html; charset=utf-8")
		self.assertEqual(result["headers"]["Vary"], "Accept")
		self.assertEqual(result["body"], "no doc")

	def testShowWithDoc(self):
		self._db.post({"_id": "mytest", "description": "Hello World!"})
		result = self._db.show("test/myshow/mytest")
		self.assertEqual(result["body"], "Hello World!")

	def testOverwriteArgs(self):
		resp = self._db.show("test/args", method="POST")
		doc, req = json.loads(resp.body)["args"]
		self.assertEqual(req["method"], "POST")

	def testOverwriteHeader(self):
		resp = self._db.show("test/args", headers={"Host": "example.com"})
		doc, req = json.loads(resp.body)["args"]
		#check if the header update was succesful.
		self.assertEqual(req["headers"]["Host"], "example.com")
		#check if other headers (test subject is Accept) are still set.
		self.assertEqual(req["headers"]["Accept"], "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")

	def testShowArgs(self):
		doc, req = json.loads(self._db.show("test/args").body)["args"]

		#test doc - well, the unavailability of it...
		self.assertIsNone(doc)

		#test request object
		self.assertEqual(req["body"], "undefined")
		self.assertEqual(req["cookie"], {})
		self.assertEqual(req["form"], {})

		self.assertEqual(req["headers"]["Host"], "localhost:5984")
		self.assertEqual(req["headers"]["Accept"], "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
		self.assertIn("en", req["headers"]["Accept-Language"])
		self.assertIn("en-us", req["headers"]["Accept-Language"])
		self.assertWebKitUserAgent(req["headers"]["User-Agent"])

		self.assertIsNone(req["id"])
		self.assertEqual(req["info"]["db_name"], "test")
		self.assertIn("update_seq", req["info"])
		self.assertEqual(req["method"], "GET")
		self.assertEqual(req["path"], ["test", "_design", "test", "_show", "args"])
		self.assertEqual(req["peer"], "127.0.0.1")
		self.assertEqual(req["query"], {})
		self.assertEqual(req["raw_path"], "/test/_design/test/_show/args")
		self.assertEqual(req["requested_path"], ["test", "_design", "test", "_show", "args"])
		self.assertEqual(req["secObj"], {
			"admins": {
				"names": [],
				"roles": [],
			},
			"members": {
				"names": [],
				"roles": [],
			},
		})
		self.assertEqual(req["userCtx"], {
			"db": "test",
			"name": None,
			"roles": [
				"_admin",
			],
		})
		self.assertUuid(req["uuid"])

	def testUnexistingDoc(self):
		doc, req = json.loads(self._db.show("test/args/abc").body)["args"]
		self.assertIsNone(doc)
		self.assertEqual(req["id"], "abc")
		self.assertIn("abc", req["path"])

	def testWithDesignDocAsArg(self):
		doc, req = json.loads(self._db.show("test/args/_design/test").body)["args"]
		self.assertEqual(req["id"], "_design/test")
		self.assertEqual(req["raw_path"], "/test/_design/test/_show/args/_design/test")
		self.assertIn("shows", doc)

	def testWithFakeDesignDocAsArg(self):
		doc, req = json.loads(self._db.show("test/args/_design").body)["args"]
		self.assertIsNone(doc)
		self.assertEqual(req["id"], "_design")
		self.assertEqual(req["raw_path"], "/test/_design/test/_show/args/_design")

	def testSettingQuery(self):
		resp = self._db.show("test/args", query={"a": 1})
		doc, req = json.loads(resp.body)["args"]
		self.assertIsNone(doc)
		self.assertTrue(req["raw_path"].endswith("?a=1"))
		self.assertTrue(req["requested_path"] == ["test", "_design", "test", "_show", "args?a=1"])
		self.assertTrue(req["path"] == ["test", "_design", "test", "_show", "args"])

	def testSettingForm(self):
		resp = self._db.show("test/args", form={"a": 1})
		doc, req = json.loads(resp.body)["args"]
		self.assertIsNone(doc)
		self.assertEqual(req["body"], "a=1")
		self.assertEqual(req["headers"]["Content-Type"], "application/x-www-form-urlencoded")
		self.assertEqual(req["headers"]["Content-Length"], "3")
		self.assertEqual(req["method"], "POST")

	def testUnexistingDDoc(self):
		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.show("abc/args")
		self.assertEqual(cm.exception["name"], "not_found")
		self.assertEqual(cm.exception["message"], "missing")

	def testUnexistingShowFunc(self):
		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.show("test/unexisting-show")
		self.assertEqual(cm.exception["status"], 404)
		self.assertEqual(cm.exception["name"], "not_found")
		self.assertEqual(cm.exception["message"], "missing show function unexisting-show on design doc _design/test")

	def testProvidersDefault(self):
		resp = self._db.show("test/usingProviders")
		self.assertEqual(resp["code"], 200)
		self.assertEqual(resp["body"], "<h1>Hello World!</h1>")
		self.assertEqual(resp["headers"]["Content-Type"], "text/html; charset=utf-8")
		self.assertEqual(resp["headers"]["Vary"], "Accept")

	def testProvidersFormat(self):
		resp = self._db.show("test/usingProviders", query={"format": "json"})
		self.assertEqual(resp["code"], 200)
		self.assertEqual(json.loads(resp["body"]), {"message": "Hello World!"})
		self.assertEqual(resp["headers"]["Content-Type"], "application/json")
		self.assertEqual(resp["headers"]["Vary"], "Accept")

	def testProvidersAcceptHeader(self):
		resp = self._db.show("test/usingProviders", headers={"Accept": "text/css,*/*;q=0.1"})
		self.assertEqual(resp["body"], 'body {content: "Hello World!"}')
		self.assertEqual(resp["headers"]["Content-Type"], "text/css")

	def testCustomProvider(self):
		resp = self._db.show("test/usingProviders", headers={"Accept": "application/octet-stream"})
		self.assertEqual(resp["code"], 200)
		with self.assertRaises(KeyError):
			resp["body"]
		self.assertEqual(base64.b64decode(resp["base64"].encode("ascii")), b"Hello World!")
		self.assertEqual(resp["headers"]["Content-Type"], "application/octet-stream; charset=ascii")

	def testUnexistingFormat(self):
		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.show("test/usingProviders", query={"format": "text"})
		self.assertEqual(cm.exception["status"], 500)
		self.assertEqual(cm.exception["name"], "render_error")
		self.assertEqual(cm.exception["message"], "the format option is set to 'text', but there's no provider registered for that format.")

	def testNoMatchingProvider(self):
		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.show("test/usingProviders", headers={"Accept": "text/plain"})
		self.assertEqual(cm.exception["status"], 406)
		self.assertEqual(cm.exception["name"], "not_acceptable")
		self.assertTrue(cm.exception["message"].startswith("Content-Type(s) text/plain not supported, try one of: "))
		self.assertIn("application/json", cm.exception["message"])

	def testOldStyleJson(self):
		resp = self._db.show("test/oldStyleJson")
		self.assertEqual(resp["headers"]["Content-Type"], "application/json")
		self.assertEqual(json.loads(resp["body"]), {"old_style": "json"})

	def testFormatWhenEmptyShowFunc(self):
		resp = self._db.show("test/empty")
		self.assertEqual(resp.code, 200)
		self.assertEqual(resp["headers"]["Content-Type"], "text/html; charset=utf-8")
		self.assertEqual(resp.body, "")

	def testNoFunc(self):
		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.show("test/nofunc")
		self.assertEqual(cm.exception["status"], 500)
		self.assertEqual(cm.exception["name"], "compilation_error")

	def testInvalidSyntax(self):
		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.show("test/invalidsyntax")
		self.assertEqual(cm.exception["status"], 500)
		self.assertEqual(cm.exception["name"], "compilation_error")

class SyncShowTestsWithEmptyDesignDoc(SyncPouchDBTestCaseWithDB):
	def test(self):
		self._db.put({"_id": "_design/test"})

		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.show("test/test/test")

		self.assertEqual(cm.exception["status"], 404)

class AsyncShowTests(AsyncPouchDBTestCaseWithDB):
	def setUp(self):
		super(AsyncShowTests, self).setUp()

		def cb(*args):
			pass
		self._db.put(SHOW_DOCUMENT, cb)
		self.waitUntilCalled(cb)

	def testShowWithoutDoc(self):
		def cb(err, result):
			self.assertEqual(result["body"], "no doc")
		self._db.show("test/myshow", cb)
		self.waitUntilCalled(cb)

	def testUnexistingDDoc(self):
		def cb(err, resp):
			self.assertEqual(err["name"], "not_found")
			self.assertEqual(err["message"], "missing")

		self._db.show("abc/args", cb)
		self.waitUntilCalled(cb)

class AsyncListTests(AsyncPouchDBTestCaseWithDB):
	def setUp(self):
		super(AsyncListTests, self).setUp()

		def docCb(resp):
			pass

		def ddocCb(resp):
			self._db.put({"_id": "testdoc"}).then(docCb)

		self._db.put(LIST_DOCUMENT).then(ddocCb)
		self.waitUntilCalled(docCb)

	def testArgs(self):
		def cb(err, resp):
			head, req = json.loads(resp.body)["args"]
			self.assertEqual(head["offset"], 0)
			self.assertIsNone(req["id"])
			self.assertEqual(req["query"]["a"], "b")

		self._db.list("test/args/ids", cb, query={"a": "b"})
		self.waitUntilCalled(cb)

class SyncListTestsWithEmptyDesignDoc(SyncPouchDBTestCaseWithDB):
	def test(self):
		self._db.put({"_id": "_design/test"})

		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.list("test/test/test")

		self.assertEqual(cm.exception["status"], 400)

class SyncListTests(SyncPouchDBTestCaseWithDB):
	def setUp(self):
		super(SyncListTests, self).setUp()

		self._db.put(LIST_DOCUMENT)
		self._db.put({"_id": "testdoc"})

	def testCouchEval(self):
		resp = self._db.list("test/test-coucheval/ids")
		self.assertEqual(resp["code"], 200)
		self.assertEqual(resp["body"], "6 - Hello World!")

	def testArgs(self):
		resp = self._db.list("test/args/ids", query={"a": "b"})
		head, req = json.loads(resp.body)["args"]
		self.assertEqual(head["offset"], 0)
		self.assertEqual(head["total_rows"], 1)

		self.assertIsNone(req["id"])
		self.assertEqual(req["raw_path"], "/test/_design/test/_list/args/ids?a=b")
		self.assertEqual(req["requested_path"], ["test", "_design", "test", "_list", "args", "ids?a=b"])
		self.assertEqual(req["path"], ["test", "_design", "test", "_list", "args", "ids"])
		#and one at random, to check if the rest (shared with show) is still ok.
		self.assertEqual(req["peer"], "127.0.0.1")

	def testUnexistingDesignDoc(self):
		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.list("unexisting/args/ids")
		self.assertEqual(cm.exception["name"], "not_found")

	def testUnexistingListFunc(self):
		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.list("test/unexisting/ids")
		self.assertTrue(str(cm.exception))
		self.assertEqual(cm.exception["name"], "not_found")
		self.assertEqual(cm.exception["message"], "missing list function unexisting on design doc _design/test")

	def testUnexistingView(self):
		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.list("test/args/unexisting")
		self.assertEqual(cm.exception["name"], "not_found")

	def testListApi(self):
		resp = self._db.list("test/use-list-api/ids")
		self.assertEqual(resp["headers"]["Transfer-Encoding"], "chunked")
		self.assertEqual(resp["code"], 500)
		row1, row2 = resp.body.split("\n")
		self.assertEqual(json.loads(row1), {"id": "testdoc", "key": "testdoc", "value": "value"})
		self.assertEqual(row2, "testHello World!")

	def testWrongContentType(self):
		"""CouchDB only supports application/json here. It's a CouchDB
		restriction: probably best to emulate it...

		"""
		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.list("test/args/ids", headers={"Content-Type": "application/x-www-form-urlencoded"})
		self.assertEqual(cm.exception["status"], 400)
		self.assertEqual(cm.exception["name"], "bad_request")
		self.assertEqual(cm.exception["message"], "invalid_json")

class SyncUpdateTests(SyncPouchDBTestCaseWithDBAndDoc):
	def setUp(self):
		super(SyncUpdateTests, self).setUp()

		self._db.put(UPDATE_DOCUMENT)

	def testArgs(self):
		doc, req = json.loads(self._db.update("test/args/mytest", query={"a": 3}).body)
		self.assertTrue(doc["test"])
		self.assertEqual(req["id"], "mytest")
		self.assertEqual(req["raw_path"], "/test/_design/test/_update/args/mytest?a=3")

	def testArgsWithoutDoc(self):
		resp = self._db.update("test/args", withValidation=True)
		doc, req = json.loads(resp.body)
		self.assertIsNone(doc)
		self.assertNotIn("withValidation", req)

	def testUnexistingFunction(self):
		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.update("test/unexisting/mytest")
		self.assertTrue(str(cm.exception))
		self.assertEqual(cm.exception["name"], "not_found")
		self.assertEqual(cm.exception["message"], "missing update function unexisting on design doc _design/test")

	def testSaving(self):
		resp = self._db.update("test/save-adding-date", body=json.dumps({
			"_id": "test",
			"name": "Today"
		}))
		self.assertEqual(resp.body, "Hello World!")

		doc = self._db.get("test")
		self.assertTrue(doc["updated"])
		self.assertEqual(doc["name"], "Today")

class AsyncUpdateTests(AsyncPouchDBTestCaseWithDB):
	def setUp(self):
		super(AsyncUpdateTests, self).setUp()

		def cb(err, resp):
			pass
		self._db.put(UPDATE_DOCUMENT, cb)
		self.waitUntilCalled(cb)

	def testException(self):
		def cb(err, resp):
			self.assertEqual(err["status"], 500)
			self.assertEqual(err["name"], "ReferenceError")
			self.assertIn("abc", err["message"])

		self._db.update("test/exception", cb)
		self.waitUntilCalled(cb)

class AsyncUpdateWithEmptyDesignDocTests(AsyncPouchDBTestCaseWithDB):
	def setUp(self):
		super(AsyncUpdateWithEmptyDesignDocTests, self).setUp()

		def cb(err, resp):
			pass

		self._db.put({"_id": "_design/test"}, cb)
		self.waitUntilCalled(cb)

	def testBasic(self):
		def cb(err, resp):
			self.assertEqual(err["status"], 404)
			self.assertEqual(err["name"], "not_found")
			self.assertEqual(err["message"], "missing update function unexisting on design doc _design/test")

		self._db.update("test/unexisting", cb)
		self.waitUntilCalled(cb)

class AsyncRewriteTests(AsyncPouchDBTestCaseWithDB):
	def setUp(self):
		super(AsyncRewriteTests, self).setUp()

		self._db.put(REWRITE_DOCUMENT, self.cb)
		self.waitUntilCalled(self.cb)

	def testBasicUrl(self):
		def cb(err, req):
			self.assertEqual(req.raw_path, "/test/_design/test/_list/test/ids?k=v")
		self._db.rewriteResultRequestObject("test/test/all", cb, query={"k": "v"})
		self.waitUntilCalled(cb)

	def testBasicResp(self):
		def cb(err, resp):
			self.assertEqual(err["status"], 400)
			self.assertEqual(err["name"], "not_found")
			self.assertIn("view named ids", err["message"])

		self._db.rewrite("test/test/all", cb)
		self.waitUntilCalled(cb)

class SyncRewriteTests(SyncPouchDBTestCaseWithDB):
	def putRewrite(self, rewrite):
		return self._db.put({
			"_id": "_design/test",
			"rewrites": [rewrite],
		})

	def testHighUpPath(self):
		self.putRewrite({
			"from": "/highup",
			#should be sufficiently high up.
			"to": "../../../../../..",
		})
		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.rewrite("test/highup")

		self.assertEqual(cm.exception["status"], 404)
		self.assertEqual(cm.exception["message"], "missing")

	def testBadPath(self):
		self.putRewrite({"from": "/badpath", "to": "../../a/b/c"})
		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.rewrite("test/badpath")
		self.assertEqual(cm.exception["status"], 404)

	def testAttachmentRewrite(self):
		ddocResp = self.putRewrite({"from": "/attachment", "to": "/attachment"})
		#test if put succeeds
		resp = self._db.rewrite(
			"test/attachment/",
			method="PUT",
			withValidation=True,
			body=pouchdb.context.Blob(b"Hello World!"),
			headers={"Content-Type": "text/plain"},
			query={"rev": ddocResp.rev}
		)
		self.assertTrue(resp.ok)

		#test if delete succeeds
		resp2 = self._db.rewrite(
			"test/attachment",
			method="DELETE",
			withValidation=False,
			query={"rev": resp.rev}
		)
		self.assertTrue(resp2.ok)

		#test if post gives a 405
		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.rewrite(
				"/test/attachment",
				method="POST",
				#not sure if it would be required. Playing safe here.
				#Not that it should ever reach the rev check.
				query={"rev": resp2.rev}
			)
		self.assertEqual(cm.exception["status"], 405)
		self.assertEqual(cm.exception["name"], "method_not_allowed")
		self.assertIn("POST", cm.exception["message"])

	def testLocalDocRewrite(self):
		self.putRewrite({"from": "/doc", "to": ".././../_local/test"})
		resp = self._db.rewrite("test/doc", method="PUT", body='{"_id": "test"}', withValidation=True)
		self.assertTrue(resp.ok)

	def testAllDbsRewrite(self):
		self.putRewrite({"from": "/alldbs", "to": "../../../_all_dbs"})
		resp = self._db.rewrite("test/alldbs")
		self.assertIsInstance(resp, collections.Sequence)

		resp2 = self._db.rewriteResultRequestObject("test/alldbs")
		self.assertEqual(resp2["path"], ["_all_dbs"])

	def testPostDocRewrite(self):
		self.putRewrite({"from": "postdoc", "to": "../../", "method": "POST"})

		resp = self._db.rewrite("test/postdoc", body="{}", method="POST")
		self.assertUuid(resp.id)
		self.assertTrue(resp.rev.startswith("1-"))
		self.assertTrue(resp.ok)

		resp2 = self._db.rewrite("test/postdoc", body="{}", method="POST", withValidation=True)
		self.assertUuid(resp2.id)
		self.assertTrue(resp2.rev.startswith("1-"))
		self.assertTrue(resp2.ok)

class SyncCouchDBBasedRewriteTests(unittest.TestCase):
	"""Based on CouchDB's rewrite test suite: rewrite.js. Not every test
	has yet been ported, but a large amount has been.

	Original test source:
	https://github.com/apache/couchdb/blob/master/share/www/script/test/rewrite.js

	"""
	@classmethod
	def setUpClass(cls):
		cls._env = alt_setup()
		cls._db = cls._env.PouchDB("test")

		designDoc = {
			"_id": "_design/test",
			"language": "javascript",
			"_attachments": {
				"foo.txt": {
					"content_type": "text/plain",
					"data": "VGhpcyBpcyBhIGJhc2U2NCBlbmNvZGVkIHRleHQ=",
				},
			},
			"rewrites": [
				{
					"from": "foo",
					"to": "foo.txt"
				},
				{
					"from": "foo2",
					"to": "foo.txt",
					"method": "GET",
				},
				{
					"from": "hello/:id",
					"to": "_update/hello/:id",
					"method": "PUT",
				},
				{
					"from": "/welcome",
					"to": "_show/welcome",
				},
				{
					"from": "/welcome/:name",
					"to": "_show/welcome",
					"query": {
						"name": ":name",
					},
				},
				{
					"from": "/welcome2",
					"to": "_show/welcome",
					"query": {
						"name": "user",
					},
				},
				{
					"from": "/welcome3/:name",
					"to": "_update/welcome2/:name",
					"method": "PUT",
				},
				{
					"from": "/welcome3/:name",
					"to": "_show/welcome2/:name",
					"method": "GET",
				},
				{
					"from": "/welcome4/*",
					"to" : "_show/welcome3",
					"query": {
						"name": "*",
					},
				},
				{
					"from": "/welcome5/*",
					"to" : "_show/*",
					"query": {
						"name": "*",
					},
				},
				{
					"from": "basicView",
					"to": "_view/basicView",
				},
				{
					"from": "simpleForm/basicView",
					"to": "_list/simpleForm/basicView",
				},
				{
					"from": "simpleForm/basicViewFixed",
					"to": "_list/simpleForm/basicView",
					"query": {
						"startkey": 3,
						"endkey": 8,
					},
				},
				{
					"from": "simpleForm/basicViewPath/:start/:end",
					"to": "_list/simpleForm/basicView",
					"query": {
						"startkey": ":start",
						"endkey": ":end",
					},
					"formats": {
						"start": "int",
						"end": "int",
					},
				},
				{
					"from": "simpleForm/complexView",
					"to": "_list/simpleForm/complexView",
					"query": {
						"key": [1, 2],
					},
				},
				{
					"from": "simpleForm/complexView2",
					"to": "_list/simpleForm/complexView",
					"query": {
						"key": ["test", {}],
					},
				},
				{
					"from": "simpleForm/complexView3",
					"to": "_list/simpleForm/complexView",
					"query": {
						"key": ["test", ["test", "essai"]],
					},
				},
				{
					"from": "simpleForm/complexView4",
					"to": "_list/simpleForm/complexView2",
					"query": {
						"key": {"c": 1}
					},
				},
				{
					"from": "simpleForm/complexView5/:a/:b",
					"to": "_list/simpleForm/complexView3",
					"query": {
						"key": [":a", ":b"],
					},
				},
				{
					"from": "simpleForm/complexView6",
					"to": "_list/simpleForm/complexView3",
					"query": {
						"key": [":a", ":b"],
					},
				},
				{
					"from": "simpleForm/complexView7/:a/:b",
					"to": "_view/complexView3",
					"query": {
						"key": [":a", ":b"],
						"include_docs": ":doc",
					},
					"format": {
						"doc": "bool",
					},
				},
				{
					"from": "/",
					"to": "_view/basicView",
				},
				{
					"from": "/db/*",
					"to": "../../*",
				},
			],
			"lists": {
				"simpleForm": r"""function(head, req) {
					log("simpleForm");
					send('<ul>');
					var row, row_number = 0, prevKey, firstKey = null;
					while (row = getRow()) {
						row_number += 1;
						if (!firstKey) firstKey = row.key;
						prevKey = row.key;
						send('\n<li>Key: '+row.key
								 +' Value: '+row.value
								 +' LineNo: '+row_number+'</li>');
					}
					return '</ul><p>FirstKey: '+ firstKey + ' LastKey: '+ prevKey+'</p>';
				}""",
			},
			"shows": {
				"welcome": """function(doc,req) {
					return "Welcome " + req.query["name"];
				}""",
				"welcome2": """function(doc, req) {
					return "Welcome " + doc.name;
				}""",
				"welcome3": """function(doc,req) {
					return "Welcome " + req.query["name"];
				}""",
			},
			"updates": {
				"hello": """function(doc, req) {
					if (!doc) {
						if (req.id) {
							return [{
								_id : req.id
							}, "New World"]
						}
						return [null, "Empty World"];
					}
					doc.world = "hello";
					doc.edited_by = req.userCtx;
					return [doc, "hello doc"];
				}""",
				"welcome2": """function(doc, req) {
					if (!doc) {
						if (req.id) {
							return [{
								_id: req.id,
								name: req.id
							}, "New World"]
						}
						return [null, "Empty World"];
					}
					return [doc, "hello doc"];
				}""",
			},
			"views": {
				"basicView": {
					"map": """function(doc) {
						if (doc.integer) {
							emit(doc.integer, doc.string);
						}
						
					}""",
				},
				"complexView": {
					"map": """function(doc) {
						if (doc.type == "complex") {
							emit([doc.a, doc.b], doc.string);
						}
					}"""
				},
				"complexView2": {
					"map": """function(doc) {
						if (doc.type == "complex") {
							emit(doc.a, doc.string);
						}
					}""",
				},
				"complexView3": {
					"map": """function(doc) {
						if (doc.type == "complex") {
							emit(doc.b, doc.string);
						}
					}""",
				},
			},
		}

		def makeDocs(start, end):
			docs = []
			for i in range(start, end):
				docs.append({
					"_id": str(i),
					"integer": i,
					"string": str(i),
				})
			return docs

		docs1 = makeDocs(0, 10)
		docs2 = [
			{"a": 1, "b": 1, "string": "doc 1", "type": "complex"},
			{"a": 1, "b": 2, "string": "doc 2", "type": "complex"},
			{"a": "test", "b": {}, "string": "doc 3", "type": "complex"},
			{"a": "test", "b": ["test", "essai"], "string": "doc 4", "type": "complex"},
			{"a": {"c": 1}, "b": "", "string": "doc 5", "type": "complex"},
		]
		cls._db.bulkDocs({"docs": [designDoc] + docs1 + docs2})

	@classmethod
	def tearDownClass(cls):
		cls._db.destroy()

	def testSimpleRewriting(self):
		#GET is the default http method
		resp = self._db.rewrite("test/foo");
		self.assertEqual(resp.data, b"This is a base64 encoded text")
		self.assertEqual(resp.type, "text/plain")

		resp2 = self._db.rewrite("test/foo2")
		self.assertEqual(resp2.data, b"This is a base64 encoded text")
		self.assertEqual(resp2.type, "text/plain")

	def testBasicUpdate(self):
		#hello update world
		doc = {"word":"plankton", "name":"Rusty"}
		resp = self._db.post(doc)
		self.assertTrue(resp.ok)
		docid = resp.id

		resp = self._db.rewrite("test/hello/" + docid, method="PUT")
		self.assertEqual(resp.code, 201)
		self.assertEqual(resp.body, "hello doc")
		self.assertIn("charset=utf-8", resp.headers["Content-Type"])

		doc = self._db.get(docid)
		self.assertEqual(doc.world, "hello")

	def testBasicShow(self):
		resp = self._db.rewrite("test/welcome", query={"name": "user"})
		self.assertEqual(resp.body, "Welcome user")

		resp = self._db.rewrite("test/welcome/user")
		self.assertEqual(resp.body, "Welcome user")

		resp = self._db.rewrite("test/welcome2")
		self.assertEqual(resp.body, "Welcome user")

	def testWelcome3Test(self):
		resp = self._db.rewrite("test/welcome3/test", method="PUT")
		self.assertEqual(resp.code, 201)
		self.assertEqual(resp.body, "New World")
		self.assertIn("charset=utf-8", resp.headers["Content-Type"])

		resp = self._db.rewrite("test/welcome3/test")
		self.assertEqual(resp.body, "Welcome test")

	def testWelcome4User(self):
		resp = self._db.rewrite("test/welcome4/user")
		self.assertEqual(resp.body, "Welcome user")

	def testWelcome5Welcome3(self):
		resp = self._db.rewrite("test/welcome5/welcome3")
		self.assertEqual(resp.body, "Welcome welcome3")

	def testBasicView(self):
		resp = self._db.rewrite("test/basicView")
		self.assertEqual(resp.total_rows, 9)

	def testRootRewrite(self):
		resp = self._db.rewrite("test/")
		self.assertEqual(resp.total_rows, 9)

	def testSimpleFormBasicView(self):
		resp = self._db.rewrite("test/simpleForm/basicView", query={"startkey": 3, "endkey": 8})
		self.assertEqual(resp.code, 200, "with query params")
		self.assertNotIn("Key: 1", resp.body)
		self.assertIn("FirstKey: 3", resp.body)
		self.assertIn("LastKey: 8", resp.body)

	def testSimpleFormBasicViewFixed(self):
		resp = self._db.rewrite("test/simpleForm/basicViewFixed")
		self.assertEqual(resp.code, 200, "with query params")
		self.assertNotIn("Key: 1", resp.body)
		self.assertIn("FirstKey: 3", resp.body)
		self.assertIn("LastKey: 8", resp.body)

	def testSimpleFormBasicViewFixedDifferentQuery(self):
		resp = self._db.rewrite("test/simpleForm/basicViewFixed", query={"startkey": 4})
		self.assertEqual(resp.code, 200, "with query params")
		self.assertNotIn("Key: 1", resp.body)
		self.assertIn("FirstKey: 3", resp.body)
		self.assertIn("LastKey: 8", resp.body)

	def testSimpleViewBasicViewPath(self):
		resp = self._db.rewrite("test/simpleForm/basicViewPath/3/8")
		self.assertNotIn("Key: 1", resp.body)
		self.assertIn("FirstKey: 3", resp.body)
		self.assertIn("LastKey: 8", resp.body)

	def testSimpleFormComplexView(self):
		resp = self._db.rewrite("test/simpleForm/complexView")
		self.assertEqual(resp.code, 200, "with query params")
		self.assertRegexpMatches(resp.body, "FirstKey: [1, 2]")

	def testSimpleFormComplexView2(self):
		resp = self._db.rewrite("test/simpleForm/complexView2")
		self.assertEqual(resp.code, 200, "with query params")
		self.assertIn("Value: doc 3", resp.body)

	def testSimpleFormComplexView3(self):
		resp = self._db.rewrite("test/simpleForm/complexView3")
		self.assertEqual(resp.code, 200, "with query params")
		self.assertIn("Value: doc 4", resp.body)

	def testSimpleFormComplexView4(self):
		resp = self._db.rewrite("test/simpleForm/complexView4")
		self.assertEqual(resp.code, 200, "with query params")
		self.assertIn("Value: doc 5", resp.body)

	def testSimpleFormComplexView5WithArgs(self):
		resp = self._db.rewrite("test/simpleForm/complexView5/test/essai")
		self.assertEqual(resp.code, 200, "with query params")
		self.assertIn("Value: doc 4", resp.body)

	def testComplexView6WithQuery(self):
		resp = self._db.rewrite("test/simpleForm/complexView6", query={"a": "test", "b": "essai"})
		self.assertEqual(resp.code, 200, "with query params")
		self.assertIn("Value: doc 4", resp.body)

	def testSimpleFormComplexView7WithArgsAndQuery(self):
		resp = self._db.rewrite("test/simpleForm/complexView7/test/essai", query={"doc": True})
		self.assertIsInstance(resp.rows[0].doc, collections.Mapping)

	def testDbWithArgs(self):
		#The original test suite uses the 'meta' query parameter which
		#PouchDB doesn't implement. revs_info could just be dropped in
		#without further changes, though.
		resp = self._db.rewrite("test/db/_design/test", query={"revs_info": True})
		self.assertEqual(resp._id, "_design/test")
		self.assertIsInstance(resp._revs_info, collections.Sequence)

class SyncRewriteTestsWithInvalidDesignDoc(SyncPouchDBTestCaseWithDB):
	def testEmptyDesignDoc(self):
		self._db.put({"_id": "_design/test"})

		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.rewrite("test/test/all")

		self.assertEqual(cm.exception["status"], 404)
		self.assertEqual(cm.exception["name"], "rewrite_error")
		self.assertEqual(cm.exception["message"], "Invalid path.")

	def testInvalidRewrites(self):
		self._db.put({"_id": "_design/test", "rewrites": "Hello World!"})

		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.rewrite("test/test/all")

		self.assertEqual(cm.exception["status"], 400)
		self.assertEqual(cm.exception["name"], "rewrite_error")

	def testMissingTo(self):
		self._db.put({"_id": "_design/test", "rewrites": [
			{"from": "*"},
		]})

		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.rewrite("test/test/all")

		self.assertEqual(cm.exception["status"], 500)
		self.assertEqual(cm.exception["name"], "error")
		self.assertEqual(cm.exception["message"], "invalid_rewrite_target")

	def testEmptyRewrites(self):
		self._db.put({"_id": "_design/test", "rewrites": []})

		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.rewrite("test/test/all")

		self.assertEqual(cm.exception["status"], 404)
		self.assertEqual(cm.exception["name"], "not_found")
		self.assertEqual(cm.exception["message"], "missing")
