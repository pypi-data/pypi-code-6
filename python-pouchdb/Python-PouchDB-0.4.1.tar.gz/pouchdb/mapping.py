# -*- coding: utf-8 -*-
#
# Copyright (C) 2007-2009 Christopher Lenz
# Copyright (C) 2014 Marten de Vries
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Mapping from raw JSON data structures to Python objects and vice versa.

While this module is partly based on ``couchdb.mapping``, it doesn't try
to provide the exact same API. The largest differences can be found in
the :class:`DictField` class, the :class:`ListField` class, the
:meth:`Document.query` method and the fact that there's no ``Mapping``
class.

Examples on how to use this module:

>>> env = setup()
>>> db = env.PouchDB('python-tests')

To define a document mapping, you declare a Python class inherited from
`Document`, and add any number of `Field` attributes:

>>> from datetime import datetime
>>> from pouchdb.mapping import Document, TextField, IntegerField, DateTimeField
>>> 
>>> class Person(Document):
... 	name = TextField()
... 	age = IntegerField()
... 	added = DateTimeField(default=datetime.now)
... 
>>> person = Person(name='John Doe', age=42)
>>> person.store(db) #doctest: +ELLIPSIS
Person(added=datetime.datetime(...), age=42, name='John Doe')
>>> person.age
42

You can then load the data from the CouchDB server through your `Document`
subclass, and conveniently access all attributes:

>>> person = Person.load(db, person.id)
>>> old_rev = person.rev
>>> print person.name
John Doe
>>> person.age
42
>>> person.added                #doctest: +ELLIPSIS
datetime.datetime(...)

To update a document, simply set the attributes, and then call the
:meth:`Document.store` method:

>>> person.name = 'John R. Doe'
>>> person.store(db)            #doctest: +ELLIPSIS
Person(added=datetime.datetime(...), age=42, name='John R. Doe')

If you retrieve the document from the server again, you should be getting the
updated data:

>>> person = Person.load(db, person.id)
>>> print person.name
John R. Doe
>>> person.rev != old_rev
True

>>> env.destroy('python-tests')

