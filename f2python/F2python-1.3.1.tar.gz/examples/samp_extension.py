""" An example giving a pattern to write the method of a F2 class.
    Th. Estier - jan 2005
   
    Two cases are given:
    1. definition of a simple F2 class "Person".
    2. definition of a meta-class (a subclass of class CLASS) (more complicated...)
       The "triggers" part is useful only if you intend to extend behaviour of
        F2 meta-classes (CLASS, SubClass, Attribute, etc.)
"""
import F2

class Person(F2.F2_Object):

    def hire(self, in_department):
        "this method hires a guy in Employee."
        Emps = F2.F2_Class('Employee')
        if not self.exist_in(Emps):
            Emps.enter(self)
        self.dept = in_department
            
    ###### F2 schema of the class ######
    
    def class_schema(self, f2_db):
        "this is a class-method, called by the registering mechanism."
        if not hasattr(f2_db, 'Person'):
            P = f2_db.class_create(className='Person',
                                   schema={firstname : f2_db.String,
                                           lastname  : f2_db.String})
            E = f2_db.class_create(className='Employee',
                                   superClass=P,
                                   schema={dept : f2_db.Department})
    
#### register my class:
F2._RegisterPythonClass('Person', Person)
F2._RegisterPythonClass('Employee', Person)

#######################################################################################
class MyGigaClass(F2.F2_Class):

    def giga_method(self, param):
        "this method is simply great."
        for attr in self.direct_attributes():
            do_something_great()
    
    ###### triggers ######
    
    def post_create(self, **attr_values):
        "this method is called immediately after the creation of a giga-class."
        do_something_even_better()
    
    def pre_assign(self, name, old_val, new_val):
        "this method is called immediately before the update of a gigaclass attribute."
        raise DontDoThis_Error, "You cannot do that."
        
    ###### F2 schema of the class ######
    
    def class_schema(self, f2_db):
        "this is a class-method, called by the registering mechanism."
        if not hasattr(f2_db, 'GigaClass'):
            f2_db.class_create(className='GigaClass',
                               superClass=f2_connection.CLASS,
                               schema={ --- secret de fabrication --- })
    
#### register my class:
F2._RegisterPythonClass('GigaClass', MyGigaClass)
