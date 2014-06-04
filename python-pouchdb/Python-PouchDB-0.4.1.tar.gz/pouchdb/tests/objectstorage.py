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

import sys
import StringIO
import pouchdb.objectstorage
from pouchdb.tests.utils import SyncPouchDBTestCaseWithDB
import datetime

class Person(object):
	def __init__(self, name, birth=None):
		self._name = name
		self._birth = birth or datetime.date.today()
		self.data = [{"a": [1, 2, 3]}]

	def __str__(self):
		return "Hi, I'm %s, nice to meet you! I was born at %s." % (self._name, self._birth)

	def sayHello(self, f=sys.stdout):
		f.write(str(self) + "\n")

class ObjectStorageTests(SyncPouchDBTestCaseWithDB):
	def testWithoutId(self):
		person = Person("Joe")

		storeResult = pouchdb.objectstorage.store(person, self._db)
		self.assertEqual(storeResult, person)

		person2 = pouchdb.objectstorage.load(self._db, person.id)
		f = StringIO.StringIO()
		person2.sayHello(f)
		self.assertTrue(f.getvalue().endswith("\n"))
		#will fail in the year 2100 :(
		self.assertTrue(f.getvalue().startswith("Hi, I'm Joe, nice to meet you! I was born at 20"))

		person3 = pouchdb.objectstorage.load(self._db, person2.id, person2.rev)
		self.assertEqual(person2.data, [{"a": [1, 2, 3]}])

	def testPrefix(self):
		prefix = "myprefix_"
		person = Person("Joe 2.0")
		pouchdb.objectstorage.store(person, self._db, id="joe", prefix=prefix)

		#one extra 'cause only for private fields the prefix should be
		#used in the first place.
		self.assertIn("myprefix__", str(self._db.get("joe")))

		loaded = pouchdb.objectstorage.load(self._db, "joe", prefix=prefix)
		self.assertIn("a", loaded.data[0])

	def testStoreAgainAfterUpdate(self):
		person = Person("Joe 3.0")
		person.id = "joe"
		pouchdb.objectstorage.store(person, self._db)
		old_rev = person.rev
		person.data = {"some": 1}
		pouchdb.objectstorage.store(person, self._db)

		old = pouchdb.objectstorage.load(self._db, "joe", rev=old_rev)
		new = pouchdb.objectstorage.load(self._db, "joe", rev=person.rev)

		self.assertIn("a", old.data[0])
		self.assertEqual(new.data, {"some": 1})
