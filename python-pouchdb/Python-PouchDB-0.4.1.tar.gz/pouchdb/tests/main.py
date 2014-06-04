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
	SyncPouchDBTestCase,
	SyncPouchDBTestCaseWithDB,
	SyncPouchDBTestCaseWithDBAndDoc,
	SyncPouchDBTestCaseWithDBAndAttachment,
	SyncPouchDBHTTPTestCase,

	AsyncPouchDBTestCase,
	AsyncPouchDBTestCaseWithDB,
	AsyncPouchDBTestCaseWithDBAndDoc,
	AsyncPouchDBTestCaseWithDBAndAttachment,
	AsyncPouchDBHTTPTestCase,

	BASE_URL,
	HTTP_AUTH,
	FAST_ONLY,
	USERNAME,
	PASSWORD
)

import pouchdb
import unittest
import requests
import numbers
import warnings
import json

BULK_DOCS = {
	"docs": [
		{
			"a": 1,
			"b": 2,
		},
		{
			
			"c": 3,
			"d": 4,
		},
	],
}

QUERY_FUNC = {
	"map": """function (doc) {
		emit(null, doc._rev);
	}""",
}

REVS_DIFF_DATA = {
	"myDoc1": [
		"1-b2e54331db828310f3c772d6e042ac9c",
		"2-3a24009a9525bde9e4bfa8a99046b00d",
	],
}

class AuthenticationMixin(object):
	_username = "python_pouchdb_test"
	_password = "thePassword"
	_metadata = {"updated": "02-02-2002"}

class SyncDestroyTests(SyncPouchDBTestCaseWithDBAndDoc):
	def testInstanceDestroy(self):
		self.assertTrue(self._db.destroy()["ok"])
		db = self._env.PouchDB("test")
		with self.assertRaises(pouchdb.PouchDBError) as cm:
			db.get("mytest")
		self.assertEqual(cm.exception["status"], 404)

	def testGlobalDestroy(self):
		self.assertIsNone(self._env.destroy("test"))
		db = self._env.PouchDB("test")
		with self.assertRaises(pouchdb.PouchDBError) as cm:
			db.get("mytest")
		self.assertEqual(cm.exception["status"], 404)

	def testGlobalNoName(self):
		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._env.destroy()

class AsyncDestroyTests(AsyncPouchDBTestCaseWithDBAndDoc):
	def testInstanceDestroy(self):
		def callback(err, resp):
			self.assertFalse(err)

			db = self._env.PouchDB("test")
			def getCallback(err, resp):
				self.assertEqual(err["status"], 404)
			db.get("mytest", getCallback)
			self.waitUntilCalled(getCallback)

		self._db.destroy(callback)
		self.waitUntilCalled(callback)

	def testGlobalDestroy(self):
		def callback(err, resp):
			self.assertFalse(err)

			db = self._env.PouchDB("test")
			def getCallback(err, resp):
				self.assertEqual(err["status"], 404)
			db.get("mytest", getCallback)
			self.waitUntilCalled(getCallback)

		self._env.destroy("test", callback)
		self.waitUntilCalled(callback)

	def testGlobalDestroyWithNameOption(self):
		def getCallback(err, resp):
			self.assertEqual(err["status"], 404)

		def callback(err, resp):
			self.assertFalse(err)

			db = self._env.PouchDB("test")
			db.get("mytest", getCallback)

		self._env.destroy(callback, name="test")
		self.waitUntilCalled(getCallback)

class SyncPutTests(SyncPouchDBTestCaseWithDB):
	def testSimplePut(self):
		resp = self._db.put({"_id": "mytest", "test": True})
		self.assertEqual(resp["id"], "mytest")

	def testJsonPut(self):
		resp = self._db.put('{"_id": "mytest", "test": true}')
		self.assertEqual(resp["id"], "mytest")

class AsyncPutTests(AsyncPouchDBTestCaseWithDB):
	def testAsyncPut(self):
		result = {}
		def callback(err, resp):
			result["err"] = err
			result["resp"] = resp
		self._db.put({"_id": "abcd", "something": 26}, callback)
		self.assertFalse(result)
		self.waitUntilCalled(callback)
		self.assertTrue(result["resp"]["ok"])

	def testPutProvidingId(self):
		def cb(err, resp):
			self.assertEqual(resp.id, "mytest")
		self._db.put({}, "mytest", cb)
		self.waitUntilCalled(cb)

class SyncPostTests(SyncPouchDBTestCaseWithDB):
	def testSimplePost(self):
		self.assertTrue(self._db.post({"test": False})["ok"])

class AsyncPostTests(AsyncPouchDBTestCaseWithDB):
	def testSimplePost(self):
		def callback(resp):
			assert resp["ok"]
		self._db.post({"test": False}).then(callback)
		self.waitUntilCalled(callback)

class SyncGetTests(SyncPouchDBTestCaseWithDBAndDoc):
	def testSimpleGet(self):
		doc = self._db.get("mytest")
		self.assertEqual(doc["_id"], "mytest")

	def testMissingDoc(self):
		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.get("unexisting-doc")
		self.assertEqual(cm.exception["status"], 404)
		self.assertIn("404", str(cm.exception))

