import traceback
from counter import Counter
from controller import Controller, ParentDeadException
from helper import Helper

class Each:
  def __init__(self, app):
    self._app = app

  def build_node(self, name, emits, output_format, prepare, execute, parallelism):
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

    Helper.check_name("each", self._name, self._app._names)
    Helper.check_each(self)
    Helper.check_emits("each", self._emits, self._app._streams)

  def run_operation(self):
    host = self._app._options.get("host", None)
    port = self._app._options.get("port", None)
    controller = Controller(host, port, self._emits)

    controller.get_pidDir()

    while True:
      try:
        d = controller.read()
        if d == None:
          continue
        elif "command" in d and d["command"] == "prepare":
          if self._prepare != None:
            self._prepare(controller)
        else:
          tup = controller.get_tuple(d)
          if tup == None:
            continue
          self._execute(controller, tup)
      except KeyboardInterrupt:
        raise
      except ParentDeadException, e:
        controller.log("jvm appears to have died")
        raise
      except:
        controller.fail("Exception in each: "+traceback.format_exc())
      controller.done()
