from controller import *
from counter import Counter
from helper import Helper
from component_stream import ComponentStream
from component_source import ComponentSource
from base import Base
from version import VERSION

class Component(Base):
  def __init__(self, name=None):
    Base.__init__(self, name)
    Helper.check_name("component", self._name, {})
    self._options = Helper.opt_parser()

    if(self._options["command"] == "info"):
      self._info_file = open(self._options["file"], "w+")
      Helper.write_hash_to_file({"language":"python", "name":self._name, "flow_type":"component", "multilang_version":VERSION}, self._info_file)

  def inputs(self, name=None, fields=None):
    node = ComponentSource(name, fields)
    Helper.check_name("inputs", node._name, self._names)
    Helper.check_component_source(node)

    self._nodes.append(node)

    if(self._options["command"] == "info"):
      node_hash = {"name":node._name, "type":node._type, "fields":node._fields}
      Helper.write_node_to_file(node_hash, self._info_file)

    # component inputs only specify one output stream at a time
    output_stream = ComponentStream(node._emits[0], self, node._name)
    return output_stream
