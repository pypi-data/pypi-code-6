from counter import Counter

class InjectedComponent:
  def __init__(self, name, idn, additional_inputs, outputs, output_format):
    self._name = name if name else "component_"+Counter.get()
    self._id = str(idn)
    self._type = "component"
    self._consumes = []

    if isinstance(additional_inputs, list):
      self._consumes = additional_inputs
    elif additional_inputs != None:
      self._consumes = [additional_inputs]

    if outputs == None:
      outputs = ["stream_"+Counter.get()]
    elif isinstance(outputs, basestring):
      outputs = [outputs]
    self._emits = outputs

    self._output_format = output_format
