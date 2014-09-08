import traceback
from counter import Counter
from controller import ParentDeadException

class Filter:
  def __init__(self, name, emits, prepare, keep, parallelism):
    self._name = name if name else "filter_"+Counter.get()
    self._type = "filter"

    if emits == None:
      emits = ["stream_"+Counter.get()]
    elif isinstance(emits, basestring):
      emits = [emits]
    self._emits = emits

    self._prepare = prepare
    self._keep = keep
    self._parallelism = parallelism


  def run(self, controller):
    controller.get_pidDir()
    if self._prepare != None:
      self._prepare(controller)

    while True:
      try:
        d = controller.read()
        if d == None:
          continue
        tup = controller.get_tuple(d)
        if tup == None:
          continue
        if self._keep(tup):
          controller.emit(tup)
      except KeyboardInterrupt:
        raise
      except ParentDeadException, e:
        controller.log("jvm appears to have died")
        raise
      except:
        controller.fail("Exception in filter: "+traceback.format_exc())
      controller.done()
