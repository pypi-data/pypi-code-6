'''Wrapper for vedis.h

Generated with:
ctypesgen/ctypesgen.py vedis/src/vedis.h -L ./ -l vedis -o /home/charles/tmp/scrap/z1/src/vedis/vedis/_vedis.py

Do not modify this file.
'''

__docformat__ =  'restructuredtext'

# Begin preamble

import ctypes, os, sys
from ctypes import *

_int_types = (c_int16, c_int32)
if hasattr(ctypes, 'c_int64'):
    # Some builds of ctypes apparently do not have c_int64
    # defined; it's a pretty good bet that these builds do not
    # have 64-bit pointers.
    _int_types += (c_int64,)
for t in _int_types:
    if sizeof(t) == sizeof(c_size_t):
        c_ptrdiff_t = t
del t
del _int_types

class c_void(Structure):
    # c_void_p is a buggy return type, converting to int, so
    # POINTER(None) == c_void_p is actually written as
    # POINTER(c_void), so it can be treated as a real pointer.
    _fields_ = [('dummy', c_int)]

def POINTER(obj):
    p = ctypes.POINTER(obj)

    # Convert None to a real NULL pointer to work around bugs
    # in how ctypes handles None on 64-bit platforms
    if not isinstance(p.from_param, classmethod):
        def from_param(cls, x):
            if x is None:
                return cls()
            else:
                return x
        p.from_param = classmethod(from_param)

    return p

class UserString:
    def __init__(self, seq):
        if isinstance(seq, basestring):
            self.data = seq
        elif isinstance(seq, UserString):
            self.data = seq.data[:]
        else:
            self.data = str(seq)
    def __str__(self): return str(self.data)
    def __repr__(self): return repr(self.data)
    def __int__(self): return int(self.data)
    def __long__(self): return long(self.data)
    def __float__(self): return float(self.data)
    def __complex__(self): return complex(self.data)
    def __hash__(self): return hash(self.data)

    def __cmp__(self, string):
        if isinstance(string, UserString):
            return cmp(self.data, string.data)
        else:
            return cmp(self.data, string)
    def __contains__(self, char):
        return char in self.data

    def __len__(self): return len(self.data)
    def __getitem__(self, index): return self.__class__(self.data[index])
    def __getslice__(self, start, end):
        start = max(start, 0); end = max(end, 0)
        return self.__class__(self.data[start:end])

    def __add__(self, other):
        if isinstance(other, UserString):
            return self.__class__(self.data + other.data)
        elif isinstance(other, basestring):
            return self.__class__(self.data + other)
        else:
            return self.__class__(self.data + str(other))
    def __radd__(self, other):
        if isinstance(other, basestring):
            return self.__class__(other + self.data)
        else:
            return self.__class__(str(other) + self.data)
    def __mul__(self, n):
        return self.__class__(self.data*n)
    __rmul__ = __mul__
    def __mod__(self, args):
        return self.__class__(self.data % args)

    # the following methods are defined in alphabetical order:
    def capitalize(self): return self.__class__(self.data.capitalize())
    def center(self, width, *args):
        return self.__class__(self.data.center(width, *args))
    def count(self, sub, start=0, end=sys.maxint):
        return self.data.count(sub, start, end)
    def decode(self, encoding=None, errors=None): # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.decode(encoding, errors))
            else:
                return self.__class__(self.data.decode(encoding))
        else:
            return self.__class__(self.data.decode())
    def encode(self, encoding=None, errors=None): # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.encode(encoding, errors))
            else:
                return self.__class__(self.data.encode(encoding))
        else:
            return self.__class__(self.data.encode())
    def endswith(self, suffix, start=0, end=sys.maxint):
        return self.data.endswith(suffix, start, end)
    def expandtabs(self, tabsize=8):
        return self.__class__(self.data.expandtabs(tabsize))
    def find(self, sub, start=0, end=sys.maxint):
        return self.data.find(sub, start, end)
    def index(self, sub, start=0, end=sys.maxint):
        return self.data.index(sub, start, end)
    def isalpha(self): return self.data.isalpha()
    def isalnum(self): return self.data.isalnum()
    def isdecimal(self): return self.data.isdecimal()
    def isdigit(self): return self.data.isdigit()
    def islower(self): return self.data.islower()
    def isnumeric(self): return self.data.isnumeric()
    def isspace(self): return self.data.isspace()
    def istitle(self): return self.data.istitle()
    def isupper(self): return self.data.isupper()
    def join(self, seq): return self.data.join(seq)
    def ljust(self, width, *args):
        return self.__class__(self.data.ljust(width, *args))
    def lower(self): return self.__class__(self.data.lower())
    def lstrip(self, chars=None): return self.__class__(self.data.lstrip(chars))
    def partition(self, sep):
        return self.data.partition(sep)
    def replace(self, old, new, maxsplit=-1):
        return self.__class__(self.data.replace(old, new, maxsplit))
    def rfind(self, sub, start=0, end=sys.maxint):
        return self.data.rfind(sub, start, end)
    def rindex(self, sub, start=0, end=sys.maxint):
        return self.data.rindex(sub, start, end)
    def rjust(self, width, *args):
        return self.__class__(self.data.rjust(width, *args))
    def rpartition(self, sep):
        return self.data.rpartition(sep)
    def rstrip(self, chars=None): return self.__class__(self.data.rstrip(chars))
    def split(self, sep=None, maxsplit=-1):
        return self.data.split(sep, maxsplit)
    def rsplit(self, sep=None, maxsplit=-1):
        return self.data.rsplit(sep, maxsplit)
    def splitlines(self, keepends=0): return self.data.splitlines(keepends)
    def startswith(self, prefix, start=0, end=sys.maxint):
        return self.data.startswith(prefix, start, end)
    def strip(self, chars=None): return self.__class__(self.data.strip(chars))
    def swapcase(self): return self.__class__(self.data.swapcase())
    def title(self): return self.__class__(self.data.title())
    def translate(self, *args):
        return self.__class__(self.data.translate(*args))
    def upper(self): return self.__class__(self.data.upper())
    def zfill(self, width): return self.__class__(self.data.zfill(width))

class MutableString(UserString):
    """mutable string objects

    Python strings are immutable objects.  This has the advantage, that
    strings may be used as dictionary keys.  If this property isn't needed
    and you insist on changing string values in place instead, you may cheat
    and use MutableString.

    But the purpose of this class is an educational one: to prevent
    people from inventing their own mutable string class derived
    from UserString and than forget thereby to remove (override) the
    __hash__ method inherited from UserString.  This would lead to
    errors that would be very hard to track down.

    A faster and better solution is to rewrite your program using lists."""
    def __init__(self, string=""):
        self.data = string
    def __hash__(self):
        raise TypeError("unhashable type (it is mutable)")
    def __setitem__(self, index, sub):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data): raise IndexError
        self.data = self.data[:index] + sub + self.data[index+1:]
    def __delitem__(self, index):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data): raise IndexError
        self.data = self.data[:index] + self.data[index+1:]
    def __setslice__(self, start, end, sub):
        start = max(start, 0); end = max(end, 0)
        if isinstance(sub, UserString):
            self.data = self.data[:start]+sub.data+self.data[end:]
        elif isinstance(sub, basestring):
            self.data = self.data[:start]+sub+self.data[end:]
        else:
            self.data =  self.data[:start]+str(sub)+self.data[end:]
    def __delslice__(self, start, end):
        start = max(start, 0); end = max(end, 0)
        self.data = self.data[:start] + self.data[end:]
    def immutable(self):
        return UserString(self.data)
    def __iadd__(self, other):
        if isinstance(other, UserString):
            self.data += other.data
        elif isinstance(other, basestring):
            self.data += other
        else:
            self.data += str(other)
        return self
    def __imul__(self, n):
        self.data *= n
        return self

