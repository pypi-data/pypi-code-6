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

"""The :mod:`pouchdb` package mostly mirrors the `PouchDB JavaScript
API`_.

.. _PouchDB JavaScript API: http://pouchdb.com/api.html

There are two API versions: one asynchronous one, which almost directly
maps functions to their JavaScript equivalents and supports both
promises and callbacks in most cases, and a synchronous one, which
doesn't have a JavaScript equivalent, but is often easier to use.

API examples
============

**Synchronous:**

>>> environment = setup()
>>> db = environment.PouchDB('example')
>>> printjson(db.put({"_id": 'my_example_doc'})) #doctest: +ELLIPSIS
{"id": "my_example_doc", "ok": true, "rev": "1-..."}
>>> printjson(db.get('my_example_doc')) #doctest: +ELLIPSIS
{"_id": "my_example_doc", "_rev": "1-..."}

and (using :class:`dict`-like syntax):

>>> db["my_example_doc"] = {}
>>> printjson(db["my_example_doc"]) #doctest: +ELLIPSIS
{"_id": "my_example_doc", "_rev": "2-..."}

**Asynchronous:**

>>> def callback(err, resp):
...     printjson(["inside callback:", resp])
... 
>>> env = setup(async=True)
>>> db = env.PouchDB('example')
>>> promise = db.post({}, callback)

or ``db.post({}).then(callback)``, with the ``err`` argument removed
from the callback function.
Time to run the event loop. Normally, that's done using e.g.
``QtGui.QApplication().exec_()``, but for testing purposes like this
the following can be used:

>>> env.context.waitUntilCalled(callback) #doctest: +ELLIPSIS
["inside callback:", {"id": "...", "ok": true, "rev": "1-..."}]
>>> promise2 = env.destroy('example')

For more examples, see the :doc:`tests` documentation page.

API conventions
===============

Since the asynchronous and synchronous api have the same methods, those
methods are documented in abstract base classes:
:class:`AbstractEnvironment` and :class:`AbstractPouchDB`. Their
subclasses (:class:`AsyncEnvironment`, :class:`SyncEnvironment`,
:class:`AsyncPouchDB` and :class:`SyncPouchDB`) are the ones
actually exposed to you in the API.

The names in the JavaScript API of PouchDB are in camelCase_.
Python-PouchDB provides snake_case_ aliases where necessary, since
that's the preffered form according to the `PEP 8 style guide`_.

.. _camelCase: https://en.wikipedia.org/wiki/CamelCase
.. _snake_case: https://en.wikipedia.org/wiki/Snake_case
.. _PEP 8 style guide: http://legacy.python.org/dev/peps/pep-0008/#function-names

As shown in the example, you can pass in dictionaries as documents.
Additionally, Python-PouchDB allows passing in JSON strings. So, no need
to convert if you already have a JSON string.

"""

from pouchdb import context
from pouchdb import utils
from pouchdb.info import __author__, __version__, __copyright__

import itertools
import functools
import collections
import os
import abc
import contextlib
import tempfile
import shutil
import atexit

with utils.suppress(ImportError):
	import faulthandler
	faulthandler.enable()

_IGNORED_ERRORS = [
	"ArrayBuffer values are deprecated in Blob Constructor.",
	"ArrayBuffer is deprecated in XMLHttpRequest.send(). Use ArrayBufferView instead.",
	"EVALUATED FUNCTION LOGS:",
]

def _getPromiseResponse(ctx, promise):
	returned = {}
	def success(resp):
		returned["resp"] = resp
	def fail(err):
		returned["err"] = err

	promise.then(success, fail)
	ctx.waitUntilCalled([success, fail])

	if returned.get("err"):
		raise PouchDBError(returned["err"])
	return returned["resp"]

@contextlib.contextmanager
def _getting_callback_result(ctx):
	returning = {}
	def callback(err=None, resp=None):
		returning["err"] = err
		returning["resp"] = resp
	info = {"callback": callback}
	yield info
	ctx.waitUntilCalled(callback)
	if returning.get("err"):
		raise PouchDBError(returning["err"])
	info["resp"] = returning["resp"]

def _filterNone(args):
	return [a for a in args if a is not None]

def _jsonAllowed(value):
	if isinstance(value, basestring):
		return context.JSON(value)
	return value

def _aliasFor(methodName):
	def alias(self, *args, **kwargs):
		return getattr(self, methodName)(*args, **kwargs)
	alias.__doc__ = "Alias for :meth:`%s`." % methodName
	return alias

