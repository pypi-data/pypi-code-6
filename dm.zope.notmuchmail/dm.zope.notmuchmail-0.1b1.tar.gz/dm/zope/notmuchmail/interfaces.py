# Copyright (C) 2012 by Dr. Dieter Maurer <dieter@handshake.de>
# All rights resevered -- see "LICENSE.txt" for details.
from zope.interface import Interface, Attribute
from zope.interface.common.sequence import IMinimalSequence

class INotMuchDatabase(Interface):
  """An `INotMuch` database."""

  def create_query(querystring):
    """create query for *querystring*."""


class IAdditionalHeaderItems(IMinimalSequence):
  """provides additional header items.

  The result is a sequence of *name*, *value* pairs.
  """
