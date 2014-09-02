"""
Allows for ctypes derived classes, such as Structure and Bitfield, to be
accessed over a remote interface, such as TCP/IP or a VME indirection
scheme.  Effectively, this means turning requests for elements of the
structure into requests for arbitrary byte sequences, fetching them,
and managing the translation.

Protocol Handlers
-----------------

The protocol handler is responsible for transporting arbitrary data.
It is defined by having writeBytes and readBytes methods.

If, for instance, you had a mechanism whereby, over an Ethernet
socket, you could write 8 bytes to address 0x100 as 
``W 0x100 55 45 10 18 26 28 33 47``, then read back four of those
bytes by sending ``R 0x100 4`` and getting back ``55 45 10 18`` (all
of that newline delimited), then your protocol handler would look like so::

    class SerialHandler(object):
        def __init__(self, sock):
            self.sock = sock
            
        def writeBytes(self, addr, data):
            msg = "W " + hex(addr) + ' '.join(str(d) for d in data)
            self.sock.sendall(msg.encode('ascii'))
            
        def readBytes(self, addr, size):
            msg = "R 0x{0:X} {1}".format(addr, size)
            self.sock.sendall(msg.encode('ascii'))
             
            received = []
            while True:
                x = self.sock.recv(4096)
                received.append(x)
                if b'\n' in x:
                    break
                    
            msg = b''.join(received)
            data = bytes(int(b) for b in msg.split(b' '))
            return data

Note that the protocol handler doesn't care about the underlying data
representation; these bytes could be parts of strings, floats, or integers.

The binary data for the readBytes and writeBytes methods is not required to
be mutable; either bytes() or bytearray() data may be provided.

Remote Classes
--------------

Underneath the hood are three very similar classes, the RemoteStruct,
RemoteArray, and RemoteBitfield.  These classes can be called out
directly, or the Remote function (which pretends to be a class initializer)
will create whichever is appropriate.

Whether you instantiate a class, or let the Remote function do it, the
initialization convention will be the same::

    Remote(basis, handler)
    RemoteStruct(basis, handler)
    RemoteArray(basis, handler)
    RemoteBitfield(basis, handler)
    
Where basis is the underlying structure to map (a class, not a instance),
and handler is the protocol handler to use.

The constructors handle nested structure definitions appropriately.  So,
to take the following set of code::

    BF_FLAGS = make_bf('BF_FLAGS', fields = [
            ('en0', c_uint, 1),
            ('_dummy1', c_uint, 3),
            ('en1', c_uint, 1),
            ('_dummy5', c_uint, 3),
            ('val', c_uint, 8),
            ('_dummy16', c_uint, 16)
        ],
        basetype = c_uint32
    ) 

    class SubStructure(Structure):
        _fields_ = [
            ('flags', BF_FLAGS),
            ('_dummy1', c_uint32),
            ('offset', c_int32),
            ('slope', c_float)
        ]

    class FakeCalTable(Structure):
        _fields_ = [
            ('serial', c_uint32),
            ('dash', c_uint32),
            ('_dummy2', c_uint32*2),
            ('chans', SubStructure * 16),
            ('checksum', c_uint32)
        ]
        
    target = Remote(FakeCalTable, handler)
    
The structure built will be::

    target                      RemoteStruct
        .serial                 <data>
        .dash                   <data>
        .chans                  RemoteArray
            [0]                 RemoteStruct
                .flags          RemoteBitfield
                    .en0        <data>
                    .en1        <data>
                    .val        <data>
                .offset         <data>
                .slope          <data>
            [1]                 RemoteStruct
                .flags          RemoteBitfield
                ...

:author: Rob Gaddi, Highland Technology
:date:   03-Jun-2014

"""

from bitfield import *

#######################################################################
# Dealing with the different Python versions takes a little bit
# of cleverness.
#######################################################################

class _NullDecorator(object):
	def __init__(self, *args, **kwargs):
		pass
		
	def __call__(self, fn):
		return fn

try:
    from functools import lru_cache
except ImportError:
    # lru_cache not available in this version of Python.  The performance
    # enhancement is nice, but not essential.
    lru_cache = _NullDecorator