class String(MutableString, Union):

    _fields_ = [('raw', POINTER(c_char)),
                ('data', c_char_p)]

    def __init__(self, obj=""):
        if isinstance(obj, (str, unicode, UserString)):
            self.data = str(obj)
        else:
            self.raw = obj

    def __len__(self):
        return self.data and len(self.data) or 0

    def from_param(cls, obj):
        # Convert None or 0
        if obj is None or obj == 0:
            return cls(POINTER(c_char)())

        # Convert from String
        elif isinstance(obj, String):
            return obj

        # Convert from str
        elif isinstance(obj, str):
            return cls(obj)

        # Convert from c_char_p
        elif isinstance(obj, c_char_p):
            return obj

        # Convert from POINTER(c_char)
        elif isinstance(obj, POINTER(c_char)):
            return obj

        # Convert from raw pointer
        elif isinstance(obj, int):
            return cls(cast(obj, POINTER(c_char)))

        # Convert from object
        else:
            return String.from_param(obj._as_parameter_)
    from_param = classmethod(from_param)

def ReturnString(obj, func=None, arguments=None):
    return String.from_param(obj)

# As of ctypes 1.0, ctypes does not support custom error-checking
# functions on callbacks, nor does it support custom datatypes on
# callbacks, so we must ensure that all callbacks return
# primitive datatypes.
#
# Non-primitive return values wrapped with UNCHECKED won't be
# typechecked, and will be converted to c_void_p.
def UNCHECKED(type):
    if (hasattr(type, "_type_") and isinstance(type._type_, str)
        and type._type_ != "P"):
        return type
    else:
        return c_void_p

# ctypes doesn't have direct support for variadic functions, so we have to write
# our own wrapper class
class _variadic_function(object):
    def __init__(self,func,restype,argtypes):
        self.func=func
        self.func.restype=restype
        self.argtypes=argtypes
    def _as_parameter_(self):
        # So we can pass this variadic function as a function pointer
        return self.func
    def __call__(self,*args):
        fixed_args=[]
        i=0
        for argtype in self.argtypes:
            # Typecheck what we can
            fixed_args.append(argtype.from_param(args[i]))
            i+=1
        return self.func(*fixed_args+list(args[i:]))

# End preamble

_libs = {}
_libdirs = ['./']

# Begin loader

# ----------------------------------------------------------------------------
# Copyright (c) 2008 David James
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

import os.path, re, sys, glob
import ctypes
import ctypes.util

def _environ_path(name):
    if name in os.environ:
        return os.environ[name].split(":")
    else:
        return []

class LibraryLoader(object):
    def __init__(self):
        self.other_dirs=[]

    def load_library(self,libname):
        """Given the name of a library, load it."""
        paths = self.getpaths(libname)

        for path in paths:
            if os.path.exists(path):
                return self.load(path)

        raise ImportError("%s not found." % libname)

    def load(self,path):
        """Given a path to a library, load it."""
        try:
            # Darwin requires dlopen to be called with mode RTLD_GLOBAL instead
            # of the default RTLD_LOCAL.  Without this, you end up with
            # libraries not being loadable, resulting in "Symbol not found"
            # errors
            if sys.platform == 'darwin':
                return ctypes.CDLL(path, ctypes.RTLD_GLOBAL)
            else:
                return ctypes.cdll.LoadLibrary(path)
        except OSError,e:
            raise ImportError(e)

    def getpaths(self,libname):
        """Return a list of paths where the library might be found."""
        if os.path.isabs(libname):
            yield libname

        else:
            for path in self.getplatformpaths(libname):
                yield path

            path = ctypes.util.find_library(libname)
            if path: yield path

    def getplatformpaths(self, libname):
        return []

# Darwin (Mac OS X)

class DarwinLibraryLoader(LibraryLoader):
    name_formats = ["lib%s.dylib", "lib%s.so", "lib%s.bundle", "%s.dylib",
                "%s.so", "%s.bundle", "%s"]

    def getplatformpaths(self,libname):
        if os.path.pathsep in libname:
            names = [libname]
        else:
            names = [format % libname for format in self.name_formats]

        for dir in self.getdirs(libname):
            for name in names:
                yield os.path.join(dir,name)

    def getdirs(self,libname):
        '''Implements the dylib search as specified in Apple documentation:

        http://developer.apple.com/documentation/DeveloperTools/Conceptual/
            DynamicLibraries/Articles/DynamicLibraryUsageGuidelines.html

        Before commencing the standard search, the method first checks
        the bundle's ``Frameworks`` directory if the application is running
        within a bundle (OS X .app).
        '''

        dyld_fallback_library_path = _environ_path("DYLD_FALLBACK_LIBRARY_PATH")
        if not dyld_fallback_library_path:
            dyld_fallback_library_path = [os.path.expanduser('~/lib'),
                                          '/usr/local/lib', '/usr/lib']

        dirs = []

        if '/' in libname:
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))
        else:
            dirs.extend(_environ_path("LD_LIBRARY_PATH"))
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))

        dirs.extend(self.other_dirs)
        dirs.append(".")

        if hasattr(sys, 'frozen') and sys.frozen == 'macosx_app':
            dirs.append(os.path.join(
                os.environ['RESOURCEPATH'],
                '..',
                'Frameworks'))

        dirs.extend(dyld_fallback_library_path)

        return dirs

# Posix

class PosixLibraryLoader(LibraryLoader):
    _ld_so_cache = None

    def _create_ld_so_cache(self):
        # Recreate search path followed by ld.so.  This is going to be
        # slow to build, and incorrect (ld.so uses ld.so.cache, which may
        # not be up-to-date).  Used only as fallback for distros without
        # /sbin/ldconfig.
        #
        # We assume the DT_RPATH and DT_RUNPATH binary sections are omitted.

        directories = []
        for name in ("LD_LIBRARY_PATH",
                     "SHLIB_PATH", # HPUX
                     "LIBPATH", # OS/2, AIX
                     "LIBRARY_PATH", # BE/OS
                    ):
            if name in os.environ:
                directories.extend(os.environ[name].split(os.pathsep))
        directories.extend(self.other_dirs)
        directories.append(".")

        try: directories.extend([dir.strip() for dir in open('/etc/ld.so.conf')])
        except IOError: pass

        directories.extend(['/lib', '/usr/lib', '/lib64', '/usr/lib64'])

        cache = {}
        lib_re = re.compile(r'lib(.*)\.s[ol]')
        ext_re = re.compile(r'\.s[ol]$')
        for dir in directories:
            try:
                for path in glob.glob("%s/*.s[ol]*" % dir):
                    file = os.path.basename(path)

                    # Index by filename
                    if file not in cache:
                        cache[file] = path

                    # Index by library name
                    match = lib_re.match(file)
                    if match:
                        library = match.group(1)
                        if library not in cache:
                            cache[library] = path
            except OSError:
                pass

        self._ld_so_cache = cache

    def getplatformpaths(self, libname):
        if self._ld_so_cache is None:
            self._create_ld_so_cache()

        result = self._ld_so_cache.get(libname)
        if result: yield result

        path = ctypes.util.find_library(libname)
        if path: yield os.path.join("/lib",path)

