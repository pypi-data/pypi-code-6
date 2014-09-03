from controller import *
from counter import Counter
from helper import Helper
from stream import *
from source import Source
from base import Base
from version import VERSION

class App(Base):
  def __init__(self, name=None):
    Base.__init__(self, name)
    Helper.check_name("app", self._name, {})
    self._options = Helper.opt_parser()

    if(self._options["command"] == "info"):
      self._info_file = open(self._options["file"], "w+")
      Helper.write_hash_to_file({"language":"python", "name":self._name, "flow_type":"app", "multilang_version":VERSION}, self._info_file)

  def source(self, name=None, matches=None, options={}, emits=None, end_cycle_policy="null_emit", begin_cycle=None, next_tuple=None):
    if(matches != None):
      Helper.check_matches(matches)
    node = Source(name, matches, options, emits, end_cycle_policy, begin_cycle, next_tuple)
    Helper.check_name("source", node._name, self._names)
    Helper.check_source(node)
    Helper.check_emits("source", node._emits, self._streams)
    self._nodes.append(node)

    if(self._options["command"] == "info"):
      node_hash = {"name":node._name, "type":node._type}
      if(node._relation):
        node_hash["relation"] = node._relation
      elif(node._matches):
        node_hash["matches"] = node._matches
      else:
        node_hash["end_cycle_policy"] = node._end_cycle_policy
      Helper.write_node_to_file(node_hash, self._info_file)
    elif self._options["command"] == "execute" and self._options["name"] == node._name:
      pipe_name = self._options.get("pipe","")
      controller = Controller(pipe_name, node._emits)
      node.run(controller)

    output_streams = []
    for stream in node._emits:
      output_streams.append(Stream(stream, self, node._name))
    if len(output_streams) == 1:
      output_streams = output_streams[0]

    return output_streams
