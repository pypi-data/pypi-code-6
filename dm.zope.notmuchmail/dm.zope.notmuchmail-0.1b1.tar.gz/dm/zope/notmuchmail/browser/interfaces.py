from zope.interface import Interface

class IUi(Interface):
  """Object marker interface to signal user interface availability."""

class IJqUi(IUi):
  """Object marker interface to signal use of the `JQuery` based user interface."""
