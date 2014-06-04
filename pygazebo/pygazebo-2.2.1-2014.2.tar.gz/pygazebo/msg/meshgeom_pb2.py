# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)


import vector3d_pb2

DESCRIPTOR = descriptor.FileDescriptor(
  name='meshgeom.proto',
  package='gazebo.msgs',
  serialized_pb='\n\x0emeshgeom.proto\x12\x0bgazebo.msgs\x1a\x0evector3d.proto\"k\n\x08MeshGeom\x12\x10\n\x08\x66ilename\x18\x01 \x02(\t\x12$\n\x05scale\x18\x02 \x01(\x0b\x32\x15.gazebo.msgs.Vector3d\x12\x0f\n\x07submesh\x18\x03 \x01(\t\x12\x16\n\x0e\x63\x65nter_submesh\x18\x04 \x01(\x08')




_MESHGEOM = descriptor.Descriptor(
  name='MeshGeom',
  full_name='gazebo.msgs.MeshGeom',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='filename', full_name='gazebo.msgs.MeshGeom.filename', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='scale', full_name='gazebo.msgs.MeshGeom.scale', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='submesh', full_name='gazebo.msgs.MeshGeom.submesh', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='center_submesh', full_name='gazebo.msgs.MeshGeom.center_submesh', index=3,
      number=4, type=8, cpp_type=7, label=1,
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
  serialized_start=47,
  serialized_end=154,
)

_MESHGEOM.fields_by_name['scale'].message_type = vector3d_pb2._VECTOR3D
DESCRIPTOR.message_types_by_name['MeshGeom'] = _MESHGEOM

class MeshGeom(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _MESHGEOM
  
  # @@protoc_insertion_point(class_scope:gazebo.msgs.MeshGeom)

# @@protoc_insertion_point(module_scope)
