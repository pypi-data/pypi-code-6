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

import json
import os
import unittest
import pouchdb
import pouchdb.utils
import shutil

FAST_ONLY = bool(int(os.environ.get("TEST_FAST", "0")))

configPath = os.path.join(os.path.dirname(__file__), "testconfig.json")
try:
	with open(configPath) as f: #pragma: no branch
		data = json.load(f)
except IOError: #pragma: no cover
	data = {}

USERNAME = data.get("username")
PASSWORD = data.get("password")
BASE_URL = data.get("base_url", "http://localhost:5984")
STORAGE_DIR = data.get("storage_dir", "dbs")

with pouchdb.utils.suppress(OSError):
	#to prevent the allDbs plug-in from slowing the whole thing down
	#too much.
	os.remove(os.path.join(STORAGE_DIR, "Databases.db"))
	shutil.rmtree(os.path.join(STORAGE_DIR, "http_localhost_5984"))

HTTP_AUTH = None
if USERNAME: #pragma: no branch
	HTTP_AUTH = {
		"username": USERNAME,
		"password": PASSWORD,
	}

def alt_setup(*args, **kwargs):
	kwargs["storageDir"] = STORAGE_DIR
	kwargs["baseUrl"] = BASE_URL
	return pouchdb.setup(*args, **kwargs)

tearDownHandlers = set()

class PouchDBTestCase(unittest.TestCase):
	def setUp(self):
		self._env = alt_setup(async=self.async)
		#the large amount of dbs seem to need this.
		self._env.setMaxListeners(100)
		self.waitUntilCalled = self._env.context.waitUntilCalled

	def tearDown(self):
		"""Allows external code to hook in on tearDown. Used for JS
		coverage

		"""
		for handler in tearDownHandlers: #pragma: no cover
			handler(self._env)

	def assertUuid(self, uuid):
		self.assertIsInstance(uuid, basestring)
		self.assertTrue(len(uuid) > 30)

	def assertPromise(self, promise):
		self.assertIn("then", promise)
		self.assertIn("catch", promise)

	def assertWebKitUserAgent(self, ua):
		self.assertIn("Mozilla", ua)
		self.assertIn("AppleWebKit", ua)
		self.assertIn("KHTML", ua)
		self.assertIn("Gecko", ua)

class SyncPouchDBTestCase(PouchDBTestCase):
	"""Resets the context after running a test"""

	async = False

class AsyncPouchDBTestCase(PouchDBTestCase):
	"""Resets the context after running a test"""

	async = True

	def destroy(self, db):
		def cb(err, resp):
			self.assertIsNone(err)

		if isinstance(db, pouchdb.AsyncPouchDB):
			self._db.destroy(cb)
		else:
			db = self._env.destroy(db, cb)
		self.waitUntilCalled(cb)

	def cb(self, *args, **kwargs):
		"""Can be used when you don't care about the result, but do need
		to wait using waitUntilCalled. This way you don't have to define
		your own function for every test.

		"""

class SyncPouchDBTestCaseWithDB(SyncPouchDBTestCase):
	"""Sets up a db named 'test' and resets the context afterwards."""

	def setUp(self):
		super(SyncPouchDBTestCaseWithDB, self).setUp()

		self._db = self._env.PouchDB("test")

	def tearDown(self):
		super(SyncPouchDBTestCaseWithDB, self).tearDown()

		self._db.destroy()

class AsyncPouchDBTestCaseWithDB(AsyncPouchDBTestCase):
	"""Sets up a db named 'test' and resets the context afterwards."""

	def setUp(self):
		super(AsyncPouchDBTestCaseWithDB, self).setUp()

		self._db = self._env.PouchDB("test")

	def tearDown(self):
		super(AsyncPouchDBTestCaseWithDB, self).tearDown()

		self.destroy(self._db)

class SyncPouchDBTestCaseWithDBAndDoc(SyncPouchDBTestCaseWithDB):
	"""Sets up a db named 'test', a document named 'mytest' and resets
	   the context afterwards.

	"""
	def setUp(self):
		super(SyncPouchDBTestCaseWithDBAndDoc, self).setUp()

		resp = self._db.put({"_id": "mytest", "test": True})
		self.rev = resp["rev"]

class AsyncPouchDBTestCaseWithDBAndDoc(AsyncPouchDBTestCaseWithDB):
	"""Sets up a db named 'test', a document named 'mytest' and resets
	   the context afterwards.

	"""
	def setUp(self):
		super(AsyncPouchDBTestCaseWithDBAndDoc, self).setUp()

		def callback(err, resp):
			self.rev = resp["rev"]

		self._db.put({"_id": "mytest", "test": True}, callback)
		self.waitUntilCalled(callback)

class SyncPouchDBTestCaseWithDBAndAttachment(SyncPouchDBTestCaseWithDB):
	"""Sets up a db named 'test', and adds a document named
	   'attachment_test' with an attachment named 'text' inside.
	   Afterwards, it resets the context.

	"""
	def setUp(self):
		super(SyncPouchDBTestCaseWithDBAndAttachment, self).setUp()

		resp = self._db.putAttachment("attachment_test", "text", b"abcd", "text/plain")
		self.rev = resp["rev"]

class AsyncPouchDBTestCaseWithDBAndAttachment(AsyncPouchDBTestCaseWithDB):
	"""Sets up a db named 'test', and adds a document named
	   'attachment_test' with an attachment named 'text' inside.
	   Afterwards, it resets the context.

	"""
	def setUp(self):
		super(AsyncPouchDBTestCaseWithDBAndAttachment, self).setUp()

		def cb(resp):
			self.rev = resp["rev"]

		self._db.putAttachment("attachment_test", "text", b"abcd", "text/plain").then(cb)
		self.waitUntilCalled(cb)

class SyncPouchDBHTTPTestCase(SyncPouchDBTestCase):
	"""Sets up a db named 'test', on the for the tests specified CouchDB
	instance, and removes it at the end.

	"""
	def setUp(self):
		super(SyncPouchDBHTTPTestCase, self).setUp()

		self._db = self._env.PouchDB(BASE_URL + "/test", auth=HTTP_AUTH)

	def tearDown(self):
		self._db.destroy()

class AsyncPouchDBHTTPTestCase(AsyncPouchDBTestCase):
	"""Sets up a db named 'test', on the for the tests specified CouchDB
	instance, and removes it at the end.

	"""
	def setUp(self):
		super(AsyncPouchDBHTTPTestCase, self).setUp()

		self._db = self._env.PouchDB(BASE_URL + "/test", auth=HTTP_AUTH)

	def tearDown(self):
		self.destroy(self._db)
