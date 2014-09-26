import traceback
from counter import Counter
from controller import Controller, ParentDeadException, UserEndCycleException
from helper import Helper

class Source:
  def __init__(self, app):
    self._app = app

  def build_node(self, name, matches, options, emits, end_cycle_policy, begin_cycle, next_tuple):
    self._name = name if name else "source_"+Counter.get()
    self._type = "source"
    self._options = options
    self._matches = None
    self._relation = None
    self._end_cycle_policy = None

    if(matches != None):
      Helper.check_matches(matches)
      if isinstance(matches, basestring):
        if not isinstance(options, dict):
          options = {}
        self._relation = {"query": matches, "options": options}
      elif isinstance(matches, list):
        self._matches = matches
    else:
      self._end_cycle_policy = end_cycle_policy

    if emits == None:
      emits = ["stream_"+Counter.get()]
    elif isinstance(emits, basestring):
      emits = [emits]
    self._emits = emits

    self._begin_cycle = begin_cycle
    self._next_tuple = next_tuple

    Helper.check_name("source", self._name, self._app._names)
    Helper.check_source(self)
    Helper.check_emits("source", self._emits, self._app._streams)

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
          controller.log("Not a command")
        elif d["command"] == "begin_cycle":
          if(self._begin_cycle != None):
            self._begin_cycle(controller)
        elif d["command"] == "next":
            self._next_tuple(controller)
        elif d["command"] == "ack":
          controller.ack(d.get("id",None))
        elif d["command"] == "fail":
          controller.fail(d.get("id",None))
        else:
          controller.log("Invalid command")
      except UserEndCycleException, e:
        pass
      except KeyboardInterrupt:
        raise
      except ParentDeadException, e:
        controller.log("jvm appears to have died")
        raise
      except:
        controller.fail("Exception in source: "+traceback.format_exc())
      controller.done()
