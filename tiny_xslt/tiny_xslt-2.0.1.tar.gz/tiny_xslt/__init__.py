#############################################################################
# Author  : Jerome ODIER
#
# Email   : jerome.odier@cern.ch
#
# Version : 2.0.1 (2013-2014)
#
#############################################################################

import sys
import os, os.path
import ctypes, ctypes.util
import urllib2

#############################################################################
# EXCEPTION                                                                 #
#############################################################################

class Error(Exception):
	pass

#############################################################################
# LIBRARY LOADER                                                            #
#############################################################################

if   os.name == 'posix':

	if sys.platform != 'darwin':
		OS_NAME = 'linux'
		LIBRARY_EXT = '.so'
	else:
		OS_NAME = 'osx'
		LIBRARY_EXT = '.dylib'

elif os.name == 'nt':
	OS_NAME = 'win'
	LIBRARY_EXT = '.dll'

else:
	raise Error('unsupported operating system `%s` !' % sys.platform)

#############################################################################

if   sys.maxsize == 0x000000007FFFFFFF:
	BUS_SIZE = 32
elif sys.maxsize == 0x7FFFFFFFFFFFFFFF:
	BUS_SIZE = 64
else:
	raise Error('could not find out the bus size !')

#############################################################################

def os_get_tag():
	#####################################################################
	# LINUX                                                             #
	#####################################################################

	if OS_NAME == 'linux':
		#############################################################

		try:
			f = os.popen('getconf GNU_LIBC_VERSION')
			lines = f.read()
			f.close()

		except:
			raise Error('could not execute `getconf` !')

		#############################################################

		data = lines.split()

		if len(data) != 2:
			raise Error('could not find out the LINUX version !')

		return 'linux_glibc%s_%dbits' % (data[1], BUS_SIZE)

	#####################################################################
	# OSX                                                               #
	#####################################################################

	if OS_NAME == 'osx':
		#############################################################

		try:
			f = os.popen('sw_vers -productVersion')
			lines = f.read()
			f.close()

		except:
			raise Error('could not execute `sw_vers` !')

		#############################################################

		data = lines.split()

		if len(data) != 1:
			raise Error('could not find out the OSX version !')

		data = data[0].split('.')

		return 'osx_%s.%s' % (data[0], data[1])

	#####################################################################
	# WIN                                                               #
	#####################################################################

	return 'win_%dbits' % BUS_SIZE

#############################################################################

OS_TAG = os_get_tag()

#############################################################################

def library_download(url, path):
	#####################################################################
	# DOWNLOAD LIBRARY                                                  #
	#####################################################################

	try:
		data = urllib2.urlopen(url).read()

	except urllib2.HTTPError:
		raise Error('ask your administrator to install libxml and libxslt !' % url)

	#####################################################################
	# WRITE LIBRARY                                                     #
	#####################################################################

	try:
		f = open(path, 'wb')
		f.write(data)
		f.close()

	except IOError:
		raise Error('could not write `%s` !' % url)

#############################################################################

def library_load(name, dir_name, base_url):
	#####################################################################
	# FIND & LOAD LIBRARY                                               #
	#####################################################################

	library_path = ctypes.util.find_library(name)

	if not library_path is None:

		try:
			return ctypes.cdll.LoadLibrary(library_path)

		except OSError:
			pass

	#####################################################################
	# CREATE LOCAL SANDBOX                                              #
	#####################################################################

	LIBRARY_BASE_PATH = os.path.expanduser("~") + os.sep + dir_name

	if   OS_NAME == 'linux':
		os.putenv('LD_LIBRARY_PATH', '%s:%s' % (LIBRARY_BASE_PATH, os.getenv('LD_LIBRARY_PATH')))
	elif OS_NAME == 'osx':
		os.putenv('DYLD_LIBRARY_PATH', '%s:%s' % (LIBRARY_BASE_PATH, os.getenv('DYLD_LIBRARY_PATH')))
	elif OS_NAME == 'win':
		os.putenv(               'PATH', '%s;%s' % (LIBRARY_BASE_PATH, os.getenv(               'PATH')))

	#####################################################################

	if os.path.isdir(LIBRARY_BASE_PATH) == False:

		try:
			os.mkdir(LIBRARY_BASE_PATH)

		except OSError:
			raise Error('could not create `%s` !' % LIBRARY_BASE_PATH)

	#####################################################################
	# BUILD URL & PATH                                                  #
	#####################################################################

	if base_url[-1] != '/':
		base_url = base_url + '/'

	library_url = base_url + 'lib' + name + '_' + OS_TAG + LIBRARY_EXT

	library_path = LIBRARY_BASE_PATH + os.sep + 'lib' + name + LIBRARY_EXT

	#####################################################################
	# TRY TO LOAD LIBRARY                                               #
	#####################################################################

	try:
		return ctypes.cdll.LoadLibrary(library_path)

	except OSError as e:
		error = e.__str__()

	#####################################################################
	# TRY TO DOWNLOAD LIBRARY                                           #
	#####################################################################

	library_download(library_url, library_path)

	#####################################################################
	# TRY TO LOAD LIBRARY                                               #
	#####################################################################

	try:
		return ctypes.cdll.LoadLibrary(library_path)

	except OSError as e:
		error = e.__str__()

	#####################################################################

	raise Error('could not load library `%s`, %s !' % (name, error))

