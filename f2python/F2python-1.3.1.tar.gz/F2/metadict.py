
#--------------------- T H E   A T T R I B U T E S  -----------------------

stateAttribute = 0  #-- state attribute of "Attribute"
attributeName  = 1  #-- name of each attribute
rangeClass     = 2  #-- the range of the attribute  (was named termClass)
domainClass    = 3  #-- the domain of the attribute (was named origClass)
minCard	       = 4  #-- minimum cardinality 
maxCard	       = 5  #-- maximum cardinality 
visibility     = 6  #-- visibility of each attribute

#----------------------- 
#--	class CLASS  --
#-----------------------
stateCLASS	= 7 #-- state attribute. of "CLASS"
className       = 8 #-- name of the class

#-----------------------------------------------------------------
#-- sub class AtomClass (called domains in the good ol'times)   --
#-----------------------------------------------------------------
stateAtomClass = 9  #-- state attribute. of classes by intension
baseType       = 10 #-- attribute to class baseTypes.
infValue       = 11 #-- minimum value for this domain
supValue       = 12 #-- maximum value for this domain

#--------------------------
#--  sub class tupleClass  --
#--------------------------
stateTupleClass  = 13
classStateattribute  = 14 #-- state attr. of classes by extension
#-- ...


#-------------------------------
#--    sub class subClass     --
#-------------------------------
stateSubClass = 15 #-- state attribute of "SUBCLASS"
superClass    = 16  #-- generic class (or super class) of sc.

#---------------------
#-- class BaseTypes --
#---------------------
stateBaseTypes = 17
baseTypeName = 18

#--------------------- T H E    C L A S S E S  --------------------------------

Attribute = 20

CLASS	  = 21
atomClass  = 22   #-- subclass of CLASS
tupleClass  = 23  #-- subclass of CLASS
subClass    = 24  #-- subclass of CLASS

entityState     = 25  #-- an atomClass to define states of an entity.
intClass        = 26  #-- the unconstrained atomClass of basetype isInt
realClass       = 27  #-- the unconstrained atomClass of basetype isReal 
timeClass       = 28  #-- the least constrained atomClass of basetype isTime.
stringClass     = 29  #-- the least constrained atomClass of basetype isString.
dicIdent        = 30  #-- a deprecated string class, here for backward compatibility.
AnyValue        = 31  #-- a generic value class. (special purpose reference
                      #   class, its necessity is meta-tricky..., this is NOT the
                      #   Object meta-class, this is NOT the root of all hierarchies)
                      #   F2 meta-model has no root meta-class, and this is on purpose:
                      #   F2 is not meta-layered, F2 is meta-circular. 
                      #   'AnyValue' only denotes the range of two attributes which have
                      #   a totally unconstrained atomic range (or rangeClass). You can
                      #   safely totally ignore this non-class.

baseTypes       = 32  #-- (intType, stringType, realType, timeType, anyType)
                      #   NB: isRef is for object references (was only used in F2-Ada).

#----------------- baseTypes values -------------------
intType = 33
realType = 34
timeType = 35
stringType = 36
anyType = 37

#---------------- MAX_OID  must be the greatest integer constant defined in this module.
MAX_METADICT_OID = 38