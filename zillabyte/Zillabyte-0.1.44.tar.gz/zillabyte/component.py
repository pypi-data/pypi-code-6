from controller import *
from counter import Counter
from helper import Helper
from component_stream import ComponentStream
from operation_handler import OperationHandler
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
    op = OperationHandler(self, ComponentStream)
    streams = op.build_multilang_operation("component_source", name, fields)\
                .add_operation_properties_to_info("name", "type", "fields")\
                .handle_operation()\
                .get_output_streams()
    return streams
