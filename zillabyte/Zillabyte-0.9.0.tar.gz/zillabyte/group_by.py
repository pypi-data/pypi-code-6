import traceback
from counter import Counter
from controller import Controller, ParentDeadException
from helper import Helper

class GroupBy:
  def __init__(self, app):
    self._app = app
  
  def build_node(self, name, emits, fields, begin_group, aggregate, end_group, parallelism):
    self._name = name if name else "group_by_"+Counter.get()
    self._type = "group_by"

    self._group_by = fields
    if emits == None:
      emits = ["stream_"+Counter.get()]
    elif isinstance(emits, basestring):
      emits = [emits]
    self._emits = emits

    self._begin_group = begin_group
    self._aggregate = aggregate
    self._end_group = end_group
    self._parallelism = parallelism

    Helper.check_name("group_by", self._name, self._app._names)
    Helper.check_group_by(self)
    Helper.check_emits("group_by", self._emits, self._app._streams)

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
        elif "command" not in d:
          controller.log("Not a command "+str(d))
        elif d["command"] == "prepare":
          if self._prepare != None:
            self._prepare(controller)
        elif d["command"] == "begin_group":
          tup = controller.get_tuple(d)
          if tup == None:
            continue
          self._begin_group(controller, tup)
        elif d["command"] == "aggregate":
          tup = controller.get_tuple(d)
          if tup == None:
            continue
          self._aggregate(controller, tup)
        elif d["command"] == "end_group":
          self._end_group(controller)
        else:
          controller.log("Invalid command")
      except ParentDeadException, e:
        controller.log("jvm appears to have died")
        raise
      except KeyboardInterrupt:
        raise
      except:
        controller.fail("Exception in group_by: "+traceback.format_exc())
      controller.done()