class AbstractPouchDB(object):
	"""**Never** instantiate this class or one of its subclasses
	yourself. Create an environment using the :func:`setup` function
	instead, and then use its :attr:`AbstractEnvironment.PouchDB`
	attribute, with the arguments specified at :meth:`__init__`.

	Extra (optional) options for all ``AbstractPouchDB.validating*``
	methods compared to their normal ``AbstractPouchDB.*`` counterparts
	are:

	- ``secObj``: e.g.::

		{
			"admins": {
				"names": [],
				"roles": []
			},
			"members": {
				"names": [],
				"roles": []
			}
		}

	- ``userCtx``: e.g.::

		{
			"db": "test_db",
			"name": "username",
			"roles": [
				"_admin"
			]
		}

	- ``checkHttp``: Set this to ``True`` if you want to validate HTTP
	  database documents offline too. Unnecessary for CouchDB, but handy
	  for e.g. PouchDB-Server, which doesn't validate itself.

	"""
	__metaclass__ = abc.ABCMeta

	_idCounter = itertools.count()

	def __init__(self, _ctx, name=None, **options):
		"""This method creates a database or opens an existing one. If
		you use a URL like http://domain.com/dbname then Python-PouchDB
		will work as a client to an online CouchDB instance. Otherwise
		it will create a local database using the WebSQL backend.

		"""
		self._ctx = _ctx
		self._id = next(self._idCounter)

		try:
			self._ctx.newObject(self._id, name, options)
		except context.JSError, e:
			raise PouchDBError(e)

	def _asyncCall(self, methodName, *args):
		return self._ctx.call(self._id, methodName, *_filterNone(args))

	@abc.abstractmethod
	def destroy(self):
		"""Delete database."""

	@abc.abstractmethod
	def put(self, doc, id=None, rev=None, **options):
		"""Create a new document or update an existing document. If the
		document already exists, you must specify its revision ``_rev``,
		otherwise a conflict will occur.

		"""

	@abc.abstractmethod
	def post(self, doc, **options):
		"""Create a new document and let PouchDB generate an ``_id`` for
		it.

		"""

	@abc.abstractmethod
	def get(self, docid, **options):
		"""Retrieves a document, specified by ``docid``."""

	@abc.abstractmethod
	def remove(self, doc, **options):
		"""Deletes the document. doc is required to be a document with
		at least an ``_id`` and a ``_rev`` property. Sending the full
		document will work as well.

		"""

	@abc.abstractmethod
	def bulkDocs(self, docs, **options):
		"""Modify, create or delete multiple documents. The docs
		argument is an object with property docs which is an array of
		documents. You can also specify a new_edits property on the
		docs object that when set to false allows you to post existing
		documents.

		If you omit an ``_id`` parameter on a given document, the
		database will create a new document and assign the ID for you.
		To update a document, you must include both an ``_id`` parameter
		and a ``_rev`` parameter, which should match the ID and revision
		of the document on which to base your updates. Finally, to
		delete a document, include a ``_deleted`` parameter with the
		value ``True``.

		"""

	bulk_docs = _aliasFor("bulkDocs")

	@abc.abstractmethod
	def allDocs(self, **options):
		"""Fetch multiple documents. Deleted documents are only included
		if ``keys`` is specified.

		"""

	all_docs = _aliasFor("allDocs")

	@abc.abstractmethod
	def changes(self, **options):
		"""A list of changes made to documents in the database, in the
		order they were made. It returns an object with one method
		cancel, which you call if you don't want to listen to new
		changes anymore. ``onChange`` will be be called for each change
		that is encountered.

		"""

	@abc.abstractmethod
	def replicateTo(self, remoteDB, **options):
		"""A shorthand for :meth:`AbstractEnvironment.replicate`"""

	replicate_to = _aliasFor("replicateTo")

	@abc.abstractmethod
	def replicateFrom(self, remoteDB, **options):
		"""A shorthand for :meth:`AbstractEnvironment.replicate`"""

	replicate_from = _aliasFor("replicateFrom")

	@abc.abstractmethod
	def sync(self, remoteDB, **options):
		"""A shorthand for :meth:`AbstractEnvironment.sync`"""

	@abc.abstractmethod
	def putAttachment(self, docId, attachmentId, doc, type, rev=None):
		"""Attaches a binary object to a document. Most of
		Python-PouchDB's API deals with JSON, but if you're dealing
		with large binary data (such as PNGs), you may incur a
		performance or storage penalty if you simply include them as
		base64- or hex-encoded strings. In these cases, you can store
		the binary data as an attachment.

		Be aware that the argument order is different than in PouchDB
		due to the ``rev`` argument being optional. Byte strings replace
		blobs in Python-PouchDB. (e.g. ``b"Hello World!"``)

		"""

	put_attachment = _aliasFor("putAttachment")

	@abc.abstractmethod
	def getAttachment(self, docId, attachmentId, **options):
		"""Get attachment data. Returns a dictionary with the following
		format::

			{
				"data": b"Bytes as byte string",
				"type": "text/plain"
			}

		"""

	get_attachment = _aliasFor("get_attachment")

	@abc.abstractmethod
	def removeAttachment(self, docId, attachmentId, rev):
		"""Delete an attachment from a doc."""

	remove_attachment = _aliasFor("remove_attachment")

	@abc.abstractmethod
	def query(self, fun, **options):
		"""Retrieves a view, which allows you to perform more complex
		queries on Python-PouchDB. The CouchDB documentation for map/
		reduce applies to Python-PouchDB.

		Since views perform a full scan of all documents, this method
		may be slow, unless you first save your view in a design
		document.

		"""

	@abc.abstractmethod
	def viewCleanup(self, **options):
		"""Cleans up any stale map/reduce indexes.

		As design docs are deleted or modified, their associated index
		files (in CouchDB) or companion databases (in local PouchDBs)
		continue to take up space on disk. :meth:`viewCleanup` removes
		these unnecessary index files.

	"""

	view_cleanup = _aliasFor("viewCleanup")

	@abc.abstractmethod
	def info(self):
		"""Get information about a database."""

	@abc.abstractmethod
	def compact(self):
		"""Runs compaction of the database. Fires callback when
		compaction is done. If you use the http adapter and have
		specified a callback, Pouch will ping the remote database in
		regular intervals unless the compaction is finished.

		"""

	@abc.abstractmethod
	def revsDiff(self, diff):
		"""Given a set of document/revision IDs, returns the subset of
		those that do not correspond to revisions stored in the
		database. Primarily used in replication.

		"""

	revs_diff = _aliasFor("revsDiff")

	#gql plug-in
	@abc.abstractmethod
	def gql(self, query, **options):
		"""	Uses the GQL PouchDB plug-in. Check out `its documentation
		<http://pouchdb.com/gql.html>`_.

		The Google Query Language (GQL) interface provides an
		alternative method for accessing data. The version of GQL
		implemented here is based on the `Google Visualization API Query
		Language
		<https://developers.google.com/chart/interactive/docs/querylanguage>`_.

		The syntax of GQL queries should be familiar to those who have
		used SQL, but the capabilities of GQL are much more limited.

		"""

	#geopouch plug-in
	@abc.abstractmethod
	def spatial(self, fun, **options):
		"""Same as requesting ``_spatial`` in CouchDB when GeoCouch is
		installed. Wraps the geopouch plug-in.

		"""

	#search plug-in
	@abc.abstractmethod
	def search(self, func, **options):
		"""Wraps the pouchdb-search plug-in."""

	#authentication plug-in
	@abc.abstractmethod
	def signup(self, username, password, **options):
		"""Sign up a new user who doesn't exist yet. Throws an error if
		the user already exists or if the username is invalid, or if
		some network error occurred. CouchDB has some limitations on
		user names (e.g. they cannot contain the character ':').

		Note: Signing up does not automatically log in a user; you will
		need to call :meth:`login` afterwards.
		
		Options:

		- `metadata` : Object of metadata you want to store with the
		  username, e.g. an email address or any other info. Can be as
		  deeply structured as you want.

		"""

	signUp = _aliasFor("signup")
	sign_up = _aliasFor("signup")

	@abc.abstractmethod
	def login(self, username, password, **options):
		"""Log in an existing user. Throws an error if the user doesn't
		exist yet, the password is wrong, the HTTP server is
		unreachable, or a meteor struck your computer.

		"""

	logIn = _aliasFor("login")
	log_in = _aliasFor("login")

	@abc.abstractmethod
	def logout(self, **options):
		"""Logs out whichever user is currently logged in. If nobody's
		logged in, it does nothing and just returns ``{"ok": True}``.

		"""

	logOut = _aliasFor("logout")
	log_out = _aliasFor("log_out")

	@abc.abstractmethod
	def getSession(self, **options):
		"""Returns information about the current session. In other
		words, this tells you which user is currently logged in.

		"""

	get_session = _aliasFor("getSession")

	@abc.abstractmethod
	def getUser(self, username, **options):
		"""Returns the user document associated with a username.
		(CouchDB, in a pleasing show of consistency, stores users as
		JSON documents in the special _users database.) This is the
		primary way to get metadata about a user.

		"""

	get_user = _aliasFor("getUser")

	#validation plug-in
	@abc.abstractmethod
	def validatingPut(self, doc, id=None, rev=None, **options):
		"""Same as :meth:`put`, but validates like in CouchDB. Wraps
		the validation PouchDB plug-in.
		"""

	validating_put = _aliasFor("validatingPut")

	@abc.abstractmethod
	def validatingPost(self, doc, **options):
		"""Same as :meth:`post`, but validates like in CouchDB. Wraps
		the validation PouchDB plug-in.

		"""

	validating_post = _aliasFor("validatingPost")

	@abc.abstractmethod
	def validatingRemove(self, doc, **options):
		"""Same as :meth:`remove`, but validates like in CouchDB.
		Wraps the validation PouchDB plug-in.

		"""

	validating_remove = _aliasFor("validatingRemove")

	@abc.abstractmethod
	def validatingBulkDocs(self, docs, **options):
		"""Same as :meth:`bulkDocs`, but validates like in CouchDB.
		Wraps the validation PouchDB plug-in.

		"""

	validating_bulk_docs = _aliasFor("validatingBulkDocs")

	@abc.abstractmethod
	def validatingPutAttachment(self, docId, attachmentId, doc, type, rev=None, **options):
		"""Same as :meth:`putAttachment`, but validates like in
		CouchDB. Wraps the validation PouchDB plug-in.

		"""

	validating_put_attachment = _aliasFor("validatingPutAttachment")

	@abc.abstractmethod
	def validatingRemoveAttachment(self, docId, attachmentId, rev, **options):
		"""Same as :meth:`removeAttachment`, but validates like in
		CouchDB. Wraps the validation PouchDB plug-in.

		"""

	validating_remove_attachment = _aliasFor("validatingRemoveAttachment")

	#show plug-in
	@abc.abstractmethod
	def show(self, showPath, **options):
		"""Same as requesting ``_show`` in CouchDB. Wraps the show
		PouchDB plug-in.

		"""

	#list plug-in
	@abc.abstractmethod
	def list(self, listPath, **options):
		"""Same as requesting ``_list`` in CouchDB. Wraps the list
		PouchDB plug-in.

		"""

	#update plug-in
	@abc.abstractmethod
	def update(self, url, **options):
		"""Same as sending a request to ``_update`` in CouchDB. Wraps
		the update PouchDB plug-in.

		``options``:

		- ``withValidation``: If ``True``, the update function uses
		  :meth:`validatingPut` instead of (the default) :meth:`put`.

		"""

	#rewrite plug-in
	@abc.abstractmethod
	def rewrite(self, url, **options):
		"""Same as sending a request to ``_rewrite`` in CouchDB. Wraps
		the rewrite PouchDB plug-in. The ``url`` has the form
		`designDocName/rewritePath`. Keep in mind that you need to use
		``options.query`` instead of appending a ?key=value string to
		the ``url``.

		``options``:

		- ``withValidation``: If ``True``, the ``db.validating*``
		  functions are used instead of their ``db.*`` counterparts if
		  the rewrite routes to such a resource where that is relevant.

		"""

	@abc.abstractmethod
	def rewriteResultRequestObject(self, url, **options):
		"""See :meth:`rewrite`. Instead of returning the result of the
		function that the rewrite routes to, this returns a CouchDB
		request object that points to the resource the rewrite resolves
		to. See also the CouchDB documentation `on the request object`_.

		.. _on the request object: http://docs.couchdb.org/en/latest/json-structure.html#request-object

		"""