if bytes is str:
	byte_converter = bytearray
else:
	byte_converter = bytes

# We need to reverse engineer base types out of the ctypes library
structure_basetype = type(Structure)
simple_basetype = c_uint.__bases__[0]

class _SubHandler(object):
    """
    A passthrough handler that applies an offset
    on top of another higher-level handler.
    """
    
    def __init__(self, handler, offset):
        # Optimize for nested _SubHandlers by not bouncing
        # through a zillion function calls if we can figure
        # out how not to.
        #
        try:
            if isinstance(handler, self.__class__):
                self.handler = handler.handler
                self.offset = handler.offset + offset
                return
                
        except AttributeError:
            pass
            
        self.handler = handler
        self.offset = offset
        
    def readBytes(self, addr, size):
        return self.handler.readBytes(addr + self.offset, size)
        
    def writeBytes(self, addr, data):
        self.handler.writeBytes(addr + self.offset, data)

class _Translator(object):
    """
    Hidden objects that underpin the RemoteStruct concept.
    
    A Translator can be made from basically anything ctypes
    derived, and exposes methods get, set, getAll, and setAll.
    
    If the basis is a simple data type then get and set cause a transaction
    to occur across the handler.  The data type accepted/returned will be
    those accepted as the value of the data type, e.g. integers for c_uint
    types.
    
    If the basis is a Bitfield datatype, then get will return a
    RemoteBitfield object.  Set will accept only a Bitfield of the underlying
    type, or a value of the type of the Bitfield's base.
    
    If the basis is a Structure or array, then get will return a RemoteStruct
    or RemoteArray, respectively.  Set will raise a ValueError.
    
    getAll and setAll will transfer bytes to and from the basis type for
    any basis type.  These methods allow the fetching of large data blocks.
    
    Translators will never be directly exposed to the outside world, they're
    a trampoline layer for the various higher level structure types.
    
    """
    
    def __init__(self, basis, handler, offset):
        self.basis = basis
        self.handler = handler
        self.offset = offset 
        self.size = sizeof(basis)
        
        if issubclass(basis, Bitfield):
            # This is a Bitfield object.
            self.remote = RemoteBitfield(basis, self.getSubHandler())
            self.get = self.getRemote
            self.set = self.setBitfield
            
        elif hasattr(basis, '_fields_'):
            # This is a Structure.  We'll only move the fields
            # of this.
            self.remote = RemoteStruct(basis, self.getSubHandler())
            self.get = self.getRemote
            self.set = self.cantSet
            
        elif hasattr(basis, '__getitem__'):
            # This is an array.  We'll only move the elements
            # of this.
            self.remote = RemoteArray(basis, self.getSubHandler())
            self.get = self.getRemote
            self.set = self.cantSet
        
        elif hasattr(basis, 'value'):
            # This is simple data.  We want to get/set it directly.
            self.get = self.getSimple
            self.set = self.setSimple
            
        else:
            # This isn't something we know how to deal with.
            raise TypeError("Can't translate " + self.basis.__class__.__name__)
        
    def getSubHandler(self):
        return _SubHandler(self.handler, self.offset)
        
    def getAll(self):
        """Fetch this object from the handler."""
        b = self.handler.readBytes(self.offset, self.size)
        return self.basis.from_buffer_copy(b)
        
    def setAll(self, value):
        """Send this object through the handler."""
        self.handler.writeBytes(self.offset, byte_converter(value))
        
    #######################################################################
    # Some subset of these functions will be mapped onto get/set, based
    # on what the basis type is.
    #######################################################################
        
    def getRemote(self):
        return self.remote
        
    def setBitfield(self, value):
        if isinstance(value, self.basis):
            self.remote.base = value.base
        else:
            self.remote.base = value 
    
    def cantSet(self, value):
        raise TypeError("Can't assign to remote object of type " + self.basis.__class__.__name__)
        
    def getSimple(self):
        return self.getAll().value
        
    def setSimple(self, value):
        self.setAll(self.basis(value))