# Windows

class _WindowsLibrary(object):
    def __init__(self, path):
        self.cdll = ctypes.cdll.LoadLibrary(path)
        self.windll = ctypes.windll.LoadLibrary(path)

    def __getattr__(self, name):
        try: return getattr(self.cdll,name)
        except AttributeError:
            try: return getattr(self.windll,name)
            except AttributeError:
                raise

class WindowsLibraryLoader(LibraryLoader):
    name_formats = ["%s.dll", "lib%s.dll", "%slib.dll"]

    def load_library(self, libname):
        try:
            result = LibraryLoader.load_library(self, libname)
        except ImportError:
            result = None
            if os.path.sep not in libname:
                for name in self.name_formats:
                    try:
                        result = getattr(ctypes.cdll, name % libname)
                        if result:
                            break
                    except WindowsError:
                        result = None
            if result is None:
                try:
                    result = getattr(ctypes.cdll, libname)
                except WindowsError:
                    result = None
            if result is None:
                raise ImportError("%s not found." % libname)
        return result

    def load(self, path):
        return _WindowsLibrary(path)

    def getplatformpaths(self, libname):
        if os.path.sep not in libname:
            for name in self.name_formats:
                dll_in_current_dir = os.path.abspath(name % libname)
                if os.path.exists(dll_in_current_dir):
                    yield dll_in_current_dir
                path = ctypes.util.find_library(name % libname)
                if path:
                    yield path

# Platform switching

# If your value of sys.platform does not appear in this dict, please contact
# the Ctypesgen maintainers.

loaderclass = {
    "darwin":   DarwinLibraryLoader,
    "cygwin":   WindowsLibraryLoader,
    "win32":    WindowsLibraryLoader
}

loader = loaderclass.get(sys.platform, PosixLibraryLoader)()

def add_library_search_dirs(other_dirs):
    loader.other_dirs = other_dirs

load_library = loader.load_library

del loaderclass

# End loader

add_library_search_dirs([os.path.realpath(os.path.dirname(__file__))])

# Begin libraries

_libs["vedis"] = load_library("vedis")

# 1 libraries
# End libraries

# No modules

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 498
class struct_vedis_io_methods(Structure):
    pass

vedis_io_methods = struct_vedis_io_methods # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 101

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 679
class struct_vedis_kv_methods(Structure):
    pass

vedis_kv_methods = struct_vedis_kv_methods # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 102

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 666
class struct_vedis_kv_engine(Structure):
    pass

vedis_kv_engine = struct_vedis_kv_engine # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 103

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 104
class struct_vedis_context(Structure):
    pass

vedis_context = struct_vedis_context # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 104

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 105
class struct_vedis_value(Structure):
    pass

vedis_value = struct_vedis_value # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 105

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 543
class struct_vedis_vfs(Structure):
    pass

vedis_vfs = struct_vedis_vfs # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 106

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 107
class struct_vedis(Structure):
    pass

vedis = struct_vedis # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 107

sxi64 = c_longlong # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 170

sxu64 = c_ulonglong # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 171

ProcConsumer = CFUNCTYPE(UNCHECKED(c_int), POINTER(None), c_uint, POINTER(None)) # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 174

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 256
class struct_SyMutexMethods(Structure):
    pass

SyMutexMethods = struct_SyMutexMethods # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 176

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 243
class struct_SyMemMethods(Structure):
    pass

SyMemMethods = struct_SyMemMethods # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 177

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 194
class struct_SyString(Structure):
    pass

SyString = struct_SyString # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 178

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 183
class struct_syiovec(Structure):
    pass

syiovec = struct_syiovec # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 179

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 180
class struct_SyMutex(Structure):
    pass

SyMutex = struct_SyMutex # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 180

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 200
class struct_Sytm(Structure):
    pass

Sytm = struct_Sytm # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 181

struct_syiovec.__slots__ = [
    'pBase',
    'nLen',
]
struct_syiovec._fields_ = [
    ('pBase', POINTER(None)),
    ('nLen', c_ulong),
]

struct_SyString.__slots__ = [
    'zString',
    'nByte',
]
struct_SyString._fields_ = [
    ('zString', String),
    ('nByte', c_uint),
]

struct_Sytm.__slots__ = [
    'tm_sec',
    'tm_min',
    'tm_hour',
    'tm_mday',
    'tm_mon',
    'tm_year',
    'tm_wday',
    'tm_yday',
    'tm_isdst',
    'tm_zone',
    'tm_gmtoff',
]
struct_Sytm._fields_ = [
    ('tm_sec', c_int),
    ('tm_min', c_int),
    ('tm_hour', c_int),
    ('tm_mday', c_int),
    ('tm_mon', c_int),
    ('tm_year', c_int),
    ('tm_wday', c_int),
    ('tm_yday', c_int),
    ('tm_isdst', c_int),
    ('tm_zone', String),
    ('tm_gmtoff', c_long),
]

struct_SyMemMethods.__slots__ = [
    'xAlloc',
    'xRealloc',
    'xFree',
    'xChunkSize',
    'xInit',
    'xRelease',
    'pUserData',
]
struct_SyMemMethods._fields_ = [
    ('xAlloc', CFUNCTYPE(UNCHECKED(POINTER(None)), c_uint)),
    ('xRealloc', CFUNCTYPE(UNCHECKED(POINTER(None)), POINTER(None), c_uint)),
    ('xFree', CFUNCTYPE(UNCHECKED(None), POINTER(None))),
    ('xChunkSize', CFUNCTYPE(UNCHECKED(c_uint), POINTER(None))),
    ('xInit', CFUNCTYPE(UNCHECKED(c_int), POINTER(None))),
    ('xRelease', CFUNCTYPE(UNCHECKED(None), POINTER(None))),
    ('pUserData', POINTER(None)),
]

ProcMemError = CFUNCTYPE(UNCHECKED(c_int), POINTER(None)) # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 254

struct_SyMutexMethods.__slots__ = [
    'xGlobalInit',
    'xGlobalRelease',
    'xNew',
    'xRelease',
    'xEnter',
    'xTryEnter',
    'xLeave',
]
struct_SyMutexMethods._fields_ = [
    ('xGlobalInit', CFUNCTYPE(UNCHECKED(c_int), )),
    ('xGlobalRelease', CFUNCTYPE(UNCHECKED(None), )),
    ('xNew', CFUNCTYPE(UNCHECKED(POINTER(SyMutex)), c_int)),
    ('xRelease', CFUNCTYPE(UNCHECKED(None), POINTER(SyMutex))),
    ('xEnter', CFUNCTYPE(UNCHECKED(None), POINTER(SyMutex))),
    ('xTryEnter', CFUNCTYPE(UNCHECKED(c_int), POINTER(SyMutex))),
    ('xLeave', CFUNCTYPE(UNCHECKED(None), POINTER(SyMutex))),
]

vedis_real = c_double # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 346

vedis_int64 = sxi64 # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 348

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 456
class struct_vedis_file(Structure):
    pass

vedis_file = struct_vedis_file # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 455

struct_vedis_file.__slots__ = [
    'pMethods',
]
struct_vedis_file._fields_ = [
    ('pMethods', POINTER(vedis_io_methods)),
]

