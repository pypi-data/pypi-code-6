import sys, time

db_url = 'rpc:127.0.0.1:8080'
if len(sys.argv) > 1:
	db_url = sys.argv[1]

import F2
db = F2.connect(db_url)

C = db.TupleClass.create(className='test_C')
n = db.Attribute.create(attributeName = 'nom', origClass=C, termClass=db.String)
n.set_reverse_function()

x1 = C.create(nom='titi')
x2 = C.create(nom='tutu')
x3 = C.create(nom='toto')
x4 = C.create(nom='titi')
x5 = C.create(nom='tutu')
x6 = C.create(nom='toto')
x7 = C.create(nom='titi')
x8 = C.create(nom='tutu')
x9 = C.create(nom='toto')

print "les titis:", [(x,x.nom) for x in C(nom='titi')]
print "les tutus:", [(x,x.nom) for x in C(nom='tutu')]
print "les totos:", [(x,x.nom) for x in C(nom='toto')]

db.close()