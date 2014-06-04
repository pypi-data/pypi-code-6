# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)


import vector3d_pb2
import time_pb2
import joint_wrench_pb2

DESCRIPTOR = descriptor.FileDescriptor(
  name='contact.proto',
  package='gazebo.msgs',
  serialized_pb='\n\rcontact.proto\x12\x0bgazebo.msgs\x1a\x0evector3d.proto\x1a\ntime.proto\x1a\x12joint_wrench.proto\"\xea\x01\n\x07\x43ontact\x12\x12\n\ncollision1\x18\x01 \x02(\t\x12\x12\n\ncollision2\x18\x02 \x02(\t\x12\'\n\x08position\x18\x03 \x03(\x0b\x32\x15.gazebo.msgs.Vector3d\x12%\n\x06normal\x18\x04 \x03(\x0b\x32\x15.gazebo.msgs.Vector3d\x12\r\n\x05\x64\x65pth\x18\x05 \x03(\x01\x12(\n\x06wrench\x18\x06 \x03(\x0b\x32\x18.gazebo.msgs.JointWrench\x12\x1f\n\x04time\x18\x07 \x02(\x0b\x32\x11.gazebo.msgs.Time\x12\r\n\x05world\x18\x08 \x02(\t')




_CONTACT = descriptor.Descriptor(
  name='Contact',
  full_name='gazebo.msgs.Contact',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='collision1', full_name='gazebo.msgs.Contact.collision1', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='collision2', full_name='gazebo.msgs.Contact.collision2', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='position', full_name='gazebo.msgs.Contact.position', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='normal', full_name='gazebo.msgs.Contact.normal', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='depth', full_name='gazebo.msgs.Contact.depth', index=4,
      number=5, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='wrench', full_name='gazebo.msgs.Contact.wrench', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='time', full_name='gazebo.msgs.Contact.time', index=6,
      number=7, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='world', full_name='gazebo.msgs.Contact.world', index=7,
      number=8, type=9, cpp_type=9, label=2,
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
  serialized_start=79,
  serialized_end=313,
)

_CONTACT.fields_by_name['position'].message_type = vector3d_pb2._VECTOR3D
_CONTACT.fields_by_name['normal'].message_type = vector3d_pb2._VECTOR3D
_CONTACT.fields_by_name['wrench'].message_type = joint_wrench_pb2._JOINTWRENCH
_CONTACT.fields_by_name['time'].message_type = time_pb2._TIME
DESCRIPTOR.message_types_by_name['Contact'] = _CONTACT

class Contact(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _CONTACT
  
  # @@protoc_insertion_point(class_scope:gazebo.msgs.Contact)

# @@protoc_insertion_point(module_scope)