class AsyncGetTests(AsyncPouchDBTestCaseWithDBAndDoc):
	def testSimpleGet(self):
		def cb(doc):
			self.assertEqual(doc["_id"], "mytest")
		self._db.get("mytest").then(cb)
		self.waitUntilCalled(cb)

class SyncRemoveTests(SyncPouchDBTestCaseWithDBAndDoc):
	def testSimpleRemove(self):
		doc = self._db.get("mytest")
		self.assertTrue(self._db.remove(doc)["ok"])
		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.get("mytest")
		self.assertEqual(cm.exception["status"], 404)

class AsyncRemoveTests(AsyncPouchDBTestCaseWithDBAndDoc):
	def testSimpleRemove(self):
		def removeCb(resp):
			self.assertTrue(resp["ok"])

		def getCb(doc):
			self._db.remove(doc).then(removeCb)

		self.assertPromise(self._db.get("mytest").then(getCb))
		self.waitUntilCalled(removeCb)

class SyncBulkDocsTests(SyncPouchDBTestCaseWithDB):
	def testSimpleBulkDocs(self):
		resp = self._db.bulkDocs(BULK_DOCS)
		self.assertEqual(len(resp), 2)

class AsyncBulkDocsTests(AsyncPouchDBTestCaseWithDB):
	def testSimpleBulkDocs(self):
		def cb(err, resp):
			self.assertEqual(len(resp), 2)

		self.assertPromise(self._db.bulkDocs(BULK_DOCS, cb))
		self.waitUntilCalled(cb)

class SyncAllDocsTests(SyncPouchDBTestCaseWithDB):
	def testAllDocsWithEmptyDB(self):
		resp = self._db.allDocs(include_docs=True)
		self.assertEqual(len(resp["rows"]), 0)

	def testAllDocsWithNonEmptyDB(self):
		self._db.post({})

		resp = self._db.allDocs(include_docs=True)
		self.assertEqual(len(resp["rows"]), 1)

class AsyncAllDocsTests(AsyncPouchDBTestCaseWithDB):
	def testAllDocsWithEmptyDB(self):
		def cb(err, resp):
			self.assertEqual(len(resp["rows"]), 0)

		self.assertPromise(self._db.allDocs(cb))
		self.waitUntilCalled(cb)

class SyncChangesTests(SyncPouchDBTestCaseWithDBAndDoc):
	def testSimple(self):
		self.assertEqual(len(self._db.changes()["results"][0]["changes"]), 1)

	def testLive(self):
		def cb(err, resp):
			self.assertEqual(resp["status"], "cancelled")
		promise = self._db.changes(live=True, complete=cb)
		self.assertIsNone(promise.cancel())
		self.waitUntilCalled(cb)

class AsyncChangesTests(AsyncPouchDBTestCaseWithDBAndDoc):
	def testAsync(self):
		data = {}
		def onComplete(err, resp):
			data["err"] = err
			data["resp"] = resp
		self.assertPromise(self._db.changes(complete=onComplete))
		self.waitUntilCalled(onComplete)
		self.assertIn("last_seq", data["resp"])

	def testLive(self):
		def cb(err, resp):
			self.assertEqual(resp["status"], "cancelled")
		promise = self._db.changes(live=True, complete=cb)
		self.assertIsNone(promise.cancel())
		self.waitUntilCalled(cb)

class SyncReplicateTests(SyncPouchDBTestCaseWithDBAndDoc):
	def testSimpleReplicate(self):
		resp = self._env.replicate("test", "testb")
		self.assertTrue(resp["ok"])

	def testLocalSync(self):
		resp = self._db.sync("testb")
		self.assertTrue(resp["pull"]["ok"])
		self.assertTrue(resp["push"]["ok"])

	def testGlobalSync(self):
		resp = self._env.sync("test", "testb")
		self.assertTrue(resp["pull"]["ok"])
		self.assertTrue(resp["push"]["ok"])

	def testSimpleReplicateTo(self):
		self.assertTrue(self._db.replicate_to("testb")["ok"])
		db = self._env.PouchDB("testb")
		#this should not throw a PouchDBError
		self.assertTrue(db.get("mytest")["test"])

	def testSimpleReplicateFrom(self):
		self.assertTrue(self._db.replicate_from("testb")["ok"])

	def testLive(self):
		resp = self._db.replicate_to("testb", live=True)
		self.assertIsNone(resp["cancel"]())

		resp2 = self._db.replicate_from("testb", live=True)
		self.assertIsNone(resp2["cancel"]())

		resp3 = self._env.replicate("test", "testb", live=True)
		self.assertIsNone(resp3["cancel"]())

	def tearDown(self):
		super(SyncReplicateTests, self).tearDown()

		self._env.destroy("testb")

