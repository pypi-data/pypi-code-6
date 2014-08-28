"""Farandole 2 bootstrapper: builds the kernel using information from metadict.py
   ------------------------
   Th. Estier
   version 1.0 - 4 may 2004
   
   written by adaptation of the Ada version (source file: bootfarandole.adb)
   Simplifications: - subclasses have no specialisation predicates,
                    - atomclasses are of a unique kind, 
"""
import metadict
from metadict import *
import OFF
import sys

db = None

def insertAttribute(attributeNo, aName, aRange, aCla, aVisi):
	"insert an entity in class attribute and build it" 
	print "adding attribute %s " % aName
	db[stateAttribute][attributeNo] = 0
	db[attributeName] [attributeNo] = aName
	db[rangeClass]    [attributeNo] = aRange
	db[domainClass]   [attributeNo] = aCla
	db[maxCard]       [attributeNo] = 1
	db[minCard]       [attributeNo] = 1
	db[visibility]    [attributeNo] = aVisi
	
	if aCla != metadict.Attribute :
		"if its not an attribute of the meta class 'Attribute', then build one"
		a = OFF.AttributeStorage(attributeNo)

def insertTupleClass(k, kName, is_sub_k=False, super_k=0):
	"insert an entity into class CLASS, into class TupleClass, and possibly a SubClass" 
	db[stateCLASS][k] = 0
	db[className][k] = kName
	db[stateTupleClass][k] = 0
	try:
		kStateAttr = db[attributeName].find('state'+kName)[0]
		db[classStateattribute][k] = kStateAttr
		addBind(stateAttribute, kStateAttr)
	except:
		print "No state attribute [state%s] found for class %s" % (kName, kName)
	if is_sub_k:
		db[stateSubClass][k] = 0
		db[superClass][k] = super_k
		addBind(stateCLASS, super_k)

def insertAtomClass(k, kName, bType, infV='?', supV='?'):
	"insert an entity into class CLASS which is an AtomClass"
	db[stateCLASS][k] = 0
	db[className][k] = kName
	db[stateAtomClass][k] = 0		
	db[baseType][k] = bType;   addBind(stateBaseTypes, bType)	
	db[infValue][k] = infV	
	db[supValue][k] = supV

def addBind(targetStateAttr, targetRank):
	"increment the reference counter of an object"
	db[targetStateAttr][targetRank] += 1

def bootstrap(db_name = 'root.db'):
	"bootstrap process of F2 database"	
	# step 0: clean-up a possibly existing list of AttributeStorage
	# (this new steps was added to help clean up OFF db when re-bootstrapped).
	if db.has_key(stateAttribute) and isinstance(db[stateAttribute], OFF.AttributeStorage):
		for a_oid  in db[stateAttribute].keys():
			if a_oid >= metadict.MAX_METADICT_OID:
				if db[a_oid]:
					dead_a = db[a_oid]
					dead_a.__release__()
	# step 1: build Attribute storage for attributes.
	a = OFF.AttributeStorage( stateAttribute )
	a = OFF.AttributeStorage( attributeName, is_reversed = True )
	a = OFF.AttributeStorage( domainClass, is_reversed = True )
	a = OFF.AttributeStorage( rangeClass )
	a = OFF.AttributeStorage( maxCard )
	a = OFF.AttributeStorage( minCard )
	a = OFF.AttributeStorage( visibility )
	
	#-- class attribute
	
	insertAttribute( stateAttribute,"stateAttribute", entityState,   metadict.Attribute, 0)
	insertAttribute( attributeName, "attributeName",  stringClass,   metadict.Attribute, 1)
	insertAttribute( rangeClass,    "rangeClass",     CLASS,         metadict.Attribute, 1)
	insertAttribute( domainClass,   "domainClass",    tupleClass,    metadict.Attribute, 1)
	insertAttribute( maxCard,       "maxCard",        intClass,      metadict.Attribute, 1)
	insertAttribute( minCard,       "minCard",        intClass,      metadict.Attribute, 1)
	insertAttribute( visibility,    "visibility",     intClass,      metadict.Attribute, 1)
	 
	#-- class CLASS
	
	insertAttribute( stateCLASS, "stateCLASS",	entityState,  CLASS,   0)
	insertAttribute( className,  "className",	stringClass,  CLASS,   1)
	
	#-- subclass SubClass (CLASS)
	insertAttribute( stateSubClass, "stateSubClass", entityState, subClass, 0)
	insertAttribute( superClass,    "superClass",    CLASS,       subClass, 1)

	#-- subclass atomClass (CLASS)
	
	insertAttribute( stateAtomClass, "stateAtomClass", entityState,     atomClass, 0)
	insertAttribute( baseType,       "baseType",       baseTypes,       atomClass, 1)
	insertAttribute( infValue,       "infValue",       AnyValue,        atomClass, 1)
	insertAttribute( supValue,       "supValue",       AnyValue,        atomClass, 1)
	
	#-- subclass tupleClass (CLASS)
	
	insertAttribute(stateTupleClass,"stateTupleClass", entityState,     tupleClass,   0)
	insertAttribute(classStateattribute,  "classStateattribute", metadict.Attribute, tupleClass,1)
	
	#-- class BaseTypes
	
	insertAttribute(stateBaseTypes, "stateBaseType", entityState,    baseTypes, 0)
	insertAttribute(baseTypeName,   "baseTypeName",   stringClass,       baseTypes, 1)
	sbt = db[stateBaseTypes];  btn = db[baseTypeName]
	sbt[intType] = 0;          btn[intType] = "intType"
	sbt[realType] = 0;         btn[realType] = "realType"
	sbt[timeType] = 0;         btn[timeType] = "timeType"
	sbt[stringType] = 0;       btn[stringType] = "stringType"
	sbt[anyType] = 0;          btn[anyType] = "anyType"
	
	#
	#-- Now install (meta-)classes themselves: instance of class CLASS
	#
	insertTupleClass(metadict.Attribute, "Attribute")
	insertTupleClass(CLASS,     "CLASS")
	insertTupleClass(atomClass, "AtomClass",  is_sub_k=True, super_k= CLASS)
	insertTupleClass(tupleClass,"TupleClass", is_sub_k=True, super_k= CLASS)
	insertTupleClass(subClass,  "SubClass",   is_sub_k=True, super_k=CLASS)
	insertTupleClass(baseTypes, "BaseType")
	
	insertAtomClass(entityState, "EntityState", intType, infV=-10, supV=sys.maxint)
	insertAtomClass(intClass,    "Int",         intType, infV=-sys.maxint-1,  supV=sys.maxint)
	insertAtomClass(realClass,   "Real",        realType)
	insertAtomClass(timeClass,   "Time",        timeType)
	insertAtomClass(stringClass, "String",      stringType)
	insertAtomClass(dicIdent,    "DicIdent",    stringType)
	insertAtomClass(AnyValue,    "AnyValue",    anyType)
	
	#
	#-- Updating binds for the whole class Attribute
	#
	for attr_rank in db[stateAttribute].keys():
		if db[stateAttribute][attr_rank] != '?':
			addBind( stateTupleClass, db[domainClass][attr_rank] )
			addBind( stateCLASS,      db[rangeClass][attr_rank] )
			
	#-- reverse some key attributes, or object browsing accelerators.
	#
	db[className].set_reverse()
	db[baseTypeName].set_reverse()
	db[superClass].set_reverse()
	
	#### install DB signature.
	import time
	db['F2_Signature'] = {'db_name' : db_name,
	                      'date_created' : time.time(),
	                      'db_platform' : sys.platform, 
	                      'db_python_version' : sys.version }
	
	#### verify that next F2 oid will be greater than all oids in metadict.
	next_oid = OFF.new_db_oid()
	while next_oid < metadict.MAX_METADICT_OID:
		next_oid = OFF.new_db_oid()
	# now F2 is ready to start over.

