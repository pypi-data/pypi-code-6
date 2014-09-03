class Sink:
  def __init__(self, name, columns, relation, scope):
    self._name = name
    self._type = "sink"
    self._columns = columns

    if relation != None:
      self._relation = relation
    else:
      self._relation = name
    self._scope = scope
