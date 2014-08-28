""" test2.py
    - measure object creation performances: time to insert 10000 employees in the database.
"""
import sys, time

db_url = 'rpc:127.0.0.1:8080'
if len(sys.argv) > 1:
	db_url = sys.argv[1]

import F2
db = F2.connect(db_url)


P = db.CLASS(className = 'Person')

if P:
	print "Class Person seems to already exist"
	P = P[0]
	E = db.Employee
else:
	print "Create a class Person"
	P = db.TupleClass.create(className='Person')
	n = db.Attribute.create(attributeName = 'nom', domainClass=P, rangeClass=db.String)
	print "P =", P
	print "Create a sub-class Employee of Person"
	E = db.TupleClass.create(className='Employee')
	E = db.SubClass.enter(E, superClass=P)
	n = db.Attribute.create(attributeName = 'manager', domainClass=E, rangeClass=P)
	print "E =", E
	
theBoss = P.create(nom='Zebigboss')

NB_OBJ = 30000

specials = (3, 33, 333, 3333, 6666)


print "Creating %d employees (100 for each displayed dot)" % NB_OBJ
now = time.time()
for i in xrange( 1, NB_OBJ ):
	e = E.create(nom='collaborateur_%d' % i, manager=theBoss)
	if i % 100 == 0:
		print '.',
		if i % 2000 == 0:
			print ' '
		sys.stdout.flush()
	if i in specials:
		e.nom = 'Titi'

print "I'm over creating them, took me %6.4f seconds" % (time.time()-now)

print "now committing..."
db.commit()

print "Done, closing"
db.close()

	