struct_vedis_io_methods.__slots__ = [
    'iVersion',
    'xClose',
    'xRead',
    'xWrite',
    'xTruncate',
    'xSync',
    'xFileSize',
    'xLock',
    'xUnlock',
    'xCheckReservedLock',
    'xSectorSize',
]
struct_vedis_io_methods._fields_ = [
    ('iVersion', c_int),
    ('xClose', CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_file))),
    ('xRead', CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_file), POINTER(None), vedis_int64, vedis_int64)),
    ('xWrite', CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_file), POINTER(None), vedis_int64, vedis_int64)),
    ('xTruncate', CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_file), vedis_int64)),
    ('xSync', CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_file), c_int)),
    ('xFileSize', CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_file), POINTER(vedis_int64))),
    ('xLock', CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_file), c_int)),
    ('xUnlock', CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_file), c_int)),
    ('xCheckReservedLock', CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_file), POINTER(c_int))),
    ('xSectorSize', CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_file))),
]

struct_vedis_vfs.__slots__ = [
    'zName',
    'iVersion',
    'szOsFile',
    'mxPathname',
    'xOpen',
    'xDelete',
    'xAccess',
    'xFullPathname',
    'xTmpDir',
    'xSleep',
    'xCurrentTime',
    'xGetLastError',
    'xMmap',
    'xUnmap',
]
struct_vedis_vfs._fields_ = [
    ('zName', String),
    ('iVersion', c_int),
    ('szOsFile', c_int),
    ('mxPathname', c_int),
    ('xOpen', CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_vfs), String, POINTER(vedis_file), c_uint)),
    ('xDelete', CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_vfs), String, c_int)),
    ('xAccess', CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_vfs), String, c_int, POINTER(c_int))),
    ('xFullPathname', CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_vfs), String, c_int, String)),
    ('xTmpDir', CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_vfs), String, c_int)),
    ('xSleep', CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_vfs), c_int)),
    ('xCurrentTime', CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_vfs), POINTER(Sytm))),
    ('xGetLastError', CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_vfs), c_int, String)),
    ('xMmap', CFUNCTYPE(UNCHECKED(c_int), String, POINTER(POINTER(None)), POINTER(vedis_int64))),
    ('xUnmap', CFUNCTYPE(UNCHECKED(None), POINTER(None), vedis_int64)),
]

pgno = sxu64 # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 587

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 593
class struct_vedis_page(Structure):
    pass

vedis_page = struct_vedis_page # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 592

struct_vedis_page.__slots__ = [
    'zData',
    'pUserData',
]
struct_vedis_page._fields_ = [
    ('zData', POINTER(c_ubyte)),
    ('pUserData', POINTER(None)),
]

vedis_kv_handle = POINTER(None) # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 602

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 610
class struct_vedis_kv_io(Structure):
    pass

vedis_kv_io = struct_vedis_kv_io # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 609

struct_vedis_kv_io.__slots__ = [
    'pHandle',
    'pMethods',
    'xGet',
    'xLookup',
    'xNew',
    'xWrite',
    'xDontWrite',
    'xDontJournal',
    'xDontMkHot',
    'xPageRef',
    'xPageUnref',
    'xPageSize',
    'xReadOnly',
    'xTmpPage',
    'xSetUnpin',
    'xSetReload',
    'xErr',
]
struct_vedis_kv_io._fields_ = [
    ('pHandle', vedis_kv_handle),
    ('pMethods', POINTER(vedis_kv_methods)),
    ('xGet', CFUNCTYPE(UNCHECKED(c_int), vedis_kv_handle, pgno, POINTER(POINTER(vedis_page)))),
    ('xLookup', CFUNCTYPE(UNCHECKED(c_int), vedis_kv_handle, pgno, POINTER(POINTER(vedis_page)))),
    ('xNew', CFUNCTYPE(UNCHECKED(c_int), vedis_kv_handle, POINTER(POINTER(vedis_page)))),
    ('xWrite', CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_page))),
    ('xDontWrite', CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_page))),
    ('xDontJournal', CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_page))),
    ('xDontMkHot', CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_page))),
    ('xPageRef', CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_page))),
    ('xPageUnref', CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_page))),
    ('xPageSize', CFUNCTYPE(UNCHECKED(c_int), vedis_kv_handle)),
    ('xReadOnly', CFUNCTYPE(UNCHECKED(c_int), vedis_kv_handle)),
    ('xTmpPage', CFUNCTYPE(UNCHECKED(POINTER(c_ubyte)), vedis_kv_handle)),
    ('xSetUnpin', CFUNCTYPE(UNCHECKED(None), vedis_kv_handle, CFUNCTYPE(UNCHECKED(None), POINTER(None)))),
    ('xSetReload', CFUNCTYPE(UNCHECKED(None), vedis_kv_handle, CFUNCTYPE(UNCHECKED(None), POINTER(None)))),
    ('xErr', CFUNCTYPE(UNCHECKED(None), vedis_kv_handle, String)),
]

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 640
class struct_vedis_kv_cursor(Structure):
    pass

vedis_kv_cursor = struct_vedis_kv_cursor # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 639

struct_vedis_kv_cursor.__slots__ = [
    'pStore',
]
struct_vedis_kv_cursor._fields_ = [
    ('pStore', POINTER(vedis_kv_engine)),
]

struct_vedis_kv_engine.__slots__ = [
    'pIo',
]
struct_vedis_kv_engine._fields_ = [
    ('pIo', POINTER(vedis_kv_io)),
]

struct_vedis_kv_methods.__slots__ = [
    'zName',
    'szKv',
    'szCursor',
    'iVersion',
    'xInit',
    'xRelease',
    'xConfig',
    'xOpen',
    'xReplace',
    'xAppend',
    'xCursorInit',
    'xSeek',
    'xFirst',
    'xLast',
    'xValid',
    'xNext',
    'xPrev',
    'xDelete',
    'xKeyLength',
    'xKey',
    'xDataLength',
    'xData',
    'xReset',
    'xCursorRelease',
]
struct_vedis_kv_methods._fields_ = [
    ('zName', String),
    ('szKv', c_int),
    ('szCursor', c_int),
    ('iVersion', c_int),
    ('xInit', CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_kv_engine), c_int)),
    ('xRelease', CFUNCTYPE(UNCHECKED(None), POINTER(vedis_kv_engine))),
    ('xConfig', CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_kv_engine), c_int, c_void_p)),
    ('xOpen', CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_kv_engine), pgno)),
    ('xReplace', CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_kv_engine), POINTER(None), c_int, POINTER(None), vedis_int64)),
    ('xAppend', CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_kv_engine), POINTER(None), c_int, POINTER(None), vedis_int64)),
    ('xCursorInit', CFUNCTYPE(UNCHECKED(None), POINTER(vedis_kv_cursor))),
    ('xSeek', CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_kv_cursor), POINTER(None), c_int, c_int)),
    ('xFirst', CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_kv_cursor))),
    ('xLast', CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_kv_cursor))),
    ('xValid', CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_kv_cursor))),
    ('xNext', CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_kv_cursor))),
    ('xPrev', CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_kv_cursor))),
    ('xDelete', CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_kv_cursor))),
    ('xKeyLength', CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_kv_cursor), POINTER(c_int))),
    ('xKey', CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_kv_cursor), CFUNCTYPE(UNCHECKED(c_int), POINTER(None), c_uint, POINTER(None)), POINTER(None))),
    ('xDataLength', CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_kv_cursor), POINTER(vedis_int64))),
    ('xData', CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_kv_cursor), CFUNCTYPE(UNCHECKED(c_int), POINTER(None), c_uint, POINTER(None)), POINTER(None))),
    ('xReset', CFUNCTYPE(UNCHECKED(None), POINTER(vedis_kv_cursor))),
    ('xCursorRelease', CFUNCTYPE(UNCHECKED(None), POINTER(vedis_kv_cursor))),
]

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 737
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_open'):
        continue
    vedis_open = _lib.vedis_open
    vedis_open.argtypes = [POINTER(POINTER(vedis)), String]
    vedis_open.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 738