@contextlib.contextmanager
def _convert404ToKeyError():
	try:
		yield
	except PouchDBError, e:
		if e["status"] == 404:
			raise KeyError(str(e))
		#probably an authorization problem
		raise

class SyncPouchDB(AbstractPouchDB, collections.MutableMapping):
	"""This class is a MutableMapping, which means it can be used like a
	:class:`dict`. For details on how that works with revisions, see
	the documentations on the following methods: :meth:`__getitem__`,
	:meth:`__setitem__` and :meth:`__delitem__`.

	See for all the methods that being a MutableMapping offers, `the
	docs about it`_.

	.. _the docs about it: https://docs.python.org/2/library/collections.html#collections-abstract-base-classes

	>>> db = setup()["my-example"]
	>>> db["mytest"] = {"test": "ok"}
	>>> printjson(list(db))
	["mytest"]
	>>> len(db)
	1
	>>> "mytest" in db
	True
	>>> "abc" in db
	False

	"""
	def __getitem__(self, docId):
		"""A shortcut for the :meth:`AbstractPouchDB.get` method.
		
		Raises a :exc:`KeyError` in place of a :exc:`PouchDBError` if
		that error's status is 404 Not Found.

		>>> db = setup().PouchDB("example")
		>>> db["abc"]
		Traceback (most recent call last):
		  ...
		KeyError: '{"status":404,"name":"not_found","message":"missing"}'

		"""
		with _convert404ToKeyError() as e:
			return self.get(docId)

	def __delitem__(self, docId):
		"""A shortcut for the :meth:`AbstractPouchDB.remove` method.

		Raises a :exc:`KeyError` in place of a :exc:`PouchDBError` if
		that error's status is 404 Not Found. Removes the current
		document from the database (in other words, the **latest
		revision** is taken from the database).

		>>> db = setup()["example"]
		>>> del db["abc"]
		Traceback (most recent call last):
		  ...
		KeyError: '{"status":404,"name":"not_found","message":"missing"}'

		"""
		with _convert404ToKeyError() as e:
			self.remove(self[docId])

	def __setitem__(self, docId, doc):
		"""Sets ``doc``'s _id to ``docId`` and saves the result. When
		no ``doc["_rev"]`` is defined, the one from the current document
		saved under that id is reused. That is a **difference** from the
		normal :meth:`AbstractPouchDB.put` method. When succesful,
		``doc["_rev"]`` will have been set to its new value.

		"""
		doc["_id"] = docId
		if not "_rev" in doc:
			#get the rev of the current document - if one exists.
			with utils.suppress(PouchDBError):
				doc["_rev"] = self.get(docId)._rev
		resp = self.put(doc)
		doc["_rev"] = resp.rev

	def __eq__(self, other):
		"""Only equal when ``other`` is just another reference to
		``self``

		"""
		return self is other

	def __iter__(self):
		return (row["id"] for row in self.allDocs()["rows"])

	def __len__(self):
		return self.allDocs()["total_rows"]

	def get_(self, *args, **kwargs):
		"""Because ``MutableMapping.get`` is overwritten by the
		:meth:`get` method, it's aliased under this name.

		>>> printjson(db.get_("abc", {"hello": "world"}))
		{"hello": "world"}

		"""
		#can't use super() - using MRO doesn't work when two equally
		#named methods have different signatures.
		return collections.MutableMapping.get(self, *args, **kwargs)

	def _syncCall(self, methodName, *args):
		promise = self._ctx.call(self._id, methodName, *_filterNone(args))
		return _getPromiseResponse(self._ctx, promise)

	def destroy(self):
		return self._syncCall("destroy")

	def put(self, doc, id=None, rev=None, **options):
		return self._syncCall("put", _jsonAllowed(doc), id, rev, options)

	def post(self, doc, **options):
		return self._syncCall("post", _jsonAllowed(doc), options)

	def get(self, docid, **options):
		return self._syncCall("get", docid, options)

	def remove(self, doc, **options):
		return self._syncCall("remove", _jsonAllowed(doc), options)

	def bulkDocs(self, docs, **options):
		return self._syncCall("bulkDocs", _jsonAllowed(docs), options)

	def allDocs(self, **options):
		return self._syncCall("allDocs", options)

	def changes(self, **options):
		"""When the ``live`` or ``continuous`` option is active, this
		method acts like its asynchronous equivalent.

		"""
		return self._callFunc(options)("changes", options)

	def _callFunc(self, options):
		if options.get("live", False) or options.get("continuous", False):
			return self._asyncCall
		return self._syncCall

	def replicateTo(self, remoteDB, **options):
		"""When the ``live`` or ``continuous`` option is active, this
		method acts like its asynchronous equivalent.

		"""
		return self._callFunc(options)("replicate.to", remoteDB, options)

	def replicateFrom(self, remoteDB, **options):
		"""When the ``live`` or ``continuous`` option is active, this
		method acts like its asynchronous equivalent.

		"""
		return self._callFunc(options)("replicate.from", remoteDB, options)

	def sync(self, remoteDB, **options):
		"""When the ``live`` or ``continuous`` option is active, this
		method acts like its asynchronous equivalent.

		"""
		return self._callFunc(options)("replicate.sync", remoteDB, options)

	def putAttachment(self, docId, attachmentId, doc, type, rev=None):
		return self._syncCall("putAttachment", docId, attachmentId, rev, context.Blob(doc), type)

	def getAttachment(self, docId, attachmentId, **options):
		return self._syncCall("getAttachment", docId, attachmentId, options)

	def removeAttachment(self, docId, attachmentId, rev):
		return self._syncCall("removeAttachment", docId, attachmentId, rev)

	def query(self, fun, **options):
		return self._syncCall("query", fun, options)

	def viewCleanup(self, **options):
		return self._syncCall("viewCleanup", options)

	def info(self):
		return self._syncCall("info")

	def compact(self, **options):
		return self._syncCall("compact", options)

	def revsDiff(self, diff):
		return self._syncCall("revsDiff", _jsonAllowed(diff))

	#gql plug-in
	def gql(self, query, **options):
		with _getting_callback_result(self._ctx) as info:
			self._ctx.call(self._id, "gql", query, options, info["callback"])
		return info["resp"]

	#spatial plug-in
	def spatial(self, fun, **options):
		return self._syncCall("spatial", fun, options)

	#search plug-in
	def search(self, func, **options):
		return self._syncCall("search", func, options)

	#authentication plug-in
	def signup(self, username, password, **options):
		return self._syncCall("signup", username, password, options)

	def login(self, username, password, **options):
		return self._syncCall("login", username, password, options)

	def logout(self, **options):
		return self._syncCall("logout", options)

	def getSession(self, **options):
		return self._syncCall("getSession", options)

	def getUser(self, username, **options):
		return self._syncCall("getUser", username, options)

	#validation plug-in
	def validatingPut(self, doc, id=None, rev=None, **options):
		return self._syncCall("validatingPut", _jsonAllowed(doc), id, rev, options)

	def validatingPost(self, doc, **options):
		return self._syncCall("validatingPost", _jsonAllowed(doc), options)

	def validatingRemove(self, doc, **options):
		return self._syncCall("validatingRemove", _jsonAllowed(doc), options)

	def validatingBulkDocs(self, docs, **options):
		return self._syncCall("validatingBulkDocs", _jsonAllowed(docs), options)

	def validatingPutAttachment(self, docId, attachmentId, doc, type, rev=None, **options):
		return self._syncCall("validatingPutAttachment", docId, attachmentId, rev, context.Blob(doc), type, options)

	def validatingRemoveAttachment(self, docId, attachmentId, rev, **options):
		return self._syncCall("validatingRemoveAttachment", docId, attachmentId, rev, options)

	#show plug-in
	def show(self, showPath, **options):
		return self._syncCall("show", showPath, options)

	#list plug-in
	def list(self, listPath, **options):
		return self._syncCall("list", listPath, options)

	#update plug-in
	def update(self, url, **options):
		return self._syncCall("update", url, options)

	#rewrite plug-in
	def rewrite(self, url, **options):
		return self._syncCall("rewrite", url, options)

	def rewriteResultRequestObject(self, url, **options):
		return self._syncCall("rewriteResultRequestObject", url, options)

