#sundials_core.py is part of the PySUNDIALS package, and is released under the
#following terms and conditions.

#Copyright (c) 2007, James Dominy, Brett Olivier, Jan Hendrik Hofmeyr, Johann Rohwer
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met:
#
#1. Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#2. Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
#3. Neither the name of the <ORGANIZATION> nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
#LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
#SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
#INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
#CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#POSSIBILITY OF SUCH DAMAGE.

"""Provides low level auxiliary functonality for use by other PySUNDIALS modules,
including dynamic library linking, configuration location and parsing, and type
mapping for the realtype.
"""

import ctypes
from ctypes import util
import os
import sys
import re
import subprocess
from pysundials import realtype

__pysundials_version="rc4"
__sundials_version="2.3.0"

if os.name == "nt":
	libc = ctypes.CDLL(util.find_library('msvcrt'))
else:
	libc = ctypes.CDLL(util.find_library('c'))

try:
	libc.fdopen.argtypes = [ctypes.c_int, ctypes.c_int]
	libc.fdopen.restype = ctypes.c_void_p
	fdopen = libc.fdopen
except:
	libc._fdopen.argtypes = [ctypes.c_int, ctypes.c_int]
	libc._fdopen.restype = ctypes.c_void_p
	fdopen = libc._fdopen

libsigs = {
	"nvecserial": "N_VNew_Serial",
	"nvecparallel": None,
	"cvode": "CVodeCreate",
	"cvodes": "CVodeCreate",
	"ida": "IDACreate",
	"idas": None,
	"kinsol": "KINCreate"
}

def loadlib(libname):
	'''Links the specified library into the running python interpreter.\nlibname must be one of 'nvecserial', 'nvecparallel', 'cvode', 'cvodes', 'ida', or 'kinsol'.'''
	try:
		p = subprocess.Popen(['sundials-config', '-m', libname, '-t', 's', '-l', 'c', '-s', 'libs'], stdout=subprocess.PIPE)
	except OSError as e:
		if e.errno == 2:
			raise OSError("Cannot execute sundials-config, please ensure sundials-config exists and is in your PATH.")
		else:
			raise e

	libdir = p.communicate()[0].split()[0][2:]

	found = False
	for candidate in [os.path.join(libdir,fname) for fname in sorted(os.listdir(libdir)) if fname.startswith("libsundials_"+libname+".")]:
		try:
			lib = ctypes.CDLL(candidate)
			lib.__getattr__(libsigs[libname])
			found = True
			break
		except OSError, e:
			pass

	if not found:
		raise OSError("%s\nCannot load shared library %s. It is not where sundials-config indicates it should be."%(e, libname))
	else:
		return lib

if os.path.dirname(__file__) == '':
	dirname = '.'
else:
	dirname = os.path.dirname(__file__)

#auxlibname = filter(lambda s: "realtype" in s and not s.endswith(".c"),os.listdir(dirname))[0]
#sundials_core_aux = ctypes.CDLL(os.path.join(dirname,auxlibname))
#
#realsize = sundials_core_aux.getsizeofrealtype()
realsize = realtype.getsizeofrealtype()

try:
	import numpy
	numpy_imported = True
	numpy_ndarray = numpy.ndarray
	from_memory = ctypes.pythonapi.PyBuffer_FromReadWriteMemory
	from_memory.restype = ctypes.py_object
except:
	numpy_imported = False

if realsize > ctypes.sizeof(ctypes.c_double):
	raise AssertionError("SUNDIALS ERROR: size of realtype is extended, which cannot be represented in python!")
elif realsize == ctypes.sizeof(ctypes.c_double):
	realtype = ctypes.c_double
	UNIT_ROUNDOFF = 1e-9
	if numpy_imported:
		numpyrealtype = 'float64'
else:
	realtype = ctypes.c_float
	UNIT_ROUNDOFF = 1e-6
	if numpy_imported:
		numpyrealtype = 'float32'

del realsize