for _lib in _libs.values():
    if hasattr(_lib, 'vedis_config'):
        _func = _lib.vedis_config
        _restype = c_int
        _argtypes = [POINTER(vedis), c_int]
        vedis_config = _variadic_function(_func,_restype,_argtypes)

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 739
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_close'):
        continue
    vedis_close = _lib.vedis_close
    vedis_close.argtypes = [POINTER(vedis)]
    vedis_close.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 742
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_exec'):
        continue
    vedis_exec = _lib.vedis_exec
    vedis_exec.argtypes = [POINTER(vedis), String, c_int]
    vedis_exec.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 743
for _lib in _libs.values():
    if hasattr(_lib, 'vedis_exec_fmt'):
        _func = _lib.vedis_exec_fmt
        _restype = c_int
        _argtypes = [POINTER(vedis), String]
        vedis_exec_fmt = _variadic_function(_func,_restype,_argtypes)

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 744
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_exec_result'):
        continue
    vedis_exec_result = _lib.vedis_exec_result
    vedis_exec_result.argtypes = [POINTER(vedis), POINTER(POINTER(vedis_value))]
    vedis_exec_result.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 747
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_register_command'):
        continue
    vedis_register_command = _lib.vedis_register_command
    vedis_register_command.argtypes = [POINTER(vedis), String, CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_context), c_int, POINTER(POINTER(vedis_value))), POINTER(None)]
    vedis_register_command.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 748
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_delete_command'):
        continue
    vedis_delete_command = _lib.vedis_delete_command
    vedis_delete_command.argtypes = [POINTER(vedis), String]
    vedis_delete_command.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 751
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_kv_store'):
        continue
    vedis_kv_store = _lib.vedis_kv_store
    vedis_kv_store.argtypes = [POINTER(vedis), POINTER(None), c_int, POINTER(None), vedis_int64]
    vedis_kv_store.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 752
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_kv_append'):
        continue
    vedis_kv_append = _lib.vedis_kv_append
    vedis_kv_append.argtypes = [POINTER(vedis), POINTER(None), c_int, POINTER(None), vedis_int64]
    vedis_kv_append.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 753
for _lib in _libs.values():
    if hasattr(_lib, 'vedis_kv_store_fmt'):
        _func = _lib.vedis_kv_store_fmt
        _restype = c_int
        _argtypes = [POINTER(vedis), POINTER(None), c_int, String]
        vedis_kv_store_fmt = _variadic_function(_func,_restype,_argtypes)

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 754
for _lib in _libs.values():
    if hasattr(_lib, 'vedis_kv_append_fmt'):
        _func = _lib.vedis_kv_append_fmt
        _restype = c_int
        _argtypes = [POINTER(vedis), POINTER(None), c_int, String]
        vedis_kv_append_fmt = _variadic_function(_func,_restype,_argtypes)

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 755
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_kv_fetch'):
        continue
    vedis_kv_fetch = _lib.vedis_kv_fetch
    vedis_kv_fetch.argtypes = [POINTER(vedis), POINTER(None), c_int, POINTER(None), POINTER(vedis_int64)]
    vedis_kv_fetch.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 756
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_kv_fetch_callback'):
        continue
    vedis_kv_fetch_callback = _lib.vedis_kv_fetch_callback
    vedis_kv_fetch_callback.argtypes = [POINTER(vedis), POINTER(None), c_int, CFUNCTYPE(UNCHECKED(c_int), POINTER(None), c_uint, POINTER(None)), POINTER(None)]
    vedis_kv_fetch_callback.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 758
for _lib in _libs.values():
    if hasattr(_lib, 'vedis_kv_config'):
        _func = _lib.vedis_kv_config
        _restype = c_int
        _argtypes = [POINTER(vedis), c_int]
        vedis_kv_config = _variadic_function(_func,_restype,_argtypes)

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 759
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_kv_delete'):
        continue
    vedis_kv_delete = _lib.vedis_kv_delete
    vedis_kv_delete.argtypes = [POINTER(vedis), POINTER(None), c_int]
    vedis_kv_delete.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 762
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_begin'):
        continue
    vedis_begin = _lib.vedis_begin
    vedis_begin.argtypes = [POINTER(vedis)]
    vedis_begin.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 763
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_commit'):
        continue
    vedis_commit = _lib.vedis_commit
    vedis_commit.argtypes = [POINTER(vedis)]
    vedis_commit.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 764
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_rollback'):
        continue
    vedis_rollback = _lib.vedis_rollback
    vedis_rollback.argtypes = [POINTER(vedis)]
    vedis_rollback.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 767
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_util_random_string'):
        continue
    vedis_util_random_string = _lib.vedis_util_random_string
    vedis_util_random_string.argtypes = [POINTER(vedis), String, c_uint]
    vedis_util_random_string.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 768
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_util_random_num'):
        continue
    vedis_util_random_num = _lib.vedis_util_random_num
    vedis_util_random_num.argtypes = [POINTER(vedis)]
    vedis_util_random_num.restype = c_uint
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 771
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_context_kv_store'):
        continue
    vedis_context_kv_store = _lib.vedis_context_kv_store
    vedis_context_kv_store.argtypes = [POINTER(vedis_context), POINTER(None), c_int, POINTER(None), vedis_int64]
    vedis_context_kv_store.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 772
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_context_kv_append'):
        continue
    vedis_context_kv_append = _lib.vedis_context_kv_append
    vedis_context_kv_append.argtypes = [POINTER(vedis_context), POINTER(None), c_int, POINTER(None), vedis_int64]
    vedis_context_kv_append.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 773
for _lib in _libs.values():
    if hasattr(_lib, 'vedis_context_kv_store_fmt'):
        _func = _lib.vedis_context_kv_store_fmt
        _restype = c_int
        _argtypes = [POINTER(vedis_context), POINTER(None), c_int, String]
        vedis_context_kv_store_fmt = _variadic_function(_func,_restype,_argtypes)

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 774
for _lib in _libs.values():
    if hasattr(_lib, 'vedis_context_kv_append_fmt'):
        _func = _lib.vedis_context_kv_append_fmt
        _restype = c_int
        _argtypes = [POINTER(vedis_context), POINTER(None), c_int, String]
        vedis_context_kv_append_fmt = _variadic_function(_func,_restype,_argtypes)

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 775
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_context_kv_fetch'):
        continue
    vedis_context_kv_fetch = _lib.vedis_context_kv_fetch
    vedis_context_kv_fetch.argtypes = [POINTER(vedis_context), POINTER(None), c_int, POINTER(None), POINTER(vedis_int64)]
    vedis_context_kv_fetch.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 776
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_context_kv_fetch_callback'):
        continue
    vedis_context_kv_fetch_callback = _lib.vedis_context_kv_fetch_callback
    vedis_context_kv_fetch_callback.argtypes = [POINTER(vedis_context), POINTER(None), c_int, CFUNCTYPE(UNCHECKED(c_int), POINTER(None), c_uint, POINTER(None)), POINTER(None)]
    vedis_context_kv_fetch_callback.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 778
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_context_kv_delete'):
        continue
    vedis_context_kv_delete = _lib.vedis_context_kv_delete
    vedis_context_kv_delete.argtypes = [POINTER(vedis_context), POINTER(None), c_int]
    vedis_context_kv_delete.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 781
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_context_throw_error'):
        continue
    vedis_context_throw_error = _lib.vedis_context_throw_error
    vedis_context_throw_error.argtypes = [POINTER(vedis_context), c_int, String]
    vedis_context_throw_error.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 782
