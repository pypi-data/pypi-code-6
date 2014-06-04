# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)


import vector2d_pb2

DESCRIPTOR = descriptor.FileDescriptor(
  name='camerasensor.proto',
  package='gazebo.msgs',
  serialized_pb='\n\x12\x63\x61merasensor.proto\x12\x0bgazebo.msgs\x1a\x0evector2d.proto\"\xb5\x01\n\x0c\x43\x61meraSensor\x12\x16\n\x0ehorizontal_fov\x18\x01 \x01(\x01\x12)\n\nimage_size\x18\x02 \x01(\x0b\x32\x15.gazebo.msgs.Vector2d\x12\x14\n\x0cimage_format\x18\x03 \x01(\t\x12\x11\n\tnear_clip\x18\x04 \x01(\x01\x12\x10\n\x08\x66\x61r_clip\x18\x05 \x01(\x01\x12\x14\n\x0csave_enabled\x18\x06 \x01(\x08\x12\x11\n\tsave_path\x18\x07 \x01(\t')




_CAMERASENSOR = descriptor.Descriptor(
  name='CameraSensor',
  full_name='gazebo.msgs.CameraSensor',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='horizontal_fov', full_name='gazebo.msgs.CameraSensor.horizontal_fov', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='image_size', full_name='gazebo.msgs.CameraSensor.image_size', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='image_format', full_name='gazebo.msgs.CameraSensor.image_format', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='near_clip', full_name='gazebo.msgs.CameraSensor.near_clip', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='far_clip', full_name='gazebo.msgs.CameraSensor.far_clip', index=4,
      number=5, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='save_enabled', full_name='gazebo.msgs.CameraSensor.save_enabled', index=5,
      number=6, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='save_path', full_name='gazebo.msgs.CameraSensor.save_path', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
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
  serialized_start=52,
  serialized_end=233,
)

_CAMERASENSOR.fields_by_name['image_size'].message_type = vector2d_pb2._VECTOR2D
DESCRIPTOR.message_types_by_name['CameraSensor'] = _CAMERASENSOR

class CameraSensor(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _CAMERASENSOR
  
  # @@protoc_insertion_point(class_scope:gazebo.msgs.CameraSensor)

# @@protoc_insertion_point(module_scope)