class RemoteStruct(object):
    """
    The remote implementation of a ctypes Structure or Union.
    
    The initialization syntax is::
    
        RemoteStruct(basis, handler)
        
    Where ``basis`` is a Structure or Union class (not instance).
    
    The ``handler`` is any object that has at least the two methods::
    
        readBytes(self, addr, size)
        writeBytes(self, addr, data)
        
    ``readBytes`` returns a bytearray of length size.  ``writeBytes``
    accepts anything that supports the buffer protocol (bytes, bytearray,
    ctypes derived classes, etc).
    
    """
    
    def __init__(self, basis, handler):
        super(RemoteStruct, self).__setattr__('_basis', basis)
        super(RemoteStruct, self).__setattr__('_fields_', basis._fields_)
        super(RemoteStruct, self).__setattr__('_handler', handler)
        
        # Somehow, the Structure doesn't allow us to easily
        # query the types of each of its elements.  Instead,
        # we'll build up a dict to hit things quickly by
        # name.
        fields = {}
        for f in basis._fields_:
            key = f[0]
            cls = f[1]
            if len(f) > 2:
                raise ValueError(
                    "RemoteStruct doesn't support basic Structure bitfields, as "
                    "their implementation is a bit dodgy.  Please use the Bitfield "
                    "class instead to implement bit fields."
                )
            field = getattr(basis, key)
            trans = _Translator(cls, handler, field.offset)
            fields[key] = trans
            
        super(RemoteStruct, self).__setattr__('_fields', fields)
        
    def __getattr__(self, key):
        try:
            return self._fields[key].get()
        except KeyError as e:
            raise AttributeError("No field named " + key)
            
    def __setattr__(self, key, value):
        try:
            self._fields[key].set(value)
        except KeyError as e:
            raise AttributeError("No field named " + key)

    def __dir__(self):
        """
        For Python 3.2 compatibility, must return a list rather than
        an iterable.
        """
        return list(dir(self.__class__)) + [x[0] for x in self._fields_ if not x[0].startswith('_')]

class RemoteArray(object):
    """
    The remote implementation of a ctypes array.
    
    The initialization syntax is::
    
        RemoteStruct(basis, handler)
        
    Where ``basis`` is any array of ctypes classes such as a c_uint * 8.
    """
    
    def __init__(self, basis, handler):
        self._basis = basis
        self._handler = handler
        
        self._basetype = basetype = basis._type_
        self._elementsize = sizeof(basetype)
        self._count = sizeof(basis) // sizeof(basetype)
        
    @lru_cache(maxsize = 64)
    def _getTranslator(self, idx):
        """
        We'll create the translators dynamically as needed for
        this class.  This is probably woefully inefficient, but
        we'll try to fix that later.
        """
        if idx >= self._count:
            raise IndexError('Index {0} be less than {1}'.format(idx, self._count))
        offset = self._elementsize * idx
        return _Translator(self._basetype, self._handler, offset)
        
    def _idx_translator(self, idx):
        """
        Return an iterator over the translators for the
        appropriate indices, whether idx is a positive
        int, negative int, or slice.
        """
        try:
            start, stop, step = idx.indices(len(self))
            return (self._getTranslator(n) for n in range(start, stop, step))
        except AttributeError:
            # If this is negative, flip it.
            if idx < 0:
                idx = len(self) - idx
            return [self._getTranslator(idx)]
            
    def __getitem__(self, idx):
        """
        Return a single value for a single index, or a list for a
        slice index.  Negative indices are dealt with in the usual
        Pythonic way.
        """
        results = [t.get() for t in self._idx_translator(idx)]
        if len(results) == 1:
            return results[0]
        else:
            return results
            
    def __setitem__(self, idx, value):
        """
        Set a single value for a single index, or a list for a
        slice index.  Negative indices are dealt with in the usual
        Pythonic way.
        """
        try:
            valiter = iter(value)
        except TypeError:
            valiter = [value]
            
        for t, v in zip(self._idx_translator(idx), valiter):
            t.set(v)
    
    def __len__(self):
        return self._count
        
