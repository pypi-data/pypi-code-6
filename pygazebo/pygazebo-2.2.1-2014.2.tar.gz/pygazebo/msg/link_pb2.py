# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)


import header_pb2
import inertial_pb2
import collision_pb2
import visual_pb2
import sensor_pb2
import projector_pb2
import pose_pb2

DESCRIPTOR = descriptor.FileDescriptor(
  name='link.proto',
  package='gazebo.msgs',
  serialized_pb='\n\nlink.proto\x12\x0bgazebo.msgs\x1a\x0cheader.proto\x1a\x0einertial.proto\x1a\x0f\x63ollision.proto\x1a\x0cvisual.proto\x1a\x0csensor.proto\x1a\x0fprojector.proto\x1a\npose.proto\"\xd5\x02\n\x04Link\x12\n\n\x02id\x18\x01 \x01(\r\x12\x0c\n\x04name\x18\x02 \x02(\t\x12\x14\n\x0cself_collide\x18\x03 \x01(\x08\x12\x0f\n\x07gravity\x18\x04 \x01(\x08\x12\x11\n\tkinematic\x18\x05 \x01(\x08\x12\x0f\n\x07\x65nabled\x18\x06 \x01(\x08\x12\'\n\x08inertial\x18\x07 \x01(\x0b\x32\x15.gazebo.msgs.Inertial\x12\x1f\n\x04pose\x18\x08 \x01(\x0b\x32\x11.gazebo.msgs.Pose\x12#\n\x06visual\x18\t \x03(\x0b\x32\x13.gazebo.msgs.Visual\x12)\n\tcollision\x18\n \x03(\x0b\x32\x16.gazebo.msgs.Collision\x12#\n\x06sensor\x18\x0b \x03(\x0b\x32\x13.gazebo.msgs.Sensor\x12)\n\tprojector\x18\x0c \x03(\x0b\x32\x16.gazebo.msgs.Projector')




_LINK = descriptor.Descriptor(
  name='Link',
  full_name='gazebo.msgs.Link',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='id', full_name='gazebo.msgs.Link.id', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='name', full_name='gazebo.msgs.Link.name', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='self_collide', full_name='gazebo.msgs.Link.self_collide', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='gravity', full_name='gazebo.msgs.Link.gravity', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='kinematic', full_name='gazebo.msgs.Link.kinematic', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='enabled', full_name='gazebo.msgs.Link.enabled', index=5,
      number=6, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='inertial', full_name='gazebo.msgs.Link.inertial', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='pose', full_name='gazebo.msgs.Link.pose', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='visual', full_name='gazebo.msgs.Link.visual', index=8,
      number=9, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='collision', full_name='gazebo.msgs.Link.collision', index=9,
      number=10, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='sensor', full_name='gazebo.msgs.Link.sensor', index=10,
      number=11, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='projector', full_name='gazebo.msgs.Link.projector', index=11,
      number=12, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=132,
  serialized_end=473,
)

_LINK.fields_by_name['inertial'].message_type = inertial_pb2._INERTIAL
_LINK.fields_by_name['pose'].message_type = pose_pb2._POSE
_LINK.fields_by_name['visual'].message_type = visual_pb2._VISUAL
_LINK.fields_by_name['collision'].message_type = collision_pb2._COLLISION
_LINK.fields_by_name['sensor'].message_type = sensor_pb2._SENSOR
_LINK.fields_by_name['projector'].message_type = projector_pb2._PROJECTOR
DESCRIPTOR.message_types_by_name['Link'] = _LINK

class Link(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _LINK
  
  # @@protoc_insertion_point(class_scope:gazebo.msgs.Link)

# @@protoc_insertion_point(module_scope)
