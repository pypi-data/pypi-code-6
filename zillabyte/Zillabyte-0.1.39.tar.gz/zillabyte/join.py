from counter import Counter

class Join:
  def __init__(self, name, emits, fields, options):
    self._name = name if name else "join_"+Counter.get()
    self._type = "join"

    if emits == None:
      emits = ["stream_"+Counter.get()]
    elif isinstance(emits, basestring):
      emits = [emits]
    self._emits = emits

    if fields:
      if isinstance(fields, list) and len(fields) == 2:
        self._lhs_fields = fields[0]
        self._rhs_fields = fields[1]
      elif isinstance(fields, basestring):
        self._lhs_fields = fields
        self._rhs_fields = fields

    self._join_type = "inner"
    if options:
      if options["type"]:
        self._join_type = options["type"]
