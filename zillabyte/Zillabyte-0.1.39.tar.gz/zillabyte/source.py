import traceback
from counter import Counter
from controller import ParentDeadException, UserEndCycleException

class Source:
  def __init__(self, name, matches, options, emits, end_cycle_policy, begin_cycle, next_tuple):
    self._name = name if name else "source_"+Counter.get()
    self._type = "source"
    self._matches = None
    self._relation = None
    self._end_cycle_policy = None

    if(matches != None):
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

  def run(self, controller):
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
