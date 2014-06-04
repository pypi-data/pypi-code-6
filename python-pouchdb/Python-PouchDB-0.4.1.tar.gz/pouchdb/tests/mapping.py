# coding=UTF-8
#
#	Copyright 2014, Marten de Vries
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

import pouchdb
import pouchdb.mapping as m
from pouchdb.tests.utils import SyncPouchDBTestCaseWithDB
import datetime
import time
import unittest

class Test(m.Document):
	test = m.TextField(default="Hello World!")

class NoStorageMappingTests(unittest.TestCase):
	def testNonFunctionDefault(self):
		self.assertEqual(Test().test, "Hello World!")

	def testClassAccess(self):
		self.assertIsInstance(Test.test, m.TextField)

	def testUnrecognizedKwarg(self):
		with self.assertRaises(TypeError) as cm:
			Test(unexisting_field="Hi")
		self.assertIn("unexisting_field", str(cm.exception))

	def testDeletingField(self):
		with self.assertRaises(TypeError) as cm:
			del Test().test

		self.assertIn("Can't delete a document field.", str(cm.exception))

	def testTimeField(self):
		class TimeDoc(m.Document):
			time = m.TimeField()

		doc = TimeDoc(time=1000)
		self.assertIsInstance(doc.time, datetime.time)

	def testDateField(self):
		class DateDoc(m.Document):
			#yes, this is a weird way of entering a date. But it's
			#possible.
			date = m.DateField()

		doc = DateDoc(date=time.struct_time((1, 1, 1, 1, 1, 1, 1, 1, 1)))
		self.assertIsInstance(doc.date, datetime.date)

class DocWithViews(m.Document):
	syntaxErrorView = m.ViewField("test", """
		function (doc) {
			emit(doc._id, "hi");
		}}
	""")
	otherView = m.ViewField("test", """
		function (doc) {
			emit(Math.round(Math.random()), 1);
		}
	""", "_sum")

class StorageMappingTests(SyncPouchDBTestCaseWithDB):
	def testAsDictAfterStore(self):
		self.assertIn("_rev", Test().store(self._db).as_dict)

	def testViews(self):
		#two 'tests' in one function so we also test updating the design
		#doc to include the second view.
		doc = DocWithViews()
		with self.assertRaises(pouchdb.PouchDBError):
			doc.syntaxErrorView(self._db)

		self._db.post({})
		self.assertEqual(doc.otherView(self._db)["rows"], [
			{
				"key": None,
				"value": 1
			}
		])