for _lib in _libs.values():
    if hasattr(_lib, 'vedis_context_throw_error_format'):
        _func = _lib.vedis_context_throw_error_format
        _restype = c_int
        _argtypes = [POINTER(vedis_context), c_int, String]
        vedis_context_throw_error_format = _variadic_function(_func,_restype,_argtypes)

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 783
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_context_random_num'):
        continue
    vedis_context_random_num = _lib.vedis_context_random_num
    vedis_context_random_num.argtypes = [POINTER(vedis_context)]
    vedis_context_random_num.restype = c_uint
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 784
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_context_random_string'):
        continue
    vedis_context_random_string = _lib.vedis_context_random_string
    vedis_context_random_string.argtypes = [POINTER(vedis_context), String, c_int]
    vedis_context_random_string.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 785
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_context_user_data'):
        continue
    vedis_context_user_data = _lib.vedis_context_user_data
    vedis_context_user_data.argtypes = [POINTER(vedis_context)]
    vedis_context_user_data.restype = POINTER(None)
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 786
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_context_push_aux_data'):
        continue
    vedis_context_push_aux_data = _lib.vedis_context_push_aux_data
    vedis_context_push_aux_data.argtypes = [POINTER(vedis_context), POINTER(None)]
    vedis_context_push_aux_data.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 787
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_context_peek_aux_data'):
        continue
    vedis_context_peek_aux_data = _lib.vedis_context_peek_aux_data
    vedis_context_peek_aux_data.argtypes = [POINTER(vedis_context)]
    vedis_context_peek_aux_data.restype = POINTER(None)
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 788
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_context_pop_aux_data'):
        continue
    vedis_context_pop_aux_data = _lib.vedis_context_pop_aux_data
    vedis_context_pop_aux_data.argtypes = [POINTER(vedis_context)]
    vedis_context_pop_aux_data.restype = POINTER(None)
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 791
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_result_int'):
        continue
    vedis_result_int = _lib.vedis_result_int
    vedis_result_int.argtypes = [POINTER(vedis_context), c_int]
    vedis_result_int.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 792
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_result_int64'):
        continue
    vedis_result_int64 = _lib.vedis_result_int64
    vedis_result_int64.argtypes = [POINTER(vedis_context), vedis_int64]
    vedis_result_int64.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 793
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_result_bool'):
        continue
    vedis_result_bool = _lib.vedis_result_bool
    vedis_result_bool.argtypes = [POINTER(vedis_context), c_int]
    vedis_result_bool.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 794
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_result_double'):
        continue
    vedis_result_double = _lib.vedis_result_double
    vedis_result_double.argtypes = [POINTER(vedis_context), c_double]
    vedis_result_double.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 795
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_result_null'):
        continue
    vedis_result_null = _lib.vedis_result_null
    vedis_result_null.argtypes = [POINTER(vedis_context)]
    vedis_result_null.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 796
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_result_string'):
        continue
    vedis_result_string = _lib.vedis_result_string
    vedis_result_string.argtypes = [POINTER(vedis_context), String, c_int]
    vedis_result_string.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 797
for _lib in _libs.values():
    if hasattr(_lib, 'vedis_result_string_format'):
        _func = _lib.vedis_result_string_format
        _restype = c_int
        _argtypes = [POINTER(vedis_context), String]
        vedis_result_string_format = _variadic_function(_func,_restype,_argtypes)

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 798
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_result_value'):
        continue
    vedis_result_value = _lib.vedis_result_value
    vedis_result_value.argtypes = [POINTER(vedis_context), POINTER(vedis_value)]
    vedis_result_value.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 801
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_value_to_int'):
        continue
    vedis_value_to_int = _lib.vedis_value_to_int
    vedis_value_to_int.argtypes = [POINTER(vedis_value)]
    vedis_value_to_int.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 802
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_value_to_bool'):
        continue
    vedis_value_to_bool = _lib.vedis_value_to_bool
    vedis_value_to_bool.argtypes = [POINTER(vedis_value)]
    vedis_value_to_bool.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 803
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_value_to_int64'):
        continue
    vedis_value_to_int64 = _lib.vedis_value_to_int64
    vedis_value_to_int64.argtypes = [POINTER(vedis_value)]
    vedis_value_to_int64.restype = vedis_int64
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 804
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_value_to_double'):
        continue
    vedis_value_to_double = _lib.vedis_value_to_double
    vedis_value_to_double.argtypes = [POINTER(vedis_value)]
    vedis_value_to_double.restype = c_double
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 805
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_value_to_string'):
        continue
    vedis_value_to_string = _lib.vedis_value_to_string
    vedis_value_to_string.argtypes = [POINTER(vedis_value), POINTER(c_int)]
    if sizeof(c_int) == sizeof(c_void_p):
        vedis_value_to_string.restype = ReturnString
    else:
        vedis_value_to_string.restype = String
        vedis_value_to_string.errcheck = ReturnString
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 808
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_value_is_int'):
        continue
    vedis_value_is_int = _lib.vedis_value_is_int
    vedis_value_is_int.argtypes = [POINTER(vedis_value)]
    vedis_value_is_int.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 809
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_value_is_float'):
        continue
    vedis_value_is_float = _lib.vedis_value_is_float
    vedis_value_is_float.argtypes = [POINTER(vedis_value)]
    vedis_value_is_float.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 810
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_value_is_bool'):
        continue
    vedis_value_is_bool = _lib.vedis_value_is_bool
    vedis_value_is_bool.argtypes = [POINTER(vedis_value)]
    vedis_value_is_bool.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 811
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_value_is_string'):
        continue
    vedis_value_is_string = _lib.vedis_value_is_string
    vedis_value_is_string.argtypes = [POINTER(vedis_value)]
    vedis_value_is_string.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 812
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_value_is_null'):
        continue
    vedis_value_is_null = _lib.vedis_value_is_null
    vedis_value_is_null.argtypes = [POINTER(vedis_value)]
    vedis_value_is_null.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 813
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_value_is_numeric'):
        continue
    vedis_value_is_numeric = _lib.vedis_value_is_numeric
    vedis_value_is_numeric.argtypes = [POINTER(vedis_value)]
    vedis_value_is_numeric.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 814
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_value_is_scalar'):
        continue
    vedis_value_is_scalar = _lib.vedis_value_is_scalar
    vedis_value_is_scalar.argtypes = [POINTER(vedis_value)]
    vedis_value_is_scalar.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 815
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_value_is_array'):
        continue
    vedis_value_is_array = _lib.vedis_value_is_array
    vedis_value_is_array.argtypes = [POINTER(vedis_value)]
    vedis_value_is_array.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 818
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_value_int'):
        continue
    vedis_value_int = _lib.vedis_value_int
    vedis_value_int.argtypes = [POINTER(vedis_value), c_int]
    vedis_value_int.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 819
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_value_int64'):
        continue
    vedis_value_int64 = _lib.vedis_value_int64
    vedis_value_int64.argtypes = [POINTER(vedis_value), vedis_int64]
    vedis_value_int64.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 820
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_value_bool'):
        continue
    vedis_value_bool = _lib.vedis_value_bool
    vedis_value_bool.argtypes = [POINTER(vedis_value), c_int]
    vedis_value_bool.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 821
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_value_null'):
        continue
    vedis_value_null = _lib.vedis_value_null
    vedis_value_null.argtypes = [POINTER(vedis_value)]
    vedis_value_null.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 822
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_value_double'):
        continue
    vedis_value_double = _lib.vedis_value_double
    vedis_value_double.argtypes = [POINTER(vedis_value), c_double]
    vedis_value_double.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 823
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_value_string'):
        continue
    vedis_value_string = _lib.vedis_value_string
    vedis_value_string.argtypes = [POINTER(vedis_value), String, c_int]
    vedis_value_string.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 824