#############################################################################
# TINY_XSLT                                                                 #
#############################################################################

DIR_NAME = '.tiny_xslt'

URL_BASE = 'https://bitbucket.org/jodier/tiny_xslt/downloads/'

if OS_NAME != 'win':
	LIBXML2 = library_load('xml2', DIR_NAME, URL_BASE)
	LIBXSLT = library_load('xslt', DIR_NAME, URL_BASE)
else:
	LIBXML2 = library_load('xml2-2', DIR_NAME, URL_BASE)
	LIBXSLT = library_load('xslt-1', DIR_NAME, URL_BASE)

#############################################################################

LIBXML2.xmlInitParser()

#############################################################################

# xmlParseMemory #
LIBXML2.xmlParseMemory.restype = ctypes.c_void_p
LIBXML2.xmlParseMemory.argtypes = [ctypes.c_char_p, ctypes.c_int]

# xmlDocGetRootElement #
LIBXML2.xmlDocGetRootElement.restype = ctypes.c_void_p
LIBXML2.xmlDocGetRootElement.argtypes = [ctypes.c_void_p]

# xmlSetProp #
LIBXML2.xmlSetProp.restype = ctypes.c_void_p
LIBXML2.xmlSetProp.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]

# xmlFreeDoc #
LIBXML2.xmlFreeDoc.restype = None
LIBXML2.xmlFreeDoc.argtypes = [ctypes.c_void_p]

#############################################################################

# xsltParseStylesheetDoc #
LIBXSLT.xsltParseStylesheetDoc.restype = ctypes.c_void_p
LIBXSLT.xsltParseStylesheetDoc.argtypes = [ctypes.c_void_p]

# xsltApplyStylesheet #
LIBXSLT.xsltApplyStylesheet.restype = ctypes.c_void_p
LIBXSLT.xsltApplyStylesheet.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(ctypes.c_char_p)]

# xsltSaveResultToString #
LIBXSLT.xsltSaveResultToString.restype = ctypes.c_int
LIBXSLT.xsltSaveResultToString.argtypes = [ctypes.POINTER(ctypes.c_char_p), ctypes.POINTER(ctypes.c_int), ctypes.c_void_p, ctypes.c_void_p]

# xsltFreeStylesheet #
LIBXSLT.xsltFreeStylesheet.restype = None
LIBXSLT.xsltFreeStylesheet.argtypes = [ctypes.c_void_p]

#############################################################################

def _xsl_load(txt):
	doc = LIBXML2.xmlParseMemory(txt, len(txt))

	if doc == 0:
		raise Error('could not parse xsl document !')

	###################
	# PATCH FOR pyAMI #
	###################

	root = LIBXML2.xmlDocGetRootElement(doc)

	LIBXML2.xmlSetProp(root, 'version', '1.0')

	###################
	# PATCH FOR pyAMI #
	###################

	result = LIBXSLT.xsltParseStylesheetDoc(doc)

	if result == 0:
		raise Error('could not parse xsl document !')

	return result

#############################################################################

def _xml_load(txt):
	result = LIBXML2.xmlParseMemory(txt, len(txt))

	if result == 0:
		raise Error('could not parse xml document !')

	return result

#############################################################################

def transform(xsl, xml):
	xsl_doc = _xsl_load(xsl.encode('utf-8'))
	xml_doc = _xml_load(xml.encode('utf-8'))

	res_doc = LIBXSLT.xsltApplyStylesheet(xsl_doc, xml_doc, None)

	if res_doc == 0:
		raise Error('could not transform xml document !')

	size = ctypes.c_int()
	buff = ctypes.c_char_p()

	LIBXSLT.xsltSaveResultToString(ctypes.pointer(buff), ctypes.pointer(size), res_doc, xsl_doc)

	result = buff.value

	LIBXML2.xmlFreeDoc(res_doc)
	LIBXML2.xmlFreeDoc(xml_doc)

	LIBXSLT.xsltFreeStylesheet(xsl_doc)

	return result

#############################################################################
