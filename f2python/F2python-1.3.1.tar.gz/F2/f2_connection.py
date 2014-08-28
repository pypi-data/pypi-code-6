"""
F2 Database Interface
---------------------

Definition of   F 2 _ C o n n e c t i o n, 

the traditional DB accessor of a database API.
Also contains the f2_caster: the mapping between
python code classes and F2 classes. 

Th. Estier

version 1.2 - june 2005
   --
   written after the original Ada version from 1989-1990, Th. Estier, CUI Geneva.
"""
import sys, OFF, transaction

import f2_object, f2_class
F2_Object = f2_object.F2_Object
F2_Object_list = f2_object.F2_Object_list
F2_Class = f2_class.F2_Class


####################  F 2 _ C o n n e c t i o n  ####################

class F2_Connection:
    "an object accessor for a F2 database storage."
    
    def __init__(self, storage_name = 'file:root.db', u='', p='', alt_c=None):
        """The storage_name may have three forms: 
           - file:<local pathname to file storage>
           - rpc:<host_address>:<port_number>
           - shared:
           In the later case, an alternate connection is given in alt_c
        """
        OS = OFF.OFFStore(storage_name, username=u, passwd=p, alt_connection=alt_c)
        self.OFFStore = OS
        self.db_root = OS.db_root
        self.connection = OS.connection
        self.db = OS.db
        OFF.cache_functions(OS)
        self.fix_registered_Python_Klasses()
            
    def __getattr__(self, name):
        return f2_class.F2_Class(name)
    
    def class_create(self, className, superClass=None, schema={}, database=None):
        """A syntactic short-circuit for declaring classes. Example:
           db.class_create(className='Person', database=Mybase,
                           schema={'firstname': db.String,
                                   'lastname' : db.String,
                                   'work_in'  : db.Department})
           schema is a dictionary interpreted as a list of attributes for the class.
           If argument superClass is given, a sub-class is created.
           If argument database is given, the new created class is attached to db 'database'.
           For each attribute, cardinalities (min & max) may be precised in a tuple
           with the range (or rangeClass)
        """ 
        newC = F2_Class('TupleClass').create(className = className)
        if superClass:
            F2_Class('SubClass').enter(newC, superClass = superClass)
        if database:
            if isinstance(database, str):
                db_name = database
                database = self.Database(name=db_name)
                if isinstance(database, list):
                    if database == []:
                        database = self.Database.create(name=db_name)
                    else:
                        database = database[0]
            newC.db = database
        Attribute = F2_Class('Attribute')
        for attr_name, attr_vals in schema.items():
            if isinstance(attr_vals, tuple):
                rangeC = attr_vals[0]
                if len(attr_vals) >= 2:
                    minCard = 0
                    maxCard = attr_vals[1]
                if len(attr_vals) >= 3:
                    minCard = maxCard
                    maxCard = attr_vals[2]
                if maxCard in ('n', 'N', '*'):
                    maxCard = sys.maxint
            else:
                rangeC = attr_vals
                minCard = None
                maxCard = None
            n = Attribute.create(attributeName = attr_name,
                                 domainClass = newC,
                                 rangeClass = rangeC,
                                 visibility = 1)
            if minCard is not None:
                n.minCard = minCard
                n.maxCard = maxCard
        return newC
    
    def html_repr(self, some_value, visited_objs=None, using=None, depth=1):
        """produce a html representation of some_value, which may
           be either a single F2_Object, or a F2_Object_list
           By default, render null values as blanks, to avoid '?'-clutters. """
        if not visited_objs:
            visited_objs = []
        if isinstance(some_value, list):
            if isinstance(some_value[0], F2_Object):
                return self.html_table_repr(some_value, visited_objs, using, depth-1)
            else:
                res = '<table class="f2valuelist">\n'
                for o in some_value:
                    res = res + '<tr><td>%s</td></tr>\n' % self.html_repr(o, 
                                                                          visited_objs+some_value,
                                                                          using = using,
                                                                          depth = depth-1)
                return res + '</table>\n'
        elif isinstance(some_value, F2_Object):
            if depth <= 0 or some_value in visited_objs or not some_value:
                if some_value:
                    return html_encode(str(some_value))
                else:
                    return " "
            else:
                return self.html_table_repr(F2_Object_list([some_value]), 
                                            visited_objs+[some_value], 
                                            using, 
                                            depth-1)
        else: # some_value is an atomic (python) value: a string, an int, ... or '?'.
            if some_value != '?':
                return html_encode(str(some_value))
            else:
                return " "
            
    def html_table_repr(self, value_list, visited_objs=None, using=None, depth=1):
        """produce a table representation of an (F2) object list. """
        if using is None: using = []
        o_class = F2_Class(value_list[0])
        attr_list = [(a.attributeName, a.rangeClass.className) 
                      for a in o_class.all_attributes() 
                      if a.visibility == 1 and (a.attributeName in using or not using)]
        res='<table class="f2table">\n<tr>'
        for a,c in attr_list:
            res = res + '<th title="%s">%s</th>' % (c,a)
        for obj in value_list:
            res = res + '</tr>\n<tr>'
            for a,c in attr_list:
                res = res + '<td>%s</td>' % self.html_repr(getattr(obj, a),
                                                           visited_objs+[obj],
                                                           using = using,
                                                           depth = depth-1)
        return res + '</tr></table>\n'
        
    def pack(self):
        "require F2 storage to squeeze/pack allocated storage ressources (files, tables, etc.)"
        self.db.pack()
    
    def commit(self):
        transaction.commit()
        self.connection.sync()
        
    def rollback(self):
        transaction.abort()
        self.connection.sync()
        
    def close(self, commit_needed=True):
        "last operation on F2_Connection before application stops."
        self.OFFStore.close(commit_needed)

    def fix_registered_Python_Klasses(self):
        "tune mapping between F2 classes and Python representatives"
        new_caster = { }
        for f2_k, Python_Klass in f2_object.python_caster.items():
            if hasattr(Python_Klass, 'class_schema'):
                c_s = Python_Klass.class_schema
                if callable(c_s):
                    Python_Klass.class_schema(f2_db=self)
            try:
                new_caster[F2_Class(f2_k)._rank] = Python_Klass
            except:
                new_caster[f2_k] = Python_Klass
        f2_object.python_caster = new_caster
    
    
def html_encode(s):
    "html encodes strings with simple entities"
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
    