class AsyncReplicateTests(AsyncPouchDBTestCaseWithDBAndDoc):
	def testReplicateWithOnComplete(self):
		result = {}
		def onComplete(err, resp):
			result["err"] = err
			result["resp"] = resp

		promise = self._env.replicate("test", "testb", complete=onComplete)
		self.assertFalse(promise["cancelled"])
		self.waitUntilCalled(onComplete)
		self.assertEqual(result["resp"]["docs_written"], 1)

	def testLocalSync(self):
		def cb(err, resp):
			self.assertTrue(resp["pull"]["ok"])
			self.assertTrue(resp["push"]["ok"])
		self._db.sync("testb", cb, complete=cb)
		self.waitUntilCalled(cb)

	def testGlobalSync(self):
		def cb(err, resp):
			self.assertTrue(resp["pull"]["ok"])
			self.assertTrue(resp["push"]["ok"])
		self._env.sync("test", "testb", complete=cb)
		self.waitUntilCalled(cb)

	def testLive(self):
		resp = self._db.replicate_to("testb", live=True)
		self.assertIsNone(resp["cancel"]())

		resp2 = self._db.replicate_from("testb", live=True)
		self.assertIsNone(resp2["cancel"]())

		resp3 = self._env.replicate("test", "testb", live=True)
		self.assertIsNone(resp3["cancel"]())

	def testReplicateFromWithCallback(self):
		result = {}
		def callback(err, resp):
			result["err"] = err
			result["resp"] = resp

		self._db.replicate_from("testb", callback)
		self.waitUntilCalled(callback)
		self.assertEqual(result["resp"]["docs_written"], 0)

	def testReplicateToWithCallback(self):
		result = {}
		def callback(err, resp):
			result["err"] = err
			result["resp"] = resp

		self._db.replicate_to("testb", callback)
		self.waitUntilCalled(callback)
		self.assertEqual(result["resp"]["docs_written"], 1)

	def tearDown(self):
		super(AsyncReplicateTests, self).tearDown()

		self.destroy("testb")

class SyncPutAttachmentTests(SyncPouchDBTestCaseWithDB):
	def testSimplePutAttachment(self):
		resp = self._db.putAttachment("attachment_test", "text", b"abcd", "text/plain")
		self.assertTrue(resp["ok"])

	def testPutTwoAttachmentsInSameDoc(self):
		resp = self._db.putAttachment("attachment_test", "text", b"abcd", "text/plain")
		rev = resp["rev"]
		resp2 = self._db.putAttachment("attachment_test", "text2", u"éfgh".encode("UTF-8"), "text/plain", rev)
		self.assertTrue(resp2["ok"])

class AsyncPutAttachmentTests(AsyncPouchDBTestCaseWithDB):
	def testPutAttachmentAsync(self):
		result = {}
		def putAttachmentCallback(err, resp):
			result["err"] = err
			result["resp"] = resp

		self._db.putAttachment("attachment_test", "text", b"abcd", "text/plain", callback=putAttachmentCallback)
		self.waitUntilCalled(putAttachmentCallback)
		self.assertTrue(result["resp"]["ok"])

class SyncGetAttachmentTests(SyncPouchDBTestCaseWithDBAndAttachment):
	def testSimpleGetAttachment(self):
		resp = self._db.getAttachment("attachment_test", "text")
		self.assertEqual(resp["data"], b"abcd")

	def testMissingDoc(self):
		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.getAttachment("unexisting_doc", "text")
		self.assertEqual(cm.exception["status"], 404)

	def testMissingAttachment(self):
		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.getAttachment("attachment_test", "unexisting_attachment")
		self.assertEqual(cm.exception["status"], 404)

class AsyncGetAttachmentTests(AsyncPouchDBTestCaseWithDBAndAttachment):
	def testGetAttachmentAsync(self):
		result = {}
		def callback(err, resp=None):
			result["err"] = err
			result["resp"] = resp
		self._db.getAttachment("attachment_test", "text", callback)
		self.waitUntilCalled(callback)
		self.assertEqual(result["resp"]["data"], b"abcd")

	def testMissingAttachmentAsync(self):
		result = {}
		def callback(err, resp=None):
			result["err"] = err
			result["resp"] = resp
		self._db.getAttachment("attachment_test", "unexisting_attachment", callback)
		self.waitUntilCalled(callback)
		self.assertEqual(result["err"]["status"], 404)

class SyncRemoveAttachmentTests(SyncPouchDBTestCaseWithDBAndAttachment):
	def testSimpleRemoveAttachment(self):
		resp = self._db.removeAttachment("attachment_test", "text", self.rev)
		self.assertTrue(resp["ok"])

	@unittest.skip("While this might be the expected API, it's not the one PouchDB uses.")
	def testRemoveUnexistingAttachment(self): #pragma: no cover
		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.removeAttachment("attachment_test", "unexisting-attachment", self.rev)
		self.assertEqual(cm.exception["status"], 404)

	def testRemoveAttachmentFromUnexistingDoc(self):
		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.removeAttachment("unexisting-doc", "text", self.rev)
		self.assertEqual(cm.exception["status"], 404)

class AsyncRemoveAttachmentTests(AsyncPouchDBTestCaseWithDBAndAttachment):
	def testRemoveAttachmentAsync(self):
		result = {}
		def callback(err, resp):
			result["err"] = err
			result["resp"] = resp
		self._db.removeAttachment("attachment_test", "text", self.rev, callback)
		self.waitUntilCalled(callback)
		self.assertTrue(result["resp"]["ok"])

	@unittest.skip("While this might be the expected API, it's not the one PouchDB uses.")
	def testRemoveUnexistingAttachmentAsync(self): #pragma: no cover
		result = {}
		def callback(err, resp):
			result["err"] = err
			result["resp"] = resp
		self._db.removeAttachment("attachment_test", "unexisting-attachment", self.rev, callback)
		self.waitUntilCalled(callback)
		self.assertTrue(result["err"]["status"], 404)

	def testRemoveAttachmentFromUnexistingDocAsync(self):
		result = {}
		def callback(err, resp=None):
			result["err"] = err
			result["resp"] = resp
		self._db.removeAttachment("unexisting-doc", "text", self.rev, callback)
		self.waitUntilCalled(callback)
		self.assertTrue(result["err"]["status"], 404)