class BaseError(Exception):
	"""The base class for all errors this module should raise.

	"""

class EnvironmentError(BaseError):
	"""Raised when something is wrong relating to the environment in
	which Python-PouchDB runs.

	"""

class PouchDBError(BaseError):
	"""All error responses PouchDB would normally give you get raised
	in the form of this error class in Python-PouchDB. You can use get
	item syntax to access properties set on the error object. E.g.:

		>>> try:
		...     setup().PouchDB('new-db').get('unexisting-doc')
		... except pouchdb.PouchDBError as e:
		...    if e["status"] == 404:
		...        print("Not found")
		...    else:
		...        print("Unknown error")
		...
		Not found

	"""
	def __init__(self, message, *args, **kwargs):
		super(PouchDBError, self).__init__(message, *args, **kwargs)

		self.message = message

	def __getitem__(self, key):
		return self.message[key]

	def __contains__(self, key):
		return key in self.message

	def __str__(self):
		with utils.suppress(KeyError, TypeError):
			return self.message["toString"]()
		return str(self.message)

class AsyncPouchDB(AbstractPouchDB):
	"""The GQL plug-in only supports the callback interface, it doesn't
	provide a promise.

	"""
	def destroy(self, callback=None):
		return self._asyncCall("destroy", callback)

	def _handlePutArgs(self, doc, id, rev, callback, options):
		if callable(id):
			callback = id
			id = None
		if callable(rev):
			callback = rev
			rev = None
		return _jsonAllowed(doc), id, rev, options, callback

	def put(self, doc, id=None, rev=None, callback=None, **options):
		return self._asyncCall("put", *self._handlePutArgs(doc, id, rev, callback, options))

	def post(self, doc, callback=None, **options):
		return self._asyncCall("post", _jsonAllowed(doc), options, callback)

	def get(self, docid, callback=None, **options):
		return self._asyncCall("get", docid, options, callback)

	def remove(self, doc, callback=None, **options):
		return self._asyncCall("remove", _jsonAllowed(doc), options, callback)

	def bulkDocs(self, docs, callback=None, **options):
		return self._asyncCall("bulkDocs", _jsonAllowed(docs), options, callback)

	def allDocs(self, callback=None, **options):
		return self._asyncCall("allDocs", options, callback)

	def changes(self, **options):
		return self._asyncCall("changes", options)

	def replicateTo(self, remoteDB, callback=None, **options):
		return self._asyncCall("replicate.to", remoteDB, options, callback)

	def replicateFrom(self, remoteDB, callback=None, **options):
		return self._asyncCall("replicate.from", remoteDB, options, callback)

	def sync(self, remoteDB, callback=None, **options):
		return self._asyncCall("replicate.sync", remoteDB, options, callback)

	def putAttachment(self, docId, attachmentId, doc, type, rev=None, callback=None):
		return self._asyncCall("putAttachment", docId, attachmentId, rev, context.Blob(doc), type, callback)

	def getAttachment(self, docId, attachmentId, callback=None, **options):
		return self._asyncCall("getAttachment", docId, attachmentId, options, callback)

	def removeAttachment(self, docId, attachmentId, rev, callback=None):
		return self._asyncCall("removeAttachment", docId, attachmentId, rev, callback)

	def query(self, fun, callback=None, **options):
		return self._asyncCall("query", fun, options, callback)

	def viewCleanup(self, callback=None, **options):
		return self._asyncCall("viewCleanup", options, callback)

	def info(self, callback=None):
		return self._asyncCall("info", callback)

	def compact(self, callback=None, **options):
		return self._asyncCall("compact", options, callback)

	def revsDiff(self, diff, callback=None):
		return self._asyncCall("revsDiff", _jsonAllowed(diff), callback)

	#gql plug-in
	def gql(self, query, callback=None, **options):
		return self._asyncCall("gql", query, options, callback)

	#spatial plug-in
	def spatial(self, fun, callback=None, **options):
		return self._asyncCall("spatial", fun, options, callback)

	#search plug-in
	def search(self, func, callback=None, **options):
		return self._asyncCall("search", func, options, callback)

	#authentication plug-in
	def signup(self, username, password, callback=None, **options):
		return self._asyncCall("signup", username, password, options, callback)

	def login(self, username, password, callback=None, **options):
		return self._asyncCall("login", username, password, options, callback)

	def logout(self, callback=None, **options):
		return self._asyncCall("logout", options, callback)

	def getSession(self, callback=None, **options):
		return self._asyncCall("getSession", options, callback)

	def getUser(self, username, callback=None, **options):
		return self._asyncCall("getUser", username, options, callback)

	#validation functions
	def validatingPut(self, doc, id=None, rev=None, callback=None, **options):
		return self._asyncCall("validatingPut", *self._handlePutArgs(doc, id, rev, callback, options))

	def validatingPost(self, doc, callback=None, **options):
		return self._asyncCall("validatingPost", _jsonAllowed(doc), options, callback)

	def validatingRemove(self, doc, callback=None, **options):
		return self._asyncCall("validatingRemove", _jsonAllowed(doc), options, callback)

	def validatingBulkDocs(self, docs, callback=None, **options):
		return self._asyncCall("validatingBulkDocs", _jsonAllowed(docs), options, callback)

	def validatingPutAttachment(self, docId, attachmentId, doc, type, rev=None, callback=None, **options):
		return self._asyncCall("validatingPutAttachment", docId, attachmentId, context.Blob(doc), type, rev, options, callback)

	def validatingRemoveAttachment(self, docId, attachmentId, rev, callback=None, **options):
		return self._asyncCall("validatingRemoveAttachment", docId, attachmentId, rev, options, callback)

	#show plug-in
	def show(self, showPath, callback=None, **options):
		return self._asyncCall("show", showPath, options, callback)

	#list plug-in
	def list(self, listPath, callback=None, **options):
		return self._asyncCall("list", listPath, options, callback)

	#update plug-in
	def update(self, url, callback=None, **options):
		return self._asyncCall("update", url, options, callback)

	#rewrite plug-in
	def rewrite(self, url, callback=None, **options):
		return self._asyncCall("rewrite", url, options, callback)

	def rewriteResultRequestObject(self, url, callback=None, **options):
		return self._asyncCall("rewriteResultRequestObject", url, options, callback)

