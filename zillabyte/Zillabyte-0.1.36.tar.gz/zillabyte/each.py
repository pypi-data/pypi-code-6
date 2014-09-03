import traceback
from counter import Counter
from controller import ParentDeadException

class Each:

  def __init__(self, name, emits, output_format, prepare, execute, parallelism):
    self._name = name if name else "each_"+Counter.get()
    self._type = "each"
    self._output_format = output_format

    if emits == None:
      emits = ["stream_"+Counter.get()]
    elif isinstance(emits, basestring):
      emits = [emits]
    self._emits = emits

    self._prepare = prepare
    self._execute = execute
    self._parallelism = parallelism

  def run(self, controller):
    controller.get_pidDir()
    if self._prepare != None:
      self._prepare(controller)

    try:
      while True:
        d = controller.read()
        if d == None:
          continue
        tup = controller.get_tuple(d)
        if tup == None:
          continue
        try:
          self._execute(controller, tup)
          controller.done()
        except:
          controller.log("Error in execute function")
          raise
    except KeyboardInterrupt:
      raise
    except ParentDeadException, e:
      controller.log("jvm appears to have died")
      raise
    except:
      controller.log("Exception in each: "+traceback.format_exc())
