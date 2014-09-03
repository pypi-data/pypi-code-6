import traceback
from controller import *
from counter import Counter
from helper import Helper
from each import Each
from filter import Filter
from group_by import GroupBy
from join import Join
from injected_component import InjectedComponent
from sink import Sink

class Stream:
  def __init__(self, name, app, previous_node_name):
    self._name = name
    self._app = app
    self._previous_node_name = previous_node_name

  def each(self, name=None, emits=None, output_format="replace", prepare=None, execute=None, parallelism=None):
    node = Each(name, emits, output_format, prepare, execute, parallelism)

    Helper.check_name("each", node._name, self._app._names)
    Helper.check_each(node)
    Helper.check_emits("each", node._emits, self._app._streams)
    self._app._nodes.append(node)

    if(self._app._options["command"] == "info"):
      node_hash = {"name":node._name, "type":node._type, "output_format":node._output_format}

      if node._parallelism != None:
        node_hash["parallelism"] = node._parallelism

      Helper.write_node_to_file(node_hash, self._app._info_file)
      arc_hash = {"name":self._name, "origin":self._previous_node_name, "dest":node._name}
      Helper.write_arc_to_file(arc_hash, self._app._info_file)
    elif self._app._options["command"] == "execute" and self._app._options["name"] == node._name:
      pipe_name = self._app._options.get("pipe","")
      controller = Controller(pipe_name, node._emits)
      node.run(controller)

    output_streams = []
    for stream in node._emits:
      output_streams.append(self.__class__(stream, self._app, node._name))
    if len(output_streams) == 1:
      output_streams = output_streams[0]

    return output_streams

  def filter(self, name=None, emits=None, prepare=None, keep=None, parallelism=None):
    node = Filter(name, emits, prepare, keep, parallelism)
    Helper.check_name("filter", node._name, self._app._names)
    Helper.check_filter(node)
    Helper.check_emits("filter", node._emits, self._app._streams)
    self._app._nodes.append(node)

    if(self._app._options["command"] == "info"):
      node_hash = {"name":node._name, "type":node._type}
      
      if node._parallelism != None:
        node_hash["parallelism"] = node._parallelism

      Helper.write_node_to_file(node_hash, self._app._info_file)
      arc_hash = {"name":self._name, "origin":self._previous_node_name, "dest":node._name}
      Helper.write_arc_to_file(arc_hash, self._app._info_file)
    elif self._app._options["command"] == "execute" and self._app._options["name"] == node._name:
      pipe_name = self._app._options.get("pipe", "")
      controller = Controller(pipe_name, node._emits)
      node.run(controller)

    output_stream = self.__class__(node._emits[0], self._app, node._name) # filters only have one output stream
    return output_stream

  def group_by(self, name=None, emits=None, fields=None, begin_group=None, aggregate=None, end_group=None, parallelism=None):
    node = GroupBy(name, emits, fields, begin_group, aggregate, end_group, parallelism)
    Helper.check_name("group_by", node._name, self._app._names)
    Helper.check_group_by(node)
    Helper.check_emits("group_by", node._emits, self._app._streams)
    self._app._nodes.append(node)

    if(self._app._options["command"] == "info"):
      node_hash = {"name":node._name, "type":node._type, "group_by":node._group_by}
      if node._parallelism != None:
        node_hash["parallelism"] = node._parallelism
        
      Helper.write_node_to_file(node_hash, self._app._info_file)
      arc_hash = {"name":self._name, "origin":self._previous_node_name, "dest":node._name}
      Helper.write_arc_to_file(arc_hash, self._app._info_file)
    elif self._app._options["command"] == "execute" and self._app._options["name"] == node._name:
      pipe_name = self._app._options.get("pipe","")
      controller = Controller(pipe_name, node._emits)
      node.run(controller)

    output_streams = []
    for stream in node._emits:
      output_streams.append(self.__class__(stream, self._app, node._name))
    if len(output_streams) == 1:
      output_streams = output_streams[0]

    return output_streams

  def join_with(self, name=None, rh_stream=None, emits=None, fields=None, options=None):
    node = Join(name, emits, fields, options)
    Helper.check_name("join", node._name, self._app._names)
    Helper.check_join(node)
    Helper.check_emits("join", node._emits, self._app._streams)
    self._app._nodes.append(node)

    if(self._app._options["command"] == "info"):
      node_hash = {"name":node._name, "type":node._type, "lhs_fields":node._lhs_fields, "rhs_fields":node._rhs_fields, "join_type":node._join_type}
         
      Helper.write_node_to_file(node_hash, self._app._info_file)
      arc_hash1 = {"name":self._name, "origin":self._previous_node_name, "dest":node._name, "left":1}
      Helper.write_arc_to_file(arc_hash1, self._app._info_file)
      arc_hash2 = {"name":rh_stream._name, "origin":rh_stream._previous_node_name, "dest":node._name, "right":1}
      Helper.write_arc_to_file(arc_hash2, self._app._info_file)

    output_stream = self.__class__(node._emits[0], self._app, node._name)
    return output_stream

  def call_component(self, name=None, component_id=None, additional_inputs=None, outputs=None, output_format="replace"):
    node = InjectedComponent(name, component_id, additional_inputs, outputs, output_format)
    Helper.check_name("component", node._name, self._app._names)
    Helper.check_call_component(node)
    Helper.check_emits("component", node._emits, self._app._streams)
    self._app._nodes.append(node)

    if(self._app._options["command"] == "info"):
      node_hash = {"name":node._name, "type":node._type, "id":node._id, "output_format":node._output_format}
      Helper.write_node_to_file(node_hash, self._app._info_file)
      arc_hash = {"name":self._name, "origin":self._previous_node_name, "dest":node._name}
      Helper.write_arc_to_file(arc_hash, self._app._info_file)
      for stream in node._consumes:
        arc_hash = {"name":stream._name, "origin":stream._previous_node_name, "dest":node._name}
        Helper.write_arc_to_file(arc_hash, self._app._info_file)

    output_streams = []
    for stream in node._emits:
      output_streams.append(self.__class__(stream, self._app, node._name))
    if len(output_streams) == 1:
      output_streams = output_streams[0]

    return output_streams 

  def sink(self, name=None, columns=None, relation=None, scope=None):
    node = Sink(name, columns, relation, scope)
    Helper.check_sink(node._name, node._columns, self._app._nodes)
    self._app._nodes.append(node)

    if(self._app._options["command"] == "info"):
      node_hash = {"name":node._name, "type":node._type, "columns":node._columns, "relation":node._relation, "scope":node._scope}
      Helper.write_node_to_file(node_hash, self._app._info_file)
      arc_hash = {"name":self._name, "origin":self._previous_node_name, "dest":node._name}
      Helper.write_arc_to_file(arc_hash, self._app._info_file)