class AbstractEnvironment(object):
	"""The environment is `an event emitter
	<http://nodejs.org/api/events.html#events_class_events_eventemitter>`_
	and will emit a 'created' event when a database is created. A
	'destroy' event is emited when a database is destroyed.

	**Don't** instantiate this class or one of its subclasses
	yourself, use the :func:`setup` function instead.
	"""
	__metaclass__ = abc.ABCMeta

	#A placeholder value when uninstantiated for sphinxdoc.
	PouchDB = "<subclass of AbstractPouchDB (approximately)>"

	@abc.abstractmethod
	def __init__(self, PouchDB, ctx, *args, **kwargs):
		super(AbstractEnvironment, self).__init__(*args, **kwargs)

		self._ctx = ctx

		#:The PouchDB class that you can use to make a new database
		#:instance. You should always use this: **never** instantiate
		#::class:`SyncPouchDB` or :class:`AsyncPouchDB` manually.
		self.PouchDB = functools.partial(PouchDB, self._ctx)

	def __getitem__(self, dbName):
		"""A shortcut for the :attr:`PouchDB` attribute. The following
		two lines of code are, as you can see, equivalent:

		>>> setup()["test"] #doctest: +ELLIPSIS
		<pouchdb.SyncPouchDB object at 0x...>
		>>> setup().PouchDB('test') #doctest: +ELLIPSIS
		<pouchdb.SyncPouchDB object at 0x...>

		"""
		return self.PouchDB(dbName)

	def _asyncCall(self, methodName, *args):
		return self._ctx.callStatic(methodName, *_filterNone(args))

	@property
	def POUCHDB_VERSION(self):
		"""The value of what is ``PouchDB.version`` in JavaScript, in
		other words, the version of PouchDB that Python-PouchDB wraps.

		"""
		return self._ctx.staticProperty("version")

	@abc.abstractmethod
	def destroy(self, name_=None, **options):
		"""Allows you to destroy a database without creating a new 
		PouchDB instance first.

		The ``name`` argument in PouchDB is called `name_` in
		Python-PouchDB, to prevent a clash with the ``options["name"]``
		argument. In JavaScript where there are no keyword arguments the
		problem doesn't exist, in Python it does, hence the change.

		"""

	@abc.abstractmethod
	def replicate(self, source, target, **options):
		"""Replicate data from source to target. Both the source and
		target can be a string representing a CouchDB database url or
		the name a local PouchDB database. If ``live`` is true, then
		this will track future changes and also replicate them
		automatically.

		"""

	@abc.abstractmethod
	def sync(self, source, target, **options):
		"""Sync data from ``source`` to ``target`` and ``target`` to
		``source``. This is a convience method for bidirectional data
		replication.

		"""

	@property
	def context(self):
		"""Allows access to the internals of Python-Pouch; only useful
		for debugging purposes. E.g. :attr:`context`.inspect() and
		:attr:`context`.waitUntilCalled(). The last is used by the
		test suite.

		"""
		return self._ctx

	#event emitter methods
	def addListener(self, event, listener):
		"""Adds a listener to the end of the listeners array for the
		specified event.

		"""
		return self._ctx.callStatic("addListener", event, listener)

	add_listener = _aliasFor("addListener")
	on = _aliasFor("addListener")

	def emit(self, event, *args):
		"""Execute each of the listeners in order with the supplied
		``args``. Returns ``True`` if event had listeners, ``False``
		otherwise.

		"""
		return self._asyncCall("emit", event, *args)

	def listeners(self, event):
		"""Returns an array of listeners for the specified event."""

		return self._asyncCall("listeners", event)

	def once(self, event, listener):
		"""Adds a one time listener for the event. This listener is
		invoked only the next time the event is fired, after which it
		is removed.

		"""
		return self._asyncCall("once", event, listener)

	def removeListener(self, event, listener):
		"""Remove a listener from the listener array for the specified
		event. Caution: changes array indices in the listener array
		behind the listener.

		"""
		return self._asyncCall("removeListener", event, listener)

	remove_listener = _aliasFor("removeListener")

	def removeAllListeners(self, event=None):
		"""Removes all listeners, or those of the specified event."""

		return self._asyncCall("removeAllListeners", event)

	remove_all_listeners = _aliasFor("removeAllListeners")

	def setMaxListeners(self, n):
		"""By default EventEmitters will print a warning if more than 10
		listeners are added for a particular event. This is a useful
		default which helps finding memory leaks. Obviously not all
		Emitters should be limited to 10. This function allows that
		to be increased. Set to zero for unlimited.

		"""
		return self._asyncCall("setMaxListeners", n)

	set_max_listeners = _aliasFor("setMaxListeners")

	#allDbs plug-in
	@abc.abstractmethod
	def allDbs(self):
		"""Wraps the pouchdb-all-dbs plug-in. Returns a list of the
		names of all local databases.

		"""

	all_dbs = _aliasFor("allDbs")

	@abc.abstractmethod
	def resetAllDbs(self):
		"""Wraps the pouchdb-all-dbs plug-in. Destroys the separate
		allDbs database. You should never need to call this function.

		"""

	reset_all_dbs = _aliasFor("resetAllDbs")