class SyncQueryTests(SyncPouchDBTestCaseWithDB):
	def testQueryWithEmptyDB(self):
		resp = self._db.query(QUERY_FUNC)
		self.assertEqual(len(resp["rows"]), 0)

	def testAllDocsWithNonEmptyDB(self):
		self._db.post({})

		resp = self._db.query(QUERY_FUNC)
		self.assertEqual(len(resp["rows"]), 1)

class AsyncQueryTests(AsyncPouchDBTestCaseWithDB):
	def testQueryWithEmptyDB(self):
		def cb(resp):
			self.assertEqual(len(resp["rows"]), 0)
		self._db.query(QUERY_FUNC).then(cb)
		self.waitUntilCalled(cb)

class SyncViewCleanupTests(SyncPouchDBTestCaseWithDB):
	def testBasic(self):
		resp = self._db.viewCleanup()
		self.assertTrue(resp["ok"])

class AsyncViewCleanupTests(AsyncPouchDBTestCaseWithDB):
	def testBasic(self):
		def cb(err, resp):
			self.assertTrue(resp["ok"])

		self._db.viewCleanup(cb)
		self.waitUntilCalled(cb)

class InfoVerifierMixin(object):
	def verifyInfo(self, info):
		self.assertIn("update_seq", info)
		self.assertEqual(info["db_name"], "test")

class SyncInfoTests(SyncPouchDBTestCaseWithDB, InfoVerifierMixin):
	def testSimpleInfo(self):
		info = self._db.info()
		self.verifyInfo(info)

class AsyncInfoTests(AsyncPouchDBTestCaseWithDB, InfoVerifierMixin):
	def testInfoAsync(self):
		data = {}
		def callback(err, resp):
			data["err"] = err
			data["resp"] = resp
		self._db.info(callback)
		self.waitUntilCalled(callback)

		self.assertIsNone(data["err"])
		self.verifyInfo(data["resp"])

class SyncCompactTests(SyncPouchDBTestCaseWithDB):
	def testCompactOnEmptyDB(self):
		self.assertIsNone(self._db.compact())

	def testCompactOnNonEmptyDB(self):
		self._db.post({})
		self.assertIsNone(self._db.compact())

class AsyncCompactTests(AsyncPouchDBTestCaseWithDB):
	def testCompactOnEmptyDB(self):
		self.assertPromise(self._db.compact())

class SyncRevsDiffTests(SyncPouchDBTestCaseWithDB):
	def testSimpleRevsDiff(self):
		resp = self._db.revsDiff(REVS_DIFF_DATA)
		#the doc isn't in the db
		self.assertEqual(len(resp["myDoc1"]["missing"]), 2)

class AsyncRevsDiffTests(AsyncPouchDBTestCaseWithDB):
	def testSimpleRevsDiff(self):
		def cb(err, resp):
			#the doc isn't in the db
			self.assertEqual(len(resp["myDoc1"]["missing"]), 2)
		self._db.revsDiff(REVS_DIFF_DATA, cb)
		self.waitUntilCalled(cb)

