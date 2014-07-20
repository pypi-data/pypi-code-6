"""
tnetstring:  data serialization using typed netstrings
======================================================

This is a data serialization library. It's a lot like JSON but it uses a
new syntax called "typed netstrings" that Zed has proposed for use in the
Mongrel2 webserver.  It's designed to be simpler and easier to implement
than JSON, with a happy consequence of also being faster in many cases.

An ordinary netstring is a blob of data prefixed with its length and postfixed
with a sanity-checking comma.  The string "hello world" encodes like this::

    11:hello world,

Typed netstrings add other datatypes by replacing the comma with a type tag.
Here's the integer 12345 encoded as a tnetstring::

    5:12345#

And here's the list [12345,True,0] which mixes integers and bools::

    19:5:12345#4:true!1:0#]

Simple enough?  This module gives you the following functions:

    :dump:    dump an object as a tnetstring to a file
    :dumps:   dump an object as a tnetstring to a string
    :load:    load a tnetstring-encoded object from a file
    :loads:   load a tnetstring-encoded object from a string
    :pop:     pop a tnetstring-encoded object from the front of a string

Note that since parsing a tnetstring requires reading all the data into memory
at once, there's no efficiency gain from using the file-based versions of these
functions.  They're only here so you can use load() to read precisely one
item from a file or socket without consuming any extra data.

The tnetstrings specification explicitly states that strings are binary blobs
and forbids the use of unicode at the protocol level.  As a convenience to
python programmers, this library lets you specify an application-level encoding
to translate python's unicode strings to and from binary blobs:

    >>> print repr(tnetstring.loads("2:\\xce\\xb1,"))
    '\\xce\\xb1'
    >>> 
    >>> print repr(tnetstring.loads("2:\\xce\\xb1,", "utf8"))
    u'\\u03b1'

:copyright: (c) 2012-2013 by Ryan Kelly <ryan@rfk.id.au>.
:copyright: (c) 2014 by Carlo Pires <carlopires@gmail.com>.
:license: MIT, see LICENCE for more details.
"""

__ver_major__ = 0
__ver_minor__ = 3
__ver_patch__ = 0
__ver_sub__ = ''
__version__ = '{}.{}.{}{}'.format(__ver_major__,__ver_minor__,__ver_patch__,__ver_sub__)

#  Use the c-extension version if available
try:
    import _tnetstring