class AsyncEnvironment(AbstractEnvironment):
	def __init__(self, *args, **kwargs):
		super(AsyncEnvironment, self).__init__(AsyncPouchDB, *args, **kwargs)

	def destroy(self, name_=None, callback=None, **options):
		if callable(name_):
			callback = name_
			name_ = None
		return self._asyncCall("destroy", name_, options, callback)

	def replicate(self, source, target, **options):
		return self._asyncCall("replicate", source, target, options)

	def sync(self, source, target, **options):
		return self._asyncCall("sync", source, target, options)

	#allDbs plugin
	def allDbs(self, callback=None):
		return self._asyncCall("allDbs", callback)

	def resetAllDbs(self, callback=None):
		return self._asyncCall("resetAllDbs", callback)

class SyncEnvironment(AbstractEnvironment, collections.Mapping):
	"""This class is a Mapping, which means it can be used like a
	:class:`dict`. (Except for setting values, in this case).

	See for all the methods that being a Mapping offers, `the docs about
	it`_.

	.. _the docs about it: https://docs.python.org/2/library/collections.html#collections-abstract-base-classes

	>>> env = setup()
	>>> env.keys() #doctest: +ELLIPSIS
	[...]

	"""
	def __init__(self, *args, **kwargs):
		super(SyncEnvironment, self).__init__(SyncPouchDB, *args, **kwargs)		

	def __delitem__(self, dbName):
		"""A shortcut for the :meth:`AbstractEnvironment.destroy`
		method. The last two of the  following lines of code are
		equivalent:

		>>> env = setup()
		>>> del env["test"]
		>>> env.destroy("test")

		"""
		self.destroy(dbName)

	def __iter__(self):
		return iter(self.allDbs())

	def __len__(self):
		return len(self.allDbs())

	def _syncCall(self, methodName, *args):
		promise = self._ctx.callStatic(methodName, *_filterNone(args))
		return _getPromiseResponse(self._ctx, promise)

	def _callFunc(self, options):
		if options.get("live", False) or options.get("continuous", False):
			return self._asyncCall
		return self._syncCall

	def destroy(self, name_=None, **options):
		self._syncCall("destroy", name_, options)

	def replicate(self, source, target, **options):
		"""When the ``live`` or ``continuous`` option is active, this
		method acts like its asynchronous equivalent.

		"""
		return self._callFunc(options)("replicate", source, target, options)

	def sync(self, source, target, **options):
		"""When the ``live`` or ``continuous`` option is active, this
		method acts like its asynchronous equivalent.

		"""
		return self._callFunc(options)("sync", source, target, options)

	#allDbs plug-in
	def allDbs(self):
		return self._syncCall("allDbs")

	def resetAllDbs(self):
		return self._syncCall("resetAllDbs")