class EventTests(SyncPouchDBTestCase):
	"""The sync and async implementains are the same (as in, implemented
	   in the base class), so there are no async tests.

	"""
	def tearDown(self):
		self._env.removeAllListeners()

	def testPouchCreatedEvent(self):
		#setup
		resp = {}
		def onCreate(dbName):
			resp["created"] = dbName
		self._env.on("created", onCreate)

		#test created
		self._env.PouchDB("abc")
		if not "created" in resp: #pragma: no cover
			self.waitUntilCalled(onCreate)
		self.assertEqual(resp["created"], "abc")

	def testPouchDestroyedEvent(self):
		#setup
		resp = {}
		def onDestroy(dbName):
			resp["destroyed"] = dbName
		self._env.addListener("destroyed", onDestroy)

		#test destroyed
		self._env.destroy("test")
		if not "destroyed" in resp: #pragma: no cover
			self.waitUntilCalled(onDestroy)
		self.assertEqual(resp["destroyed"], "test")

	def testOnceAndEmit(self):
		data = {"count": 0}
		def cb(i=1):
			data["count"] += i
		self._env.once("test", cb)
		self.assertEqual(data["count"], 0)

		self.assertTrue(self._env.emit("test", 2))
		self.waitUntilCalled(cb)
		self.assertEqual(data["count"], 2)

		self.assertFalse(self._env.emit("test"))
		self.assertEqual(data["count"], 2)

	def testListeners(self):
		#setup
		resp = {"called": False}
		def cb1():
			pass
		def cb2():
			resp["called"] = True
		self._env.on("test", cb1).on("test", cb2)

		listeners = self._env.listeners("test")
		self.assertEqual(len(listeners), 2)
		self.assertFalse(resp["called"])
		for listener in listeners:
			self.assertIsNone(listener())
			self.waitUntilCalled([cb1, cb2])
		self.assertTrue(resp["called"])

	def testSetMaxListeners(self):
		def cb():
			pass #pragma: no cover
		self._env.setMaxListeners(1)
		self._env.on("test", cb)
		with self.assertRaises(self._env.context.JSError) as cm:
			self._env.on("test", cb)
		self.assertIn("possible EventEmitter memory leak detected.", str(cm.exception))

	def testRemoveListener(self):
		called = {"cb1": False, "cb2": False}
		def cb1():
			called["cb1"] = True #pragma: no cover
		def cb2():
			called["cb2"] = True
		self._env.on("test", cb1)
		self._env.on("test", cb2)
		self._env.removeListener("test", cb1)
		self._env.emit("test")
		self.waitUntilCalled(cb2)
		self.assertFalse(called["cb1"])
		self.assertTrue(called["cb2"])

	def testRemoveAllListenersWithArg(self):
		called = {"cb1": False, "cb2": False, "cb3": False}
		def cb1():
			called["cb1"] = True #pragma: no cover
		def cb2():
			called["cb2"] = True #pragma: no cover
		def cb3():
			called["cb3"] = True

		self._env.on("test", cb1)
		self._env.on("test", cb2)
		self._env.on("myTest", cb3)

		self._env.removeAllListeners("test")
		self._env.emit("test")
		self._env.emit("myTest")
		self.waitUntilCalled(cb3)

		self.assertFalse(called["cb1"])
		self.assertFalse(called["cb2"])
		self.assertTrue(called["cb3"])

	def testRemoveAllListenersWithoutArg(self):
		called = {"cb1": False, "cb2": False, "cb3": False}
		def cb1():
			called["cb1"] = True #pragma: no cover
		def cb2():
			called["cb2"] = True #pragma: no cover
		def cb3():
			called["cb3"] = True #pragma: no cover
		self._env.on("test", cb1)
		self._env.on("test", cb2)
		self._env.on("myTest", cb3)

		self._env.removeAllListeners()
		self._env.emit("test")
		self._env.emit("myTest")

		self.assertFalse(called["cb1"])
		self.assertFalse(called["cb2"])
		self.assertFalse(called["cb3"])

class MutableMappingTests(SyncPouchDBTestCaseWithDBAndDoc):
	def testEqual(self):
		#'test' is the same db, but the instances are different
		self.assertTrue(self._db != self._env["test"])
		#same instance
		self.assertTrue(self._db == self._db)

	def testOverwrite(self):
		doc = self._db["mytest"]
		doc["test2"] = "ok"
		self._db["mytest"] = doc

		self.assertTrue(doc["_rev"].startswith("2-"))

@unittest.skipIf(FAST_ONLY, "Too slow.")
class MutableMappingHTTPTests(AuthenticationMixin, SyncPouchDBHTTPTestCase):
	def testNonNotFoundMappingGetError(self):
		#Setup. First make a document to access. Then make a user, and
		#make sure that user isn't allowed to access the document. Then
		#login and request it.
		self._db["abc"] = {}
		signupResp = self._db.sign_up(self._username, self._password)
		try:
			resp = requests.put(BASE_URL + "/test/_security", auth=(USERNAME, PASSWORD), data=json.dumps({
				"members": {
					"names": ["probably-unexisting"]
				}
			}))
			self.assertEqual(resp.status_code, 200)

			self._db.log_in(self._username, self._password)
			#the test:
			with self.assertRaises(pouchdb.PouchDBError) as cm:
				self._db["abc"] #pragma: no branch
			self.assertEqual(cm.exception["status"], 401)
			self.assertIn("not authorized", cm.exception["message"])
		finally:
			userDb = self._env.PouchDB(BASE_URL + "/_users", auth=HTTP_AUTH)
			teardownReq = userDb.remove({
				"_id": signupResp.id,
				"_rev": signupResp.rev
			})
			self.assertTrue(teardownReq["ok"])

	def tearDown(self):
		super(MutableMappingHTTPTests, self).tearDown()

		self._env.context.clearCookies()

@unittest.skipIf(FAST_ONLY, "Too slow.")
class MainHTTPTests(SyncPouchDBHTTPTestCase):
	def testSomeSimpleMethods(self):
		id = self._db.post({"test": True})["id"]
		self.assertTrue(self._db.get(id)["test"])
		self.assertIn(id, str(self._db.allDocs()))

		self.assertIn("db_name", self._db.info())

	def testAttachment(self):
		#Suppress a ResourceWarning requests throws in Python 3.
		warnings.filterwarnings("ignore", message="unclosed")

		rev = self._db.putAttachment("attachment-doc", "attachment", b"<h1>Hello World!</h1>", "text/html")["rev"]

		resp = requests.get(BASE_URL + "/test/attachment-doc/attachment")
		self.assertEqual(resp.content, b"<h1>Hello World!</h1>")
		self.assertEqual(resp.headers["Content-Type"], "text/html")

		a = self._db.getAttachment("attachment-doc", "attachment")
		self.assertEqual(a["data"], b"<h1>Hello World!</h1>")
		self.assertEqual(a["type"], "text/html")

		self._db.removeAttachment("attachment-doc", "attachment", rev)

	def testReplication(self):
		rev = self._db.put({"_id": "mytest"})["rev"]
		self._db.replicate_to("local")

		localDb = self._env.PouchDB("local")
		self.assertEqual(localDb.get("mytest")["_rev"], rev)

