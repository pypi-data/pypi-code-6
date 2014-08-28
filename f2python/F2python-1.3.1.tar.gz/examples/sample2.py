""" An example showing the syntax for declaring a simple schema using the
    short circuit function "class_create".
    Th. Estier - sept 2004
"""
import sys
db_url = 'rpc:127.0.0.1:8080'
if len(sys.argv) > 1:
	db_url = sys.argv[1]

import F2
db = F2.connect(db_url)

D = db.class_create(className='Department', 
          schema={'name': db.String})
	
P = db.class_create(className='Person', 
			  schema={'firstname': db.String,
			          'lastname' : db.String})

E = db.class_create(className='Employee',
			  superClass=db.Person,
			  schema={'work_in' : (db.Department, 1, 'N'),
		                'manager' : db.Person})

# let's print this schema:

for C in (db.Person, db.Employee, db.Department):
	print "class", C.className
	for attr in C.all_attributes():
		if attr.visibility == 1:
			print "    ", attr.attributeName,':', attr.rangeClass.className,
			if attr.minCard != F2.F2_NULL or attr.maxCard != F2.F2_NULL:
				print  attr.minCard,'..',attr.maxCard
			else:
				print
      
db.close()