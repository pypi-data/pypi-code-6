# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)



DESCRIPTOR = descriptor.FileDescriptor(
  name='world_modify.proto',
  package='gazebo.msgs',
  serialized_pb='\n\x12world_modify.proto\x12\x0bgazebo.msgs\"A\n\x0bWorldModify\x12\x12\n\nworld_name\x18\x01 \x02(\t\x12\x0e\n\x06remove\x18\x02 \x01(\x08\x12\x0e\n\x06\x63reate\x18\x03 \x01(\x08')




_WORLDMODIFY = descriptor.Descriptor(
  name='WorldModify',
  full_name='gazebo.msgs.WorldModify',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='world_name', full_name='gazebo.msgs.WorldModify.world_name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='remove', full_name='gazebo.msgs.WorldModify.remove', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='create', full_name='gazebo.msgs.WorldModify.create', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=35,
  serialized_end=100,
)

DESCRIPTOR.message_types_by_name['WorldModify'] = _WORLDMODIFY

class WorldModify(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _WORLDMODIFY
  
  # @@protoc_insertion_point(class_scope:gazebo.msgs.WorldModify)

# @@protoc_insertion_point(module_scope)