class EnvironmentTests(SyncPouchDBTestCase):
	def testInvalidDbName(self):
		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._env.PouchDB(34234)
		self.assertIn("invalid", str(cm.exception))

	def testVersion(self):
		self.assertTrue(self._env.POUCHDB_VERSION)

	@unittest.skipIf(FAST_ONLY, "too sloowwwww")
	def testSecondEnvironmentDifferentDir(self):
		storageDir = "not-the-normal-storage-dir"
		with self.assertRaises(pouchdb.EnvironmentError) as cm:
			pouchdb.setup(storageDir=storageDir)

		#should complain about this property
		self.assertIn("storageDir", str(cm.exception))
		self.assertIn(storageDir, str(cm.exception))

	def testTempDirEnv(self):
		with pouchdb.utils.suppress(pouchdb.EnvironmentError):
			pouchdb.setup()

class ContextTestsWithDb(SyncPouchDBTestCaseWithDB):
	def testDbSizeOfExistingsDB(self):
		size = self._env.context.getDbSize("test")
		self.assertIsInstance(size, numbers.Integral)
		self.assertGreater(size, 0)

	def testDbSizeOfUnexisting(self):
		with self.assertRaises(KeyError):
			self._env.context.getDbSize("unexisting_database")

class ContextTests(SyncPouchDBTestCase):
	@unittest.skipIf(FAST_ONLY, "Too slow.")
	def testInspect(self):
		self._env.context.inspect(block=False)

	def testAttributeError(self):
		with self.assertRaises(AttributeError):
			self._env.context.evalJs("return {}").a

	def testException(self):
		with self.assertRaises(Exception) as cm:
			self._env.context.evalJs("throw new Error('Hello World!')");
		self.assertIn("Hello World!", str(cm.exception))

	def testCircular(self):
		resp = self._env.context.evalJs("var a = {}; a.b = a; return a;")
		self.assertIn("recursion limit reached", str(resp))

	def testDebug(self):
		with self.assertRaises(Exception) as cm:
			self._env.context.evalJs("debug(1, 2);")
		self.assertIn("1,2", str(cm.exception))
		with self.assertRaises(Exception) as cm:
			self._env.context.evalJs("debug(1);")
		self.assertIn("1", str(cm.exception))

class SyncGQLTests(SyncPouchDBTestCaseWithDBAndDoc):
	def testSelectWhereGql(self):
		resp = self._db.gql({"select": "*", "where": "test=true"})
		self.assertEqual(len(resp["rows"]), 1)

	def testInvalidQueryFormat(self):
		with self.assertRaises(pouchdb.PouchDBError) as cm:
			self._db.gql("invalid")
		self.assertEqual(cm.exception["status"], 400)

class AsyncGQLTests(AsyncPouchDBTestCaseWithDBAndDoc):
	def testSelectWhereGql(self):
		def cb(err, resp):
			self.assertEqual(len(resp["rows"]), 1)
		self._db.gql({"select": "*", "where": "test=true"}, cb)
		self.waitUntilCalled(cb)

class SpatialTestsMixin(object):
	_designDoc = {
		'_id': '_design/foo',
		'spatial': {
			'test': 'function(doc) {if (doc.key) {emit(doc.key, doc); }}',
		},
	}
	_docs = [
		_designDoc,
		{'foo': 'bar', 'key': [1]},
		{'_id': 'volatile', 'foo': 'baz', 'key': [2]},
	]

class SyncSpatialTests(SyncPouchDBTestCaseWithDB, SpatialTestsMixin):
	def testSpatial(self):
		"""Based on the first test in the geopouch test suite.

		"""
		self._db.bulkDocs({"docs": self._docs})
		doc = self._db.get("volatile")
		self._db.remove(doc)

		resp = self._db.spatial('foo/test', start_range=[None], end_range=[None])
		self.assertEqual(len(resp["rows"]), 1, msg='Dont include deleted documents')
		for row in resp["rows"]:
			self.assertIn("key", row, msg='view row has a key')
			self.assertIn("_rev", row["value"], msg='emitted doc has rev')
			self.assertIn("_id", row["value"], msg='emitted doc has id')

class AsyncSpatialTests(AsyncPouchDBTestCaseWithDB, SpatialTestsMixin):
	def testSpatial(self):
		"""Based on the first test in the geopouch test suite.

		"""
		def spatialCb(err, resp):
			self.assertIsNone(err)
			self.assertEqual(len(resp["rows"]), 1, msg='Dont include deleted documents')
			for row in resp["rows"]:
				self.assertIn("key", row, msg='view row has a key')
				self.assertIn("_rev", row["value"], msg='emitted doc has rev')
				self.assertIn("_id", row["value"], msg='emitted doc has id')

		def removeCb(resp):
			self._db.spatial('foo/test', spatialCb, start_range=[None], end_range=[None])

		def getCb(doc):
			self._db.remove(doc).then(removeCb)

		def bulkDocsCb(resp):
			self._db.get("volatile").then(getCb)

		self._db.bulkDocs({"docs": self._docs}).then(bulkDocsCb)
		self.waitUntilCalled(spatialCb)