for _lib in _libs.values():
    if hasattr(_lib, 'vedis_value_string_format'):
        _func = _lib.vedis_value_string_format
        _restype = c_int
        _argtypes = [POINTER(vedis_value), String]
        vedis_value_string_format = _variadic_function(_func,_restype,_argtypes)

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 825
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_value_reset_string_cursor'):
        continue
    vedis_value_reset_string_cursor = _lib.vedis_value_reset_string_cursor
    vedis_value_reset_string_cursor.argtypes = [POINTER(vedis_value)]
    vedis_value_reset_string_cursor.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 826
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_value_release'):
        continue
    vedis_value_release = _lib.vedis_value_release
    vedis_value_release.argtypes = [POINTER(vedis_value)]
    vedis_value_release.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 829
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_context_new_scalar'):
        continue
    vedis_context_new_scalar = _lib.vedis_context_new_scalar
    vedis_context_new_scalar.argtypes = [POINTER(vedis_context)]
    vedis_context_new_scalar.restype = POINTER(vedis_value)
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 830
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_context_new_array'):
        continue
    vedis_context_new_array = _lib.vedis_context_new_array
    vedis_context_new_array.argtypes = [POINTER(vedis_context)]
    vedis_context_new_array.restype = POINTER(vedis_value)
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 831
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_context_release_value'):
        continue
    vedis_context_release_value = _lib.vedis_context_release_value
    vedis_context_release_value.argtypes = [POINTER(vedis_context), POINTER(vedis_value)]
    vedis_context_release_value.restype = None
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 834
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_array_fetch'):
        continue
    vedis_array_fetch = _lib.vedis_array_fetch
    vedis_array_fetch.argtypes = [POINTER(vedis_value), c_uint]
    vedis_array_fetch.restype = POINTER(vedis_value)
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 835
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_array_walk'):
        continue
    vedis_array_walk = _lib.vedis_array_walk
    vedis_array_walk.argtypes = [POINTER(vedis_value), CFUNCTYPE(UNCHECKED(c_int), POINTER(vedis_value), POINTER(None)), POINTER(None)]
    vedis_array_walk.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 836
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_array_insert'):
        continue
    vedis_array_insert = _lib.vedis_array_insert
    vedis_array_insert.argtypes = [POINTER(vedis_value), POINTER(vedis_value)]
    vedis_array_insert.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 837
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_array_count'):
        continue
    vedis_array_count = _lib.vedis_array_count
    vedis_array_count.argtypes = [POINTER(vedis_value)]
    vedis_array_count.restype = c_uint
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 838
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_array_reset'):
        continue
    vedis_array_reset = _lib.vedis_array_reset
    vedis_array_reset.argtypes = [POINTER(vedis_value)]
    vedis_array_reset.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 839
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_array_next_elem'):
        continue
    vedis_array_next_elem = _lib.vedis_array_next_elem
    vedis_array_next_elem.argtypes = [POINTER(vedis_value)]
    vedis_array_next_elem.restype = POINTER(vedis_value)
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 842
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_lib_init'):
        continue
    vedis_lib_init = _lib.vedis_lib_init
    vedis_lib_init.argtypes = []
    vedis_lib_init.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 843
