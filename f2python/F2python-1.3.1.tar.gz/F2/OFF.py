'''OFF.py
   OFF (Objects For Farandole) persistent kernel built in python
   -------------------------------------------------------------
   
   An F2 Database does not store an object as is. Storage strategy is called
   "transposed storage": for each class (or sub-class) only attributes are
   stored. For each attribute a of class C, the storage keeps the
   persistent function (or mapping) f_a : OID -> domain(a) , where
   OID is the set of C instances ids, and domain(a) is the domain
   of attribute a. For an object o, the full value of o is obtained
   by evaluating for each attribute a of o (o.a) the function f_a(o).
   f_a may be multi-valued, in which case f_a is a function onto Parts(domain(a)) 
   (also called the set of all subsets of domain(a). The reciprocal (or reverse)
   function r_f_a may optionnaly be stored, for obvious optimization reasons. 
   
   In this implementation, each persistent function is stored as one or
   two persistent ZODB.BTrees (two when the reciprocal function is also stored).

   Warning: transpose storage is so uncommon that it seems unsensible at first
            sight. But when proper data structures are used for persistent functions,
            scalability of response time and adaptability of schemas are unequalled by
            traditional object storage. Remember that F2 was designed with
            schema evolution and semi-structured data in mind. 
   
   Th. Estier
   version 1.2 - june 2005
   --
   written after the original Ada version from 1989, Th. Estier, CUI Geneva.
'''

from ZODB import FileStorage, DB
from ZEO import ClientStorage
from persistent import Persistent
import BTrees.IOBTree, BTrees.OOBTree
import transaction

import time

NULL_MARK = '?'

class AttributeStorage(Persistent):
	'''The basic class of storage: will store all values of a single attribute.
	   This is called "transposed storage" 
	   An attribute storage is made of either one or two BTrees, 2 when attribute
	   is reversed, that is when both access ways are implemented.
	   '''
	
	def __init__(self, attr_id, is_reversed = False):
		self.id = attr_id
		self.f = BTrees.IOBTree.IOBTree()
		self.r_f = None
		self.is_reversed = is_reversed
		if is_reversed:
			self.r_f = BTrees.OOBTree.OOBTree()
		# attach attribute to current root
		global currentOFFStore
		currentOFFStore.db_root[attr_id] = self
		
	def __release__(self):
		"release storage ressources"
		global currentOFFStore
		del currentOFFStore.db_root[self.id]
		del self.f
		del self.r_f
		self.is_reversed = False
		self.id = None

	def set_reverse(self):
		"add (if not already done) reverse attribute mapping (val -> [keys])"
		if not self.is_reversed:
			self.is_reversed = True
			self.r_f = BTrees.OOBTree.OOBTree()
			r = self.r_f
			for key, val in self.f.items():
				if type(val) is list:
					for v in val:
						try:key_list = r[v] + [key]
						except: key_list = [key]
						r[v] = key_list
				else:
					try: key_list = r[val] + [key]
					except: key_list = [key]
					r[val] = key_list
			self.r_f = r

	def __getitem__(self, key):
		try:
			return self.f[key]
		except:
			return NULL_MARK
		
	def __setitem__(self, key, newval):
		oldval = self[key]
		if oldval != NULL_MARK and newval == NULL_MARK:
			del self.f[key]
		elif newval != NULL_MARK:
			self.f[key] = newval
		if self.is_reversed:
			r = self.r_f
			if oldval != NULL_MARK:
				if type(oldval) is list:
					for v in oldval:
						try:
							key_list = r[v]
							key_list.remove(key)
							r[v] = key_list[:]
						except:
							pass
				else:
					try:
						key_list = r[oldval]
						key_list.remove(key)
						r[old_val] = key_list[:]
					except:
						pass
			if newval != NULL_MARK:
				if type(newval) is list:
					for v in newval:
						try: key_list = r[v] + [key]
						except: key_list = [key]
						r[v] = key_list
				else:
					try: key_list = r[newval] + [key]
					except: key_list = [key]
					r[newval] = key_list
			self.r_f = r
		
	def find(self, value):
		"""lookup value, return list of keys mapping this value.
		   if f is multivalued (stored values are lists):
		   	- if looked up value is a list, returns keys where f[k] == value,
		   	- if looked up value is an atom, returns keys where f[k] contains value"""
		if self.is_reversed:
			"then easy !"
			if type(value) is list:
				# search matching keys.
				candidates = self.r_f[value[0]]
				return [k for k in candidates if self.f[k] == value]
			else:
				# search atomic value
				try:
					return self.r_f[value][:]
				except:
					return []
		else:
			"less easy: looking up..."
			result = []
			if type(value) is list:
				for rank, lookup_val in self.f.items():
					if value == lookup_val:
						result.append(rank)
			else:
				for rank, lookup_val in self.f.items():
					if value == lookup_val or (type(lookup_val) is list and value in lookup_val):
						result.append(rank)				
			return result
	
	def items(self):
		"return the items() iterator on values"
		return self.f.items()
		
	def keys(self):
		"return the keys() iterator on values"
		return self.f.keys()
		
	def minKey(self):
		"return the smallest key on values"
		return self.f.minKey()
		
	def maxKey(self):
		"return the smallest key on values"
		return self.f.maxKey()
		
	def minVal(self):
		"""return the smallest value, that is the smalles key on reverse,
		   trigs a Value Error exception, if attribute not reversed.
		"""
		if self.is_reversed:
			return self.r_f.minKey()
		else:
			raise ValueError, 'minVal() undefined for attribute without reverse function.'
		
	def maxVal(self):
		"""return the largest value, that is the largest key on reverse,
		   trigs a Value Error exception, if attribute not reversed.
		"""
		if self.is_reversed:
			return self.r_f.maxKey()
		else:
			raise ValueError, 'maxVal() undefined for attribute without reverse function.'