class SearchTestsMixin(object):
	#based on the pouchdb-search test suite
	_doc1 = {
		"_id": "c240s1",
		"chapter": "240",
		"title": "III",
		"href": "/Laws/GeneralLaws/PartIII/TitleIII/Chapter240/Section1",
		"text": "If the record title of land is clouded by an adverse claim, or by the possibility thereof, a person in possession of such land claiming an estate of freehold therein or an unexpired term of not less than ten years, and a person who by force of the covenants in a deed or otherwise may be liable in damages, if such claim should be sustained, may file a petition in the land court stating his interest, describing the land, the claims and the possible adverse claimants so far as known to him, and praying that such claimants may be summoned to show cause why they should not bring an action to try such claim. If no better description can be given, they may be described generally, as the heirs of A B or the like. Two or more persons having separate and distinct parcels of land in the same county and holding under the same source of title, or persons having separate and distinct interests in the same parcel or parcels, may join in a petition against the same supposed claimants. If the supposed claimants are residents of the commonwealth, the petition may be inserted like a declaration in a writ, and served by a copy, like a writ of original summons. Whoever is in the enjoyment of an easement shall be held to be in possession of land within the meaning of this section",
		"section": "1",
		"part": "III",
		"type": "general",
		"desc": "Petition to compel adverse claimant to try title",
	}
	_doc2 = {
		"_id": "c240s10",
		"chapter": "240",
		"title": "III",
		"href": "/Laws/GeneralLaws/PartIII/TitleIII/Chapter240/Section10",
		"text": "After all the defendants have been served with process or notified as provided in section seven and after the appointment of a guardian ad litem or next friend, if such appointment has been made, the court may proceed as though all defendants had been actually served with process. Such action shall be a proceeding in rem against the land, and a judgment establishing or declaring the validity, nature or extent of the plaintiff’s title may be entered, and shall operate directly on the land and have the force of a release made by or on behalf of all defendants of all claims inconsistent with the title established or declared thereby. This and the four preceding sections shall not prevent the court from also exercising jurisdiction in personam against defendants actually served with process who are personally amenable to its judgments",
		"section": "10",
		"part": "III",
		"type": "general",
		"desc": "Proceeding in rem; effect of judgment",
	}
	_doc3 = {
		"_id": "c240s10A",
		"chapter": "240",
		"title": "III",
		"href": "/Laws/GeneralLaws/PartIII/TitleIII/Chapter240/Section10A",
		"text": "The superior court and the land court shall have concurrent jurisdiction of a civil action by any person or persons claiming an estate of freehold, or an unexpired term of not less than ten years, in land subject to a restriction described in section twenty-six of chapter one hundred and eighty-four, to determine and declare whether and in what manner and to what extent and for the benefit of what land the restriction is then enforceable, whether or not a violation has occurred or is threatened. The complaint shall state the names and addresses, so far as known to the plaintiff or plaintiffs, of the owners of the subject parcels as to which the determination is sought, of the owners of any benefited land and of any persons benefited other than persons interested in benefited land. There shall be filed therewith (1) a certified copy of the instrument or instruments imposing the restriction, or of a representative instrument if there are many and the complaint includes a summary of the remainder, and (2) a plan or sketch showing the approximate locations of the parcels as to which the determination is sought, and the other parcel or parcels, if any, which may have the benefit of the restriction, and the ways, public or open to public use, upon which the respective parcels abut or nearest thereto, and the street numbers, if any, of such parcels",
		"section": "10A",
		"part": "III",
		"type": "general",
		"desc": "Restrictions on land; determination; jurisdiction; petition",
	}
	_doc4 = {
		"_id": "_design/find",
		"indexes": {
			"things": {
				"index": """function(doc) {
					if (doc.text) {
						index('default', doc.text);
					}
					if (doc.desc) {
						index('title', doc.desc);
					}
				}""",
			},
		},
	}

	_docs = [_doc1, _doc2, _doc3, _doc4]

class SyncSearchTests(SyncPouchDBTestCaseWithDB, SearchTestsMixin):
	def setUp(self):
		super(SyncSearchTests, self).setUp()

		self._db.bulkDocs({"docs": self._docs})

	def testBasic(self):
		result = self._db.search("find/things", q="freehold")
		self.assertEqual(len(result.rows), 2)
		ids = [v.id for v in result.rows]
		self.assertEqual(ids, ["c240s10A", "c240s1"])

class AsyncSearchTests(AsyncPouchDBTestCaseWithDB, SearchTestsMixin):
	def setUp(self):
		super(AsyncSearchTests, self).setUp()

		def cb(*args):
			pass

		self._db.bulkDocs({"docs": self._docs}, cb)
		self.waitUntilCalled(cb)

	def testBasic(self):
		def searchCb(err, result):
			self.assertIsNone(err)
			self.assertEqual(len(result.rows), 2)
			ids = [v.id for v in result.rows]
			self.assertEqual(ids, ["c240s10A", "c240s1"])

		self._db.search("find/things", searchCb, q="freehold")
		self.waitUntilCalled(searchCb)

