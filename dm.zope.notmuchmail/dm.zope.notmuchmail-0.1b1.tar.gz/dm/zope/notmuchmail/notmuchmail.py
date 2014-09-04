# Copyright (C) 2012 by Dr. Dieter Maurer <dieter@handshake.de>
# All rights resevered -- see "LICENSE.txt" for details.
"""Utility interface to a `notmuch` database."""
from threading import local
from os import stat
from os.path import join

from zope.interface import implements
from ZODB.POSException import ConflictError

from decorator import decorator

from notmuch.errors import XapianError, NullPointerError
from notmuch import Query, Messages, Message, Tags, Threads, Thread, Database

from dm.zope.notmuchmail.interfaces import INotMuchDatabase


@decorator
def retry(f, *args, **kw):
  try: return f(*args, **kw)
  except (XapianError, NullPointerError):
    # an exception that indicates that reopening may solve the problem
    if args[0].root.reopen(): raise NotMuchConflict
    raise


NEEDS_WRAPPING = (Query, Messages, Message, Tags, Threads, Thread)
def _wrap(o, parent):
  if isinstance(o, NEEDS_WRAPPING): return _Delegator(o, parent)
  return o

@decorator
def delegator_wrap(f, *args, **kw):
  return _wrap(f(*args, **kw), args[0])


class NotMuchDatabase(object):
  """Utility implementation providing access to a thread local database.

  Initialize with the path to the maildir indexed by `notmuch`.
  """
  implements(INotMuchDatabase)

  def __init__(self, path=None):
    if path is None: path = Database(None).get_path()
    self.path = path

  storage = local()

  @retry
  @delegator_wrap
  def create_query(self, querystring):
    return self._get_db().create_query(querystring)
    
  def _get_db(self):
    s = self.storage
    db = getattr(s, "db", None)
    ts = self._get_timestamp()
    if db is None or s.ts != ts:
      db = s.db = _Delegator(Database(self.path), self)
      s.ts = ts
    return db

  def _get_timestamp(self):
    return stat(join(self.path, ".notmuch", "xapian", "flintlock")).st_mtime

  def reopen(self):
    return self._get_timestamp() != self.storage.ts

  @property
  def root(self): return self




class _Delegator(object):
  """Auxiliary class delegating to a `notmuch` object.

  It should work around the problems of the `hiararchical storage` used by
  `notmuch` which forces the application to hold a reference to a parent
  as long as the child is live. The class does this in a transparent way.
  """
  def __init__(self, to, parent):
    self.__to, self.__parent = to, parent

  @retry
  @delegator_wrap
  def __getattr__(self, key):
    a = getattr(self.__to, key)
    if callable(a): return _CallDelegator(a, self)
    return a

  @property
  def root(self):
    return self.__parent.root

  def __iter__(self):
    if isinstance(self.__to, (Threads, Messages, Tags)): return self
    raise AttributeError

  @retry
  @delegator_wrap
  def next(self): return self.__to.next()


class _CallDelegator(object):
  """Auxiliary class to call a method and wrap its result, if necessary."""
  def __init__(self, method, parent):
    self.__method, self.__parent = method, parent

  @retry
  def __call__(self, *args, **kw):
    return _wrap(self.__method(*args, **kw), self.__parent)


class NotMuchConflict(ConflictError):
  """raised in case a retrial might be successful."""