def extend_boot(f2_conn):
	"continue bootstrap process, using f2 kernel"
	from F2 import F2_Class, F2_Attribute
	print "1) adding the class 'Database', adding database 'Kernel'"
	DB = f2_conn.class_create(className='Database', schema={'name':f2_conn.String})
	database_name_attr = F2_Attribute('name', of_class=DB)
	database_name_attr.set_reverse_function()
	db_attr = f2_conn.Attribute.create(attributeName='db',
	                                   domainClass=f2_conn.CLASS,
	                                   rangeClass=DB,
	                                   minCard=1, maxCard=1, visibility=1)
	db_attr.set_reverse_function()
	kernel_db  = DB.create(name='Kernel')
	for c in f2_conn.CLASS():
		c.db = kernel_db
	print "All classes created so far belong to database 'Kernel'."
	print "2) adding the class 'Key'"
	K = f2_conn.class_create(className='Key', database=kernel_db,
	                         schema={'keyAttrs':(f2_conn.Attribute,1,'n'),
	                                 'ofClass':f2_conn.TupleClass})
	K.create(ofClass=F2_Class(metadict.CLASS), 
	         keyAttrs=F2_Attribute(metadict.className))
	K.create(ofClass=F2_Class(metadict.Attribute),
	         keyAttrs=[F2_Attribute(metadict.attributeName),
	                   F2_Attribute(metadict.domainClass)])
	K.create(ofClass=F2_Class(metadict.baseTypes), 
	         keyAttrs=F2_Attribute(metadict.baseTypeName))
	K.create(ofClass=DB,
	         keyAttrs= database_name_attr)
	print "  added keys of Kernel classes."
	
############## Start here ###############

def main(db_url, alt_connect=None):
	print "Starting bootstrap process..."
	global db
	try:
		os = OFF.OFFStore(db_url, alt_connection=alt_connect)
	except OFF.F2StorageError:
		os = OFF.currentOFFStore   # special hack to break circularity of bootstrap
	db = os.db_root  
	bootstrap(db_name=db_url)
	if alt_connect is None and db_url != 'shared:':
		os.db.pack()
		os.close(commit_needed = True)
	print "Phase 1 done."
	
	print "Now launching F2..."
	import F2
	db = F2.connect(db_url, alt_connect=alt_connect)
	extend_boot(db)
	if alt_connect is None and db_url != 'shared:':
		db.close()
	print "Phase 2 done."
