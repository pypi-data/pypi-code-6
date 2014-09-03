from stream import Stream
from counter import Counter
from helper import Helper
from sink import Sink

class ComponentStream(Stream):
  def sink(self, name=None, fields=None):
    self.outputs(name, fields)

  def outputs(self, name=None, fields=None, relation=None, scope=None):
    node = Sink(name, fields, relation, scope)
    Helper.check_name("outputs", node._name, self._app._names)
    Helper.check_component_sink(node)
    self._app._nodes.append(node)

    if(self._app._options["command"] == "info"):
      node_hash = {"name":node._name, "type":node._type, "columns":node._columns, "relation":node._relation, "scope":node._scope}
      Helper.write_node_to_file(node_hash, self._app._info_file)
      arc_hash = {"name":self._name, "origin":self._previous_node_name, "dest":node._name}
      Helper.write_arc_to_file(arc_hash, self._app._info_file)