#Caching prevents identical environments from being created which saves
#quite a bit of memory and CPU. On top of that, a reference to every
#environment needs to be kept anyway to prevent segfaulting.
_envs = {}
def setup(storageDir=None, async=False, baseUrl="file:///"):
	"""Sets up an environment which allows access to the rest of the
	API, which mostly consists out of wrappers around PouchDB's
	functions. This environment is then returned to the user.

	Depending on the ``async`` parameter, this is either an instance of
	:class:`SyncEnvironment` or :class:`AsyncEnvironment`.

	The ``storageDir`` is created automatically if it doesn't already
	exist. It can be relative, and should be a directory (not a file).
	It's where databases are saved (or more specific: WebKit's backend
	database files). When it is ``None`` (the default), a temporary
	directory is created by Python-PouchDB, which is also removed at
	process exit. This function can raise an :exc:`EnvironmentError`
	when a ``storageDir`` other than one used earlier is passed in as a
	parameter. (That's a Qt restriction, unfortunately.)

	In older versions of QtWebKit, the same-origin policy is a little
	too strict which makes it impossible to replicate with databases
	that aren't on the same domain as ``baseUrl``. In newer versions, as
	long as ``baseUrl`` is file:///, this problem doesn't exist. When
	you need to support the older version, you can set this to a domain
	so you can at least replicate to one site.

	"""
	if not storageDir:
		storageDir = tempfile.mkdtemp()
		_tempDirs.add(storageDir)
	if not (storageDir, async, baseUrl) in _envs:
		js = _getJs()
		try:
			ctx = context.JSContext(js, "PouchDB", _IGNORED_ERRORS, storageDir, baseUrl)
		except ValueError, e:
			if "offlineStoragePath" in str(e): #pragma: no branch
				raise EnvironmentError("Can't use the value '%s' for storageDir. It has already been set to something else and, because of a backend restriction, can't be changed." % storageDir)
			#this shouldn't happen, it's just there so if it does happen
			#during development sometime in the future, the error is
			#shown in a nicer way.
			raise #pragma: no cover

		Environment = AsyncEnvironment if async else SyncEnvironment
		_envs[(storageDir, async, baseUrl)] = Environment(ctx)
	return _envs[(storageDir, async, baseUrl)]

def _getJs(_cache={}):
	if not "js" in _cache:
		jsPath = os.path.join(os.path.dirname(__file__), "bundle.js")
		with open(jsPath) as f:
			_cache["js"] = f.read()
	return _cache["js"]

_tempDirs = set()
def _removeTempDirs():#pragma: no cover
	"""Not covered because coverage.py can't cover functions only
	executed atexit.

	"""
	for tempDir in _tempDirs:
		shutil.rmtree(tempDir)

atexit.register(_removeTempDirs)
