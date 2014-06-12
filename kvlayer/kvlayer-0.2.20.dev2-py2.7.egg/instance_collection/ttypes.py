#
# Autogenerated by Thrift Compiler (0.9.0)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py:new_style,slots
#

from thrift.Thrift import TType, TMessageType, TException, TApplicationException

from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol, TProtocol
try:
  from thrift.protocol import fastbinary
except:
  fastbinary = None



class TypedBlob(object):
  """
  Attributes:
   - serializer: name of the serializer for reading/writing this blob.
  Serializers can be implemented in multiple programming languages,
  e.g. yaml and json.
   - blob: bytes that serializer can load to make an in-memory object
   - config: dictionary of configuration information to pass into the
  serializer.  For example, in python, this is passed to
  my_serializer.configure(config)
  """

  __slots__ = [ 
    'serializer',
    'blob',
    'config',
   ]

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'serializer', None, None, ), # 1
    (2, TType.STRING, 'blob', None, None, ), # 2
    (3, TType.MAP, 'config', (TType.STRING,None,TType.STRING,None), {
    }, ), # 3
  )

  def __init__(self, serializer=None, blob=None, config=thrift_spec[3][4],):
    self.serializer = serializer
    self.blob = blob
    if config is self.thrift_spec[3][4]:
      config = {
    }
    self.config = config

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.serializer = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRING:
          self.blob = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.MAP:
          self.config = {}
          (_ktype1, _vtype2, _size0 ) = iprot.readMapBegin() 
          for _i4 in xrange(_size0):
            _key5 = iprot.readString();
            _val6 = iprot.readString();
            self.config[_key5] = _val6
          iprot.readMapEnd()
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('TypedBlob')
    if self.serializer is not None:
      oprot.writeFieldBegin('serializer', TType.STRING, 1)
      oprot.writeString(self.serializer)
      oprot.writeFieldEnd()
    if self.blob is not None:
      oprot.writeFieldBegin('blob', TType.STRING, 2)
      oprot.writeString(self.blob)
      oprot.writeFieldEnd()
    if self.config is not None:
      oprot.writeFieldBegin('config', TType.MAP, 3)
      oprot.writeMapBegin(TType.STRING, TType.STRING, len(self.config))
      for kiter7,viter8 in self.config.items():
        oprot.writeString(kiter7)
        oprot.writeString(viter8)
      oprot.writeMapEnd()
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, getattr(self, key))
      for key in self.__slots__]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    for attr in self.__slots__:
      my_val = getattr(self, attr)
      other_val = getattr(other, attr)
      if my_val != other_val:
        return False
    return True

  def __ne__(self, other):
    return not (self == other)


class BlobCollection(object):
  """
  BlobCollection is a simple thrift struct containing a map that
  carries TypedBlobs of data that can be lazily deserialized as
  needed.  Thrift handles the fast (de)marshalling of long strings.
  By making this a thrift class, we can also utilize the
  streamcorpus.Chunk convenience methods.

  Attributes:
   - collection_type: Type of the collection this represents.  The collection type
  defines the type of the objects stored in typed_blobs.
   - typed_blobs: Data in the collection, a map of key to actual data.
  """

  __slots__ = [ 
    'collection_type',
    'typed_blobs',
   ]

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'collection_type', None, None, ), # 1
    (2, TType.MAP, 'typed_blobs', (TType.STRING,None,TType.STRUCT,(TypedBlob, TypedBlob.thrift_spec)), {
    }, ), # 2
  )

  def __init__(self, collection_type=None, typed_blobs=thrift_spec[2][4],):
    self.collection_type = collection_type
    if typed_blobs is self.thrift_spec[2][4]:
      typed_blobs = {
    }
    self.typed_blobs = typed_blobs

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.collection_type = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.MAP:
          self.typed_blobs = {}
          (_ktype10, _vtype11, _size9 ) = iprot.readMapBegin() 
          for _i13 in xrange(_size9):
            _key14 = iprot.readString();
            _val15 = TypedBlob()
            _val15.read(iprot)
            self.typed_blobs[_key14] = _val15
          iprot.readMapEnd()
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('BlobCollection')
    if self.collection_type is not None:
      oprot.writeFieldBegin('collection_type', TType.STRING, 1)
      oprot.writeString(self.collection_type)
      oprot.writeFieldEnd()
    if self.typed_blobs is not None:
      oprot.writeFieldBegin('typed_blobs', TType.MAP, 2)
      oprot.writeMapBegin(TType.STRING, TType.STRUCT, len(self.typed_blobs))
      for kiter16,viter17 in self.typed_blobs.items():
        oprot.writeString(kiter16)
        viter17.write(oprot)
      oprot.writeMapEnd()
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, getattr(self, key))
      for key in self.__slots__]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    for attr in self.__slots__:
      my_val = getattr(self, attr)
      other_val = getattr(other, attr)
      if my_val != other_val:
        return False
    return True

  def __ne__(self, other):
    return not (self == other)