except ImportError:
    from collections import deque
    
    def dumps(value: object) -> bytes:
        """
        This function dumps a python object as a tnetstring.
        """
        #  This uses a deque to collect output fragments in reverse order,
        #  then joins them together at the end.  It's measurably faster
        #  than creating all the intermediate strings.
        #  If you're reading this to get a handle on the tnetstring format,
        #  consider the _gdumps() function instead; it's a standard top-down
        #  generator that's simpler to understand but much less efficient.
        q = deque()
        _rdumpq(q, 0, value)
        return b''.join(q)
    
    def dump(value: object, file_handle: 'file object') -> bytes:
        """
        This function dumps a python object as a tnetstring and 
        writes it to the given file.
        """
        file_handle.write(dumps(value))
    
    def _rdumpq(q: deque, size: int, value: object) -> None:
        """
        Dump value as a tnetstring, to a deque instance, last chunks first.
    
        This function generates the tnetstring representation of the given value,
        pushing chunks of the output onto the given deque instance.  It pushes
        the last chunk first, then recursively generates more chunks.
    
        When passed in the current size of the string in the queue, it will return
        the new size of the string in the queue.
    
        Operating last-chunk-first makes it easy to calculate the size written
        for recursive structures without having to build their representation as
        a string.  This is measurably faster than generating the intermediate
        strings, especially on deeply nested structures.
        """
        write = q.appendleft
        if value is None:
            write(b'0:~')
            return size + 3
        elif value is True:
            write(b'4:true!')
            return size + 7
        elif value is False:
            write(b'5:false!')
            return size + 8
        elif isinstance(value, int):
            data = str(value).encode()
            ldata = len(data)
            span = str(ldata).encode()
            write(b'#')
            write(data)
            write(b':')
            write(span)
            return size + 2 + len(span) + ldata
        elif isinstance(value, float):
            #  Use repr() for float rather than str().
            #  It round-trips more accurately.
            #  Probably unnecessary in later python versions that
            #  use David Gay's ftoa routines.
            data = repr(value).encode()
            ldata = len(data)
            span = str(ldata).encode()
            write(b'^')
            write(data)
            write(b':')
            write(span)
            return size + 2 + len(span) + ldata
        elif isinstance(value, bytes):
            lvalue = len(value)
            span = str(lvalue).encode()
            write(b',')
            write(value)
            write(b':')
            write(span)
            return size + 2 + len(span) + lvalue
        elif isinstance(value, (list,tuple)):
            write(b']')
            init_size = size = size + 1
            for item in reversed(value):
                size = _rdumpq(q, size, item)
            span = str(size - init_size).encode()
            write(b':')
            write(span)
            return size + 1 + len(span)
        elif isinstance(value, dict):
            write(b'}')
            init_size = size = size + 1
            for (k,v) in value.items():
                size = _rdumpq(q,size,v)
                size = _rdumpq(q,size,k)
            span = str(size - init_size).encode()
            write(b':')
            write(span)
            return size + 1 + len(span)
        else:
            raise ValueError("unserializable object: {} ({})".format(value, type(value)))
    
    
    def _gdumps(value: object) -> bytes:
        """
        Generate fragments of value dumped as a tnetstring.
    
        This is the naive dumping algorithm, implemented as a generator so that
        it's easy to pass to "".join() without building a new list.
    
        This is mainly here for comparison purposes; the _rdumpq version is
        measurably faster as it doesn't have to build intermediate strins.
        """
        if value is None:
            yield b'0:~'
        elif value is True:
            yield b'4:true!'
        elif value is False:
            yield b'5:false!'
        elif isinstance(value, int):
            data = str(value).encode()
            yield str(len(data)).encode()
            yield b':'
            yield data
            yield b'#'
        elif isinstance(value, float):
            data = repr(value).encode() 
            yield str(len(data)).encode()
            yield b':'
            yield data
            yield b'^'
        elif isinstance(value, bytes):
            yield str(len(value)).encode()
            yield b':'
            yield value
            yield b','
        elif isinstance(value, (list,tuple)):
            sub = []
            for item in value:
                sub.extend(_gdumps(item))
            sub = b''.join(sub)
            yield str(len(sub)).encode()
            yield b':'
            yield sub
            yield b']'
        elif isinstance(value,(dict,)):
            sub = []
            for (k,v) in value.items():
                sub.extend(_gdumps(k))
                sub.extend(_gdumps(v))
            sub = b''.join(sub)
            yield str(len(sub)).encode()
            yield b':'
            yield sub
            yield b'}'
        else:
            raise ValueError("unserializable object")
    
    def loads(string: bytes) -> object:
        """
        This function parses a tnetstring into a python object.
        """
        #  No point duplicating effort here.  In the C-extension version,
        #  loads() is measurably faster then pop() since it can avoid
        #  the overhead of building a second string.
        return pop(string)[0]
    
    def load(file_handle: 'file object') -> object:
        """load(file) -> object
    
        This function reads a tnetstring from a file and parses it into a
        python object.  The file must support the read() method, and this
        function promises not to read more data than necessary.
        """
        #  Read the length prefix one char at a time.
        #  Note that the netstring spec explicitly forbids padding zeros.
        c = file_handle.read(1)
        if not ord(b'0') <= ord(c) <= ord(b'9'):
            raise ValueError("not a tnetstring: missing or invalid length prefix")
        datalen = ord(c) - ord('0')
        c = file_handle.read(1)
        if datalen != 0:
            while ord(b'0') <= ord(c) <= ord(b'9'):
                datalen = (10 * datalen) + (ord(c) - ord('0'))
                if datalen > 999999999:
                    errmsg = "not a tnetstring: absurdly large length prefix"
                    raise ValueError(errmsg)
                c = file_handle.read(1)
        if ord(c) != ord(b':'):
            raise ValueError("not a tnetstring: missing or invalid length prefix")
        #  Now we can read and parse the payload.
        #  This repeats the dispatch logic of pop() so we can avoid
        #  re-constructing the outermost tnetstring.
        data = file_handle.read(datalen)
        if len(data) != datalen:
            raise ValueError("not a tnetstring: length prefix too big")
        tns_type = ord(file_handle.read(1))
        if tns_type == ord(b','):
            return data
        if tns_type == ord(b'#'):
            try:
                return int(data)
            except ValueError:
                raise ValueError("not a tnetstring: invalid integer literal")
        if tns_type == ord(b'^'):
            try:
                return float(data)
            except ValueError:
                raise ValueError("not a tnetstring: invalid float literal")
        if tns_type == ord(b'!'):
            if data == b'true':
                return True
            elif data == b'false':
                return False
            else:
                raise ValueError("not a tnetstring: invalid boolean literal")
        if tns_type == ord(b'~'):
            if data:
                raise ValueError("not a tnetstring: invalid null literal")
            return None
        if tns_type == ord(b']'):
            l = []
            while data:
                item, data = pop(data)
                l.append(item)
            return l
        if tns_type == ord(b'}'):
            d = {}
            while data:
                key, data = pop(data)
                val, data = pop(data)
                d[key] = val
            return d
        raise ValueError("unknown type tag")
        
    def pop(string: bytes) -> object:
        """pop(string,encoding='utf_8') -> (object, remain)
    
        This function parses a tnetstring into a python object.
        It returns a tuple giving the parsed object and a string
        containing any unparsed data from the end of the string.
        """
        #  Parse out data length, type and remaining string.
        try:
            dlen, rest = string.split(b':', 1)
            dlen = int(dlen)
        except ValueError:
            raise ValueError("not a tnetstring: missing or invalid length prefix: {}".format(string))
        try:
            data, tns_type, remain = rest[:dlen], rest[dlen], rest[dlen+1:]
        except IndexError:
            #  This fires if len(rest) < dlen, meaning we don't need
            #  to further validate that data is the right length.
            raise ValueError("not a tnetstring: invalid length prefix: {}".format(dlen))
        #  Parse the data based on the type tag.
        if tns_type == ord(b','):
            return data, remain
        if tns_type == ord(b'#'):
            try:
                return int(data), remain
            except ValueError:
                raise ValueError("not a tnetstring: invalid integer literal: {}".format(data))
        if tns_type == ord(b'^'):
            try:
                return float(data), remain
            except ValueError:
                raise ValueError("not a tnetstring: invalid float literal: {}".format(data))
        if tns_type == ord(b'!'):
            if data == b'true':
                return True, remain
            elif data == b'false':
                return False, remain
            else:
                raise ValueError("not a tnetstring: invalid boolean literal: {}".format(data))
        if tns_type == ord(b'~'):
            if data:
                raise ValueError("not a tnetstring: invalid null literal")
            return None, remain
        if tns_type == ord(b']'):
            l = []
            while data:
                item, data = pop(data)
                l.append(item)
            return (l,remain)
        if tns_type == ord(b'}'):
            d = {}
            while data:
                key, data = pop(data)
                val, data = pop(data)
                d[key] = val
            return d, remain
        raise ValueError("unknown type tag: {}".format(tns_type))
else:
    dumps = _tnetstring.dumps
    load = _tnetstring.load
    loads = _tnetstring.loads
    pop = _tnetstring.pop
    def dump(value: object, file_handle: 'file object') -> bytes:
        """
        This function dumps a python object as a tnetstring and 
        writes it to the given file.
        """
        file_handle.write(dumps(value))
