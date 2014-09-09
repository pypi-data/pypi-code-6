from counter import Counter

class ComponentSource:
  def __init__(self, name, fields):
    self._name = name
    self._type = "source"

    self._emits = ["stream_"+Counter.get()]
    self._fields = fields
