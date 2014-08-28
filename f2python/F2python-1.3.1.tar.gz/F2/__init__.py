"""
F2 Database Interface
---------------------

Provides primitive access to an F2 Database content. This layer is
built immediately on top of module OFF. Defines the most generic
class for F2 objects handles: F2_Object(), and some specific
subclasses: F2_Class(), F2_Attribute(), etc...

Th. Estier

version 1.3.1 - august 2014
   --
   written after the original Ada version from 1989-1990, Th. Estier, CUI Geneva.
"""

import f2_object, f2_class, f2_attribute, f2_connection, OFF, OFFboot

debug = False # controls debug messages printed by all modules of the package

F2_Object = f2_object.F2_Object
F2_Object_list = f2_object.F2_Object_list
F2_NULL = f2_object.F2_NULL
F2_Class = f2_class.F2_Class
F2_Attribute = f2_attribute.F2_Attribute

for f2_module in (f2_object, f2_class, f2_attribute, f2_connection):
	f2_module.debug = debug

def connect(storage_name = 'file:root.db', username='', passwd='', alt_connect=None):
	"""Opens an F2 database connection and returns an accessor.
	   The storage_name may have three forms: 
	       - file:<local pathname to file storage>
	       - rpc:<host_address>:<port_number>
	       - shared:
	   In the 3rd case, a connection is already open on some storage, and is
	   passed in parameter alt_connect.
	 """
	return f2_connection.F2_Connection(storage_name, u=username, p=passwd, alt_c=alt_connect)
	
_RegisterPythonClass = f2_object._RegisterPythonClass

