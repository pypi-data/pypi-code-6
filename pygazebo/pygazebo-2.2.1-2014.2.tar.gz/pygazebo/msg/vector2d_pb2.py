# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)


import header_pb2

DESCRIPTOR = descriptor.FileDescriptor(
  name='vector2d.proto',
  package='gazebo.msgs',
  serialized_pb='\n\x0evector2d.proto\x12\x0bgazebo.msgs\x1a\x0cheader.proto\" \n\x08Vector2d\x12\t\n\x01x\x18\x01 \x02(\x01\x12\t\n\x01y\x18\x02 \x02(\x01')




_VECTOR2D = descriptor.Descriptor(
  name='Vector2d',
  full_name='gazebo.msgs.Vector2d',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='x', full_name='gazebo.msgs.Vector2d.x', index=0,
      number=1, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='y', full_name='gazebo.msgs.Vector2d.y', index=1,
      number=2, type=1, cpp_type=5, label=2,
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
  serialized_start=45,
  serialized_end=77,
)

DESCRIPTOR.message_types_by_name['Vector2d'] = _VECTOR2D

class Vector2d(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _VECTOR2D
  
  # @@protoc_insertion_point(class_scope:gazebo.msgs.Vector2d)

# @@protoc_insertion_point(module_scope)