for _lib in _libs.values():
    if hasattr(_lib, 'vedis_lib_config'):
        _func = _lib.vedis_lib_config
        _restype = c_int
        _argtypes = [c_int]
        vedis_lib_config = _variadic_function(_func,_restype,_argtypes)

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 844
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_lib_shutdown'):
        continue
    vedis_lib_shutdown = _lib.vedis_lib_shutdown
    vedis_lib_shutdown.argtypes = []
    vedis_lib_shutdown.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 845
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_lib_is_threadsafe'):
        continue
    vedis_lib_is_threadsafe = _lib.vedis_lib_is_threadsafe
    vedis_lib_is_threadsafe.argtypes = []
    vedis_lib_is_threadsafe.restype = c_int
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 846
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_lib_version'):
        continue
    vedis_lib_version = _lib.vedis_lib_version
    vedis_lib_version.argtypes = []
    if sizeof(c_int) == sizeof(c_void_p):
        vedis_lib_version.restype = ReturnString
    else:
        vedis_lib_version.restype = String
        vedis_lib_version.errcheck = ReturnString
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 847
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_lib_signature'):
        continue
    vedis_lib_signature = _lib.vedis_lib_signature
    vedis_lib_signature.argtypes = []
    if sizeof(c_int) == sizeof(c_void_p):
        vedis_lib_signature.restype = ReturnString
    else:
        vedis_lib_signature.restype = String
        vedis_lib_signature.errcheck = ReturnString
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 848
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_lib_ident'):
        continue
    vedis_lib_ident = _lib.vedis_lib_ident
    vedis_lib_ident.argtypes = []
    if sizeof(c_int) == sizeof(c_void_p):
        vedis_lib_ident.restype = ReturnString
    else:
        vedis_lib_ident.restype = String
        vedis_lib_ident.errcheck = ReturnString
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 849
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'vedis_lib_copyright'):
        continue
    vedis_lib_copyright = _lib.vedis_lib_copyright
    vedis_lib_copyright.argtypes = []
    if sizeof(c_int) == sizeof(c_void_p):
        vedis_lib_copyright.restype = ReturnString
    else:
        vedis_lib_copyright.restype = String
        vedis_lib_copyright.errcheck = ReturnString
    break

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 71
try:
    VEDIS_VERSION = '1.2.6'
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 77
try:
    VEDIS_VERSION_NUMBER = 1002006
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 82
try:
    VEDIS_SIG = 'vedis/1.2.6'
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 89
try:
    VEDIS_IDENT = 'vedis:e361b2f3d4a71ac17e9f2ac1876232a13467dea1'
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 99
try:
    VEDIS_COPYRIGHT = 'Copyright (C) Symisc Systems, S.U.A.R.L [Mrad Chems Eddine <chm@symisc.net>] 2013, http://vedis.symisc.net/'
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 274
try:
    SXRET_OK = 0
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 275
try:
    SXERR_MEM = (-1)
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 276
try:
    SXERR_IO = (-2)
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 277
try:
    SXERR_EMPTY = (-3)
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 278
try:
    SXERR_LOCKED = (-4)
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 279
try:
    SXERR_ORANGE = (-5)
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 280
try:
    SXERR_NOTFOUND = (-6)
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 281
try:
    SXERR_LIMIT = (-7)
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 282
try:
    SXERR_MORE = (-8)
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 283
try:
    SXERR_INVALID = (-9)
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 284
try:
    SXERR_ABORT = (-10)
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 285
try:
    SXERR_EXISTS = (-11)
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 286
try:
    SXERR_SYNTAX = (-12)
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 287
try:
    SXERR_UNKNOWN = (-13)
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 288
try:
    SXERR_BUSY = (-14)
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 289
try:
    SXERR_OVERFLOW = (-15)
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 290
try:
    SXERR_WILLBLOCK = (-16)
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 291
try:
    SXERR_NOTIMPLEMENTED = (-17)
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 292
try:
    SXERR_EOF = (-18)
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 293
try:
    SXERR_PERM = (-19)
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 294
try:
    SXERR_NOOP = (-20)
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 295
try:
    SXERR_FORMAT = (-21)
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 296
try:
    SXERR_NEXT = (-22)
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 297
try:
    SXERR_OS = (-23)
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 298
try:
    SXERR_CORRUPT = (-24)
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 299
try:
    SXERR_CONTINUE = (-25)
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 300
try:
    SXERR_NOMATCH = (-26)
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 301
try:
    SXERR_RESET = (-27)
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 302
try:
    SXERR_DONE = (-28)
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 303
try:
    SXERR_SHORT = (-29)
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 304
try:
    SXERR_PATH = (-30)
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 305
try:
    SXERR_TIMEOUT = (-31)
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 306
try:
    SXERR_BIG = (-32)
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 307
try:
    SXERR_RETRY = (-33)
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 308
try:
    SXERR_IGNORE = (-63)
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 315
try:
    VEDIS_OK = SXRET_OK
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 317
try:
    VEDIS_NOMEM = SXERR_MEM
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 318
try:
    VEDIS_ABORT = SXERR_ABORT
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 319
try:
    VEDIS_IOERR = SXERR_IO
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 320
try:
    VEDIS_CORRUPT = SXERR_CORRUPT
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 321
try:
    VEDIS_LOCKED = SXERR_LOCKED
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 322
try:
    VEDIS_BUSY = SXERR_BUSY
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 323
try:
    VEDIS_DONE = SXERR_DONE
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 324
try:
    VEDIS_PERM = SXERR_PERM
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 325
try:
    VEDIS_NOTIMPLEMENTED = SXERR_NOTIMPLEMENTED
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 326
try:
    VEDIS_NOTFOUND = SXERR_NOTFOUND
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 327
try:
    VEDIS_NOOP = SXERR_NOOP
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 328
try:
    VEDIS_INVALID = SXERR_INVALID
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 329
try:
    VEDIS_EOF = SXERR_EOF
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 330
try:
    VEDIS_UNKNOWN = SXERR_UNKNOWN
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 331
try:
    VEDIS_LIMIT = SXERR_LIMIT
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 332
try:
    VEDIS_EXISTS = SXERR_EXISTS
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 333
try:
    VEDIS_EMPTY = SXERR_EMPTY
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 334
try:
    VEDIS_FULL = (-73)
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 335
try:
    VEDIS_CANTOPEN = (-74)
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 336
try:
    VEDIS_READ_ONLY = (-75)
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 337
try:
    VEDIS_LOCKERR = (-76)
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 363
try:
    VEDIS_CONFIG_ERR_LOG = 1
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 364
try:
    VEDIS_CONFIG_MAX_PAGE_CACHE = 2
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 365
try:
    VEDIS_CONFIG_KV_ENGINE = 4
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 366
try:
    VEDIS_CONFIG_DISABLE_AUTO_COMMIT = 5
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 367
try:
    VEDIS_CONFIG_GET_KV_NAME = 6
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 368
try:
    VEDIS_CONFIG_DUP_EXEC_VALUE = 7
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 369
try:
    VEDIS_CONFIG_RELEASE_DUP_VALUE = 8
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 370
try:
    VEDIS_CONFIG_OUTPUT_CONSUMER = 9
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 384
try:
    VEDIS_KV_CONFIG_HASH_FUNC = 1
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 385
try:
    VEDIS_KV_CONFIG_CMP_FUNC = 2
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 410
try:
    VEDIS_LIB_CONFIG_USER_MALLOC = 1
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 411
try:
    VEDIS_LIB_CONFIG_MEM_ERR_CALLBACK = 2
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 412
try:
    VEDIS_LIB_CONFIG_USER_MUTEX = 3
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 413
try:
    VEDIS_LIB_CONFIG_THREAD_LEVEL_SINGLE = 4
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 414
try:
    VEDIS_LIB_CONFIG_THREAD_LEVEL_MULTI = 5
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 415
try:
    VEDIS_LIB_CONFIG_VFS = 6
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 416
try:
    VEDIS_LIB_CONFIG_STORAGE_ENGINE = 7
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 417
try:
    VEDIS_LIB_CONFIG_PAGE_SIZE = 8
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 430
try:
    VEDIS_SYNC_NORMAL = 2
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 431
try:
    VEDIS_SYNC_FULL = 3
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 432
try:
    VEDIS_SYNC_DATAONLY = 16
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 440
try:
    VEDIS_LOCK_NONE = 0
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 441
try:
    VEDIS_LOCK_SHARED = 1
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 442
try:
    VEDIS_LOCK_RESERVED = 2
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 443
try:
    VEDIS_LOCK_PENDING = 3
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 444
try:
    VEDIS_LOCK_EXCLUSIVE = 4
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 579
try:
    VEDIS_ACCESS_EXISTS = 0
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 580
try:
    VEDIS_ACCESS_READWRITE = 1
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 581
try:
    VEDIS_ACCESS_READ = 2
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 648
try:
    VEDIS_CURSOR_MATCH_EXACT = 1
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 649
try:
    VEDIS_CURSOR_MATCH_LE = 2
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 650
try:
    VEDIS_CURSOR_MATCH_GE = 3
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 719
try:
    VEDIS_JOURNAL_FILE_SUFFIX = '_vedis_journal'
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 729
try:
    VEDIS_CTX_ERR = 1
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 730
try:
    VEDIS_CTX_WARNING = 2
except:
    pass

# /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 731
try:
    VEDIS_CTX_NOTICE = 3
except:
    pass

vedis_io_methods = struct_vedis_io_methods # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 498

vedis_kv_methods = struct_vedis_kv_methods # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 679

vedis_kv_engine = struct_vedis_kv_engine # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 666

vedis_context = struct_vedis_context # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 104

vedis_value = struct_vedis_value # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 105

vedis_vfs = struct_vedis_vfs # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 543

vedis = struct_vedis # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 107

SyMutexMethods = struct_SyMutexMethods # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 256

SyMemMethods = struct_SyMemMethods # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 243

SyString = struct_SyString # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 194

syiovec = struct_syiovec # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 183

SyMutex = struct_SyMutex # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 180

Sytm = struct_Sytm # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 200

vedis_file = struct_vedis_file # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 456

vedis_page = struct_vedis_page # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 593

vedis_kv_io = struct_vedis_kv_io # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 610

vedis_kv_cursor = struct_vedis_kv_cursor # /home/charles/tmp/scrap/z1/src/vedis/vedis/src/vedis.h: 640

# No inserted files