class F2StorageError(Exception):
	def __init__(self, msg):
		self.message = msg
	def __str__(self):
		return repr(self.message)
		
#### general functions for OFF persistent storage management

class OFFStore:

    def __init__(self, store_name = 'file:root.db', username='', passwd='', alt_connection=None):
        """Open the F2 object storage, returns the root_object. The store_name may have
           three forms: - file:<local pathname to file storage>
                        - rpc:<host_address>:<port_number>
                        - shared:
           In the 3rd case, a connection is already open on some storage, and is
           passed in parameter alt_connection.
        """
        self.db = None
        self.connection = None
        self.db_root = None

        if store_name.find(':') < 0:
            store_name = 'file:'+store_name

        if store_name[:5] == 'file:' :
            storage = FileStorage.FileStorage(store_name[5:])
            self.db = DB(storage)
            self.connection = self.db.open()
        
        elif store_name[:4] == 'rpc:' :
            server_addr = store_name[4:]
            if server_addr.find(':') >= 0 :
                serv_port = server_addr.split(':')
                serv_port[1] = int(serv_port[1])
                if not serv_port[0]:
                    serv_port[0] = '127.0.0.1'
            else:
                serv_port = [server_addr, 8080]
            storage = ClientStorage.ClientStorage(addr = tuple(serv_port),
                                                  username = username,
                                                  password = passwd)
            self.db = DB(storage)
            self.connection = self.db.open()
        
        elif store_name[:7] == 'shared:' :
            self.connection = alt_connection
            self.db = self.connection.db()
    
        else:
            # nothing known.
            raise F2StorageError, 'Unsupported storage type (file:, rpc:, or shared:).'
    
        self.db_root = self.connection.root()
        global currentOFFStore, db_root
        currentOFFStore = self     # short circuit on current store for bootstrap
        db_root = self.db_root
        
        if not self.db_root.has_key('F2_Signature'):
            raise F2StorageError, "Empty F2 storage, run the bootstrap process (bootf2.py) before usage."


    def close(self, commit_needed = True):
        "Close the F2 object store, commit current transaction except if specified"
        if commit_needed:
            transaction.commit()
        try:
            self.db_root['F2_Signature']['date_last_modified'] = time.time()
        except:
            raise F2StorageError, "Database corrupted, no db signature in store."
        self.db.close()

    def new_db_oid(self):
        "forge a unique OID using the ZODB new_oid() function (managed by current storage class)."
        return reduce(lambda x,y: 256 * x + ord(y), self.connection.new_oid(), 0)

#	
# Short-circuits: cache name lookups in OFF for most frequently used Meta-classes and Meta-attributes.
#
currentOFFStore=None
db_root =       None
stateAttribute=	None
attributeName =	None
domainClass = 	None
rangeClass = 	None
minCard =       None
maxCard =       None
stateCLASS =	None
className = 	None
stateTupleClass=None
stateAtomClass= None
baseType =	    None
infValue =		None
supValue =		None
classStateAttr=	None
stateSubClass =	None
superClass = 	None

def new_db_oid():
	"this function works only after initialization: after cache_function() is called"
	return currentOFFStore.new_db_oid()

import metadict

def cache_functions(offStore):
	global stateAttribute, attributeName, domainClass, rangeClass, stateCLASS, className
	global stateTupleClass, stateAtomClass, classStateAttr, stateSubClass, superClass
	global baseType, infValue, supValue, minCard, maxCard
	db_root = offStore.db_root
	stateAttribute=	db_root[metadict.stateAttribute]
	attributeName =	db_root[metadict.attributeName]
	domainClass = 	db_root[metadict.domainClass]
	rangeClass = 	db_root[metadict.rangeClass]
	minCard =       db_root[metadict.minCard]
	maxCard =       db_root[metadict.maxCard]
	stateCLASS =	db_root[metadict.stateCLASS]
	className = 	db_root[metadict.className]
	stateAtomClass= db_root[metadict.stateAtomClass]
	baseType= 	    db_root[metadict.baseType]
	infValue =		db_root[metadict.infValue]
	supValue =		db_root[metadict.supValue]
	stateTupleClass=db_root[metadict.stateTupleClass]
	classStateAttr=	db_root[metadict.classStateattribute]
	stateSubClass =	db_root[metadict.stateSubClass]
	superClass = 	db_root[metadict.superClass]


	