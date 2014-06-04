# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)


import header_pb2
import time_pb2

DESCRIPTOR = descriptor.FileDescriptor(
  name='world_stats.proto',
  package='gazebo.msgs',
  serialized_pb='\n\x11world_stats.proto\x12\x0bgazebo.msgs\x1a\x0cheader.proto\x1a\ntime.proto\"\xbc\x01\n\x0fWorldStatistics\x12#\n\x08sim_time\x18\x02 \x02(\x0b\x32\x11.gazebo.msgs.Time\x12%\n\npause_time\x18\x03 \x02(\x0b\x32\x11.gazebo.msgs.Time\x12$\n\treal_time\x18\x04 \x02(\x0b\x32\x11.gazebo.msgs.Time\x12\x0e\n\x06paused\x18\x05 \x02(\x08\x12\x12\n\niterations\x18\x06 \x02(\x04\x12\x13\n\x0bmodel_count\x18\x07 \x01(\x05')




_WORLDSTATISTICS = descriptor.Descriptor(
  name='WorldStatistics',
  full_name='gazebo.msgs.WorldStatistics',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='sim_time', full_name='gazebo.msgs.WorldStatistics.sim_time', index=0,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='pause_time', full_name='gazebo.msgs.WorldStatistics.pause_time', index=1,
      number=3, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='real_time', full_name='gazebo.msgs.WorldStatistics.real_time', index=2,
      number=4, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='paused', full_name='gazebo.msgs.WorldStatistics.paused', index=3,
      number=5, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='iterations', full_name='gazebo.msgs.WorldStatistics.iterations', index=4,
      number=6, type=4, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='model_count', full_name='gazebo.msgs.WorldStatistics.model_count', index=5,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=61,
  serialized_end=249,
)

_WORLDSTATISTICS.fields_by_name['sim_time'].message_type = time_pb2._TIME
_WORLDSTATISTICS.fields_by_name['pause_time'].message_type = time_pb2._TIME
_WORLDSTATISTICS.fields_by_name['real_time'].message_type = time_pb2._TIME
DESCRIPTOR.message_types_by_name['WorldStatistics'] = _WORLDSTATISTICS

class WorldStatistics(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _WORLDSTATISTICS
  
  # @@protoc_insertion_point(class_scope:gazebo.msgs.WorldStatistics)

# @@protoc_insertion_point(module_scope)