"""

import uuid
import inspect
import json
try:
	import dateutil.parser
except ImportError: #pragma: no cover
	raise ImportError("pouchdb.objectstorage requires the dateutil module to be installed.")
import time
import numbers
import decimal
import textwrap
import pouchdb
import datetime

class BaseField(object):
	pass

class Field(BaseField):
	"""Basic unit for mapping a piece of data between Python and JSON.

	Instances of this class can be added to subclasses of `Document` to
	describe the mapping of a document. Or rather, subclasses of this
	class.

	"""
	default = lambda self: None
	def __init__(self, name=None, default=None):
		self._jsonName = name
		if default is not None:
			if not callable(default):
				self.default = lambda: default
			else:
				self.default = default

	def jsonSerializable(self, document):
		return self.__get__(document)

	@property
	def jsonName(self):
		return self._jsonName or self.name

	def __get__(self, document, owner=None):
		try:
			return document._json[self.jsonName]
		except AttributeError:
			return self

	def __set__(self, document, value):
		if value is not None:
			value = self.toPy(value)
		document._json[self.jsonName] = value

	def __delete__(self, document):
		raise TypeError("Can't delete a document field.")

class BooleanField(Field):
	"""Mapping field for boolean values."""

	toPy = bool

class DateTimeField(Field):
	"""Mapping field for date/time values."""

	def toPy(self, val):
		if isinstance(val, time.struct_time):
			return datetime.datetime.fromtimestamp(time.mktime(val))
		if isinstance(val, numbers.Integral):
			return datetime.datetime.utcfromtimestamp(val)
		try:
			val = val.isoformat()
		except AttributeError:
			pass
		val = dateutil.parser.parse(val)
		return val

	def jsonSerializable(self, document):
		return document._json[self.jsonName].isoformat()

class DateField(DateTimeField):
	"""Mapping field for date values."""

	def toPy(self, val):
		return super(DateField, self).toPy(val).date()

class TimeField(DateTimeField):
	"""Mapping field for time values."""

	def toPy(self, val):
		return super(TimeField, self).toPy(val).timetz()

class DecimalField(Field):
	"""Mapping field for decimal values."""

	toPy = decimal.Decimal

class StructureField(Field):
	"""The stuff that :class:`ListField` and :class:`DictField` have in
	common.

	"""
	def __init__(self, name=None, default=None, jsonSerializable=None, toPy=None):
		super(StructureField, self).__init__(name, default)

		def passthrough(val):
			return val

		self._jsonSerializable = jsonSerializable or passthrough
		self._toPy = toPy or passthrough

	def jsonSerializable(self, document):
		val = document._json[self.jsonName]
		return self._jsonSerializable(val)

class DictField(StructureField):
	"""Field type for nested dictionaries.

	>>> from pouchdb.mapping import DictField
	>>> db = setup()['python-tests']

	>>> class Post(Document):
	...     title = TextField()
	...     content = TextField()
	...     author = DictField()
	...     extra = DictField()

	>>> post = Post(
	...     title='Foo bar',
	...     author=dict(name='John Doe',
	...                 email='john@doe.com'),
	...     extra=dict(foo='bar'),
	... )
	>>> post.store(db)
	Post(author={'email': 'john@doe.com', 'name': 'John Doe'}, extra={'foo': 'bar'}, title='Foo bar')
	>>> post = Post.load(db, post.id)
	>>> print post.author.name
	John Doe
	>>> print post.author.email
	john@doe.com
	>>> printjson(post.extra)
	{"foo": "bar"}

	>>> printjson(db.destroy())
	{"ok": true}

	"""
	default = lambda self: {}

	def toPy(self, val):
		return pouchdb.utils.AttrAccessDict(self._toPy(val))

class FloatField(Field):
	"""Mapping field for float values."""

	toPy = float

class IntegerField(Field):
	"""Mapping field for integer values."""

	toPy = int

class ListField(StructureField):
	"""Field type for sequences of other fields.

	>>> from pouchdb.mapping import ListField
	>>> import dateutil.parser
	>>> import copy
	>>> db = setup()["python-tests"]
	>>> 
	>>> def load(rows):
	...     for row in rows:
	...         row["time"] = dateutil.parser.parse(row["time"])
	...     return rows
	... 
	>>> def serialize(input):
	...     rows = copy.deepcopy(input)
	...     for row in rows:
	...         row["time"] = row["time"].isoformat()
	...     return rows
	... 
	>>> class Post(Document):
	...     title = TextField()
	...     content = TextField()
	...     pubdate = DateTimeField(default=datetime.now)
	...     comments = ListField(jsonSerializable=serialize, toPy=load)
	... 
	>>> post = Post(title='Foo bar')
	>>> post.comments.append(dict(author='myself', content='Bla bla',
	...                      time=datetime.now()))
	>>> len(post.comments)
	1
	>>> post.store(db) #doctest: +ELLIPSIS
	Post(...)
	>>> post = Post.load(db, post.id)
	>>> comment = post.comments[0]
	>>> print comment['author']
	myself
	>>> print comment['content']
	Bla bla
	>>> comment['time'] #doctest: +ELLIPSIS
	datetime.datetime(...)
	>>> printjson(db.destroy())
	{"ok": true}

	"""
	default = lambda self: []

	def toPy(self, val):
		return list(self._toPy(val))

class LongField(Field):
	"""Mapping field for long values."""

	toPy = long

class TextField(Field):
	"""Mapping field for float values."""

	toPy = unicode

class ViewField(BaseField):
	r"""Descriptor that can be used to bind a view definition to a property of
	a `Document` class.

	>>> from pouchdb.mapping import TextField, IntegerField, ViewField
	>>> class Person(Document):
	...     name = TextField()
	...     age = IntegerField()
	...     by_name = ViewField('people', '''\
	...         function(doc) {
	...             emit(doc.name, doc);
	...         }''')
	>>> Person.by_name
	<ViewField 'people'>

	>>> print Person.by_name.map_fun
	        function(doc) {
	            emit(doc.name, doc);
	        }

	That property can be used as a function, which will execute the view.

	>>> db = setup().PouchDB('python-tests')
	>>> Person(name='test').store(db)
	Person(name='test')
	>>> printjson(Person.by_name(db, limit=3))
	{"offset": 0, "rows": ["Person(name='test')"], "total_rows": 1}

	The results produced by the view are automatically wrapped in the
	`Document` subclass the descriptor is bound to. In this example, it
	returns instances of the `Person` class. This can be done because
	the ViewField automatically includes the ``include_docs`` option
	when making a query. See for more info the :meth:`Document.query`
	method.

	If you use Python view functions, this class can also be used as a
	decorator:

	>>> class Person(Document):
	... 	name = TextField()
	... 	age = IntegerField()
	...
	... 	@ViewField.define('people')
	... 	def by_name(doc):
	... 		yield doc['name'], doc

	>>> Person.by_name
	<ViewField 'people'>

	>>> print Person.by_name.map_fun
	def by_name(doc):
		yield doc['name'], doc

	"""

	def __init__(self, design, map_fun, reduce_fun=None, name=None, language='javascript', **defaults):
		"""Initialize the view descriptor.

		:param design: the name of the design document
		:param map_fun: the map function code
		:param reduce_fun: the reduce function code (optional)
		:param name: the actual name of the view in the design document, if
					 it differs from the name the descriptor is assigned to
		:param language: the name of the language used
		:param defaults: default query string parameters to apply

		"""
		self._design = design
		self._chosenName = name
		self.map_fun = map_fun
		self.reduce_fun = reduce_fun
		self._language = language
		self._defaults = defaults

	@property
	def _viewName(self):
		return self._chosenName or self.name

	def __repr__(self):
		return "<%s %r>" % (type(self).__name__, self._design)

	def __call__(self, db, secondTime=False, **options):
		opts = self._defaults.copy()
		opts.update(options)
		try:
			return self._cls.query(db, self._design + "/" + self._viewName, **opts)
		except pouchdb.PouchDBError, e:
			if not ("name" in e and e["name"] == "not_found"):
				raise
		id = "_design/" + self._design
		try:
			doc = db.get(id)
		except pouchdb.PouchDBError:
			doc = {"_id": id}
		#if still here, probably the view hasn't been found. Try to remedy it.
		doc["language"] = self._language
		doc.setdefault("views", {})[self._viewName] = {
			"map": self.map_fun,
		}
		if self.reduce_fun:
			doc["views"][self._viewName]["reduce"] = self.reduce_fun
		db.put(doc)

		#and retry
		return self.__call__(db, True, **options)

	@classmethod
	def define(cls, design, name=None, language='python', **defaults):
		"""Factory method for use as a decorator (only suitable for Python
		view code).

		"""
		def wrapper(f):
			map_fun = cls._getSource(f)
			return cls(design, map_fun, name=name, language=language, **defaults)
		return wrapper

	@staticmethod
	def _getSource(f):
		lines = inspect.getsourcelines(f)[0]
		#remove decorator
		lines = (l for l in lines if not l.lstrip().startswith("@"))
		#remove trailing whitespace
		source = "".join(lines).rstrip()
		#remove superfluous indentation
		return textwrap.dedent(source)

class MetaDocument(type):
	def __init__(cls, name, bases, attrs):
		super(MetaDocument, cls).__init__(name, bases, attrs)

		#get fields from base classes
		fields = {}
		for base in bases:
			with pouchdb.utils.suppress(AttributeError):
				fields.update(base._fields)
		#add 'own' fields
		for key, value in attrs.iteritems():
			if isinstance(value, BaseField):
				#a new field - set its name so it's aware of that.
				value.name = key
				value._cls = cls
				if isinstance(value, Field):
					fields[key] = value

		#store fields list in the class
		cls._fields = fields

class Document(object):
	"""The document class by default already has two defined fields:
	   ``id`` and ``rev``. They're used to determine the values of
	   CouchDB's and PouchDB's _id and _rev special attributes.

	"""
	__metaclass__ = MetaDocument
	id = TextField(name="_id", default=lambda: str(uuid.uuid4()))
	rev = TextField(name="_rev")

	def __init__(self, _jsonSource=False, **values):
		self._json = {}
		for name, field in self._fields.iteritems():
			key = field.jsonName if _jsonSource else name
			try:
				setattr(self, name, values.pop(key))
			except KeyError:
				setattr(self, name, field.default())

		if values:
			msg = "Got (an) unexpected keyword argument(s): '%s'."
			raise TypeError(msg % ", ".join(values.keys()))

	@property
	def as_dict(self):
		"""Returns the fields with their values in the form of a
		:class:`dict`.

		>>> class Post(Document):
		... 	title = TextField()
		... 	author = TextField()
		>>> post = Post(id='foo-bar', title='Foo bar', author='Joe')
		>>> printjson(post.as_dict)
		{"_id": "foo-bar", "author": "Joe", "title": "Foo bar"}

		"""
		data = self._json.copy()
		if data["_rev"] is None:
			del data["_rev"]
		return data

	def store(self, db):
		"""Store the document in the given database."""

		data = {}
		for field in self._fields.values():
			data[field.jsonName] = field.jsonSerializable(self)

		jsonData = json.dumps(data)

		resp = db.put(jsonData)
		self.id = resp["id"]
		self.rev = resp["rev"]
		return self

	@classmethod
	def load(cls, db, id):
		"""Load a specific document from the given database.

		:param db: the `Database` object to retrieve the document from
		:param id: the document ID
		:return: the `Document` instance
		:raises pouchdb.PouchDBError: when the document with `id` can't
				be found.

		"""
		resp = db.get(id)
		return cls._jsonToInstance(resp)

	@classmethod
	def _jsonToInstance(cls, data):
		return cls(_jsonSource=True, **data)

	@classmethod
	def query(cls, db, info, **options):
		"""Same as :meth:`pouchdb.AbstractPouchDB.query`, but replaces
		each row with an instance of (your subclass of)
		:class:`Document`. Additional attributes set on these objects
		are ``key`` and ``value``. Sets ``options["include_docs"]``
		to True (otherwise the mapping doesn't make any sense). Except
		when there's a reduce function, in that case no mapping takes
		place at all.

		"""
		opts = {"include_docs": True}
		opts.update(options)
		try:
			data = db.query(info, **opts)
		except pouchdb.PouchDBError, e:
			if "name" in e and e["name"] == "query_parse_error":
				return db.query(info, **options)
			raise
		newRows = []
		for row in data["rows"]:
			obj = cls._jsonToInstance(row["doc"])
			obj.key = row["key"]
			obj.value = row["value"]
			newRows.append(obj)
		data["rows"] = newRows
		return data

	def __repr__(self):
		def fieldRepr(name):
			v = self._json[name]
			if isinstance(v, dict):
				return "{%s}" % ", ".join(sorted("'%s': %r" % (k, subv) for k, subv in v.iteritems()))
			if isinstance(v, basestring):
				return "'%s'" % v
			return repr(self._json[name])

		args = [
			name + "=" + fieldRepr(name)
			for name, field in self._fields.iteritems()
			if name not in ["id", "rev"] and field.default() != self._json[name]
		]
		args = sorted(arg for arg in args if arg)
		return "%s(%s)" % (type(self).__name__, ", ".join(args))