@unittest.skipIf(FAST_ONLY, "Too slow.")
class SyncAuthenticationTests(SyncPouchDBHTTPTestCase, AuthenticationMixin):
	def testAuth(self):
		#sign up
		signupResp = self._db.signup(self._username, self._password, metadata=self._metadata)
		self.assertTrue(signupResp["ok"])

		try:
			#log in
			loginResp = self._db.login(self._username, self._password)
			self.assertEqual(loginResp["name"], self._username)

			#login info
			session = self._db.getSession()
			self.assertEqual(session["userCtx"]["name"], self._username)
			user = self._db.getUser(self._username)
			self.assertEqual(user["updated"], self._metadata["updated"])

			#logout
			logoutResp = self._db.logout()
			self.assertTrue(logoutResp["ok"])
		finally:
			userDb = self._env.PouchDB(BASE_URL + "/_users", auth=HTTP_AUTH)
			teardownReq = userDb.remove({
				"_id": signupResp.id,
				"_rev": signupResp.rev
			})
			self.assertTrue(teardownReq["ok"])

	def testAliases(self):
		#sign up
		signupResp = self._db.signUp(self._username, self._password, metadata=self._metadata)
		self.assertTrue(signupResp["ok"])

		try:
			#log in
			loginResp = self._db.logIn(self._username, self._password)
			self.assertEqual(loginResp["name"], self._username)

			#login info - basic test only
			session = self._db.getSession()
			self.assertEqual(session["userCtx"]["name"], self._username)

			#logout
			logoutResp = self._db.logOut()
			self.assertTrue(logoutResp["ok"])
		finally:
			userDb = self._env.PouchDB(BASE_URL + "/_users", auth=HTTP_AUTH)
			teardownReq = userDb.remove({
				"_id": signupResp.id,
				"_rev": signupResp.rev
			})
			self.assertTrue(teardownReq["ok"])

	def tearDown(self):
		super(SyncAuthenticationTests, self).tearDown()

		self._env.context.clearCookies()

@unittest.skipIf(FAST_ONLY, "Too slow.")
class AsyncAuthenticationTests(AsyncPouchDBHTTPTestCase, AuthenticationMixin):
	def tearDown(self):
		super(AsyncAuthenticationTests, self).tearDown()

		def cb(err, resp):
			pass

		if self._signupResp: #pragma: no branch
			userDb = self._env.PouchDB(BASE_URL + "/_users", auth=HTTP_AUTH)
			userDb.remove({
				"_id": self._signupResp.id,
				"_rev": self._signupResp.rev
			}, cb)
			self.waitUntilCalled(cb)

		self._env.context.clearCookies()

	def testAuth(self):	
		"""Handles the actual test."""

		self._signupResp = None

		self._db.signup(self._username, self._password, metadata=self._metadata, callback=self.onSignUp)
		self.waitUntilCalled(self.onLogOut)

	def onSignUp(self, err, resp):
		#for tearDown use
		self._signupResp = resp

		self.assertTrue(resp["ok"])
		self._db.login(self._username, self._password, self.onLogIn)

	def onLogIn(self, err, resp):
		self.assertEqual(resp["name"], self._username)

		self._db.getSession(self.onGetSession)

	def onGetSession(self, err, resp):
		self.assertEqual(resp["userCtx"]["name"], self._username)
		self._db.getUser(self._username, self.onGetUser)

	def onGetUser(self, err, resp):
		self.assertEqual(resp["updated"], self._metadata["updated"])

		self._db.logout(self.onLogOut)

	def onLogOut(self, err, resp):
		self.assertTrue(resp["ok"])

class SyncAllDbsTests(SyncPouchDBTestCase):
	"""Since the allDbs() thing is almost non-deterministic in a test
	suite, we don't really test functionality. Just if the methods don't
	crash. And that's fine: functionality is tested by upstream.

	"""
	def testBasic(self):
		self.assertIsInstance(self._env.allDbs(), list)

	def testReset(self):
		self.assertIsNone(self._env.reset_all_dbs())

	def testLen(self):
		"""__len__ also uses the allDbs plug-in internally."""
		self.assertIsInstance(len(self._env), numbers.Integral)

class AsyncAllDbsTests(AsyncPouchDBTestCase):
	def testAll(self):
		def cb(*args):
			pass
		self._env.allDbs(cb)
		self.waitUntilCalled(cb)
		self._env.resetAllDbs(cb)
		self.waitUntilCalled(cb)

#~ #FIXME: wait for upstream's reaction on this test.
#~ class SyncMemoryAdapterTests(SyncPouchDBTestCase):
	#~ def testBasic(self):
		#~ db = self._env.PouchDB("test", adapter="memory")
		#~ self.assertEqual(len(db.allDocs().rows), 0)
		#~ self.assertTrue(db.post({}).ok)
		#~ self.assertEqual(len(db.allDocs().rows), 1)
#~ 
		#~ db = self._env.PouchDB("test", adapter="memory")
		#~ self.assertEqual(len(db.allDocs().rows), 0)