class RemoteBitfield(object):
    def __init__(self, basis, handler):
        super(RemoteBitfield, self).__setattr__('_basis', basis)
        super(RemoteBitfield, self).__setattr__('_size', sizeof(basis))
        super(RemoteBitfield, self).__setattr__('_handler', handler)
        super(RemoteBitfield, self).__setattr__('_underlying', basis())
        
    def _update_underlying(self):
        new_basis = self._basis.from_buffer_copy(self._handler.readBytes(0, self._size))
        super(RemoteBitfield, self).__setattr__('_underlying', new_basis)
        
    def _transmit_underlying(self):
        self._handler.writeBytes(0, byte_converter(self._underlying))
        
    def __getattr__(self, key):
        self._update_underlying()
        return getattr(self._underlying, key)
        
    def __setattr__(self, key, value):
        """Set one field."""
        
        if key == 'base':
            # This one is a special case, it's the mechanism with which
            # we'll trigger writes back throught the handler
            self._underlying.base = value
            self._transmit_underlying()
            
        else:
            # Any other fields will piggyback the update mechanism.
            self.update( [(key, value)] )

    def __iter__(self):
        """Return an iterator over the field names."""
        return iter(self._underlying)
        
    def keys(self):
        """Return a list of the field names."""
        return list(iter(self))

    def __dir__(self):
        """
        For Python 3.2 compatibility, must return a list rather than
        an iterable.
        """
        return list(dir(self.__class__)) + list(self.keys())

    def clone(self):
        """Return a new bitfield with the same value.
        
        The returned value is a copy, and so is no longer linked to the
        original bitfield.  This is important when the original is located
        at anything other than normal memory, with accesses to it either
        slow or having side effects.  Creating a clone, and working
        against that clone, means that only one read will occur.
        
        """
        self._update_underlying()
        return self._underlying.clone()
        
    def items(self):
        """
        Returns an iterator over the named bitfields in the structure as
        2-tuples of (key, value).  Uses a clone so as to only read from
        the underlying data once.
        
        """
        temp = self.clone()
        return ((f, getattr(temp, f)) for f in iter(self))
        
    def update(self, E=None, **F):
        '''
        D.update([E, ]**F) -> None
        Update the bitfield from dict/iterable E and F.
        If E present and has a .keys() method, does:   for k in E: D.k = E[k]
        If E present and lacks .keys() method, does:   for (k, v) in E: D.k = v
        In either case, this is followed by:           for k in F: D.k = F[k]
        
        The entire update is applied in a single read and a single write, 
        in case the target is a memory-mapped register.  The read and write
        are independent, rather than an atomic RMW cycle.
        
        '''
        
        self._update_underlying()
        temp = self._underlying
        
        if E:
            try:
                for k in E.keys():
                    setattr(temp, k, E[k])
            except (AttributeError, ValueError):
                for k, v in E:
                    setattr(temp, k, v)
                    
        for k, v in F.items():
            setattr(temp, k, v)
            
        self._transmit_underlying()

def Remote(basis, handler):
    """
    Return the appropriate type of RemoteX to support the
    basis, be it a RemoteStruct, RemoteArray, RemoteBitfield,
    etc.
    """
    try:
        trans = _Translator(basis, handler, 0)
        return trans.remote 
    except (TypeError, AttributeError):
        raise TypeError("Can't make a remote object from " + repr(basis))

class FakeHandler(object):
	"""
	A simulated remote handler for code testing.  The handler must
	be initialized with an actual object of the same type as the
	RemoteStruct will be, or at least a buffer of the same size.
	
	The underlying object can be accessed through the ``target``
	data member.
	
	As a protocol handler for a RemoteStruct, it also support the 
	writeBytes and readBytes methods.
	
	For diagnostic purposes, the FakeHandler also provides
	the reads, writes, bytesRead, and bytesWritten data
	members.
	"""
	
	def __init__(self, target):
		self.target = target
		byte_overlay = c_uint8 * sizeof(self.target)
		self._view = byte_overlay.from_buffer(self.target)
		
		self.reads = 0
		self.writes = 0
		self.bytesRead = 0
		self.bytesWritten = 0
		
	def writeBytes(self, addr, data):
		end = addr + len(data)
		self._view[addr:end] = data
		
		self.writes += 1
		self.bytesWritten += len(data)
		
	def readBytes(self, addr, size):
		self.reads += 1
		self.bytesRead += size
		
		end = addr + size
		return bytearray(self._view[addr:end])
