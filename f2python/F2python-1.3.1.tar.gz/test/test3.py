"""test3.py
   - measure lookup performances look for 4 employees using their name.
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
	E = db.Employee
else:
	print "run first at least once test2.py on same database"

print "Let's look for employee(s) called 'Titi'..."
now = time.time()
titis = E(nom = 'Titi')
search_time = time.time() - now

print "'found", len(titis), "of them."
for e in titis:
	print "-", e, e.nom

print "in %6.4f seconds." % search_time

print "Now let's optimize: index the reverse function of attribute 'nom' "
attribut_nom = F2.F2_Attribute('nom', P[0])
attribut_nom.set_reverse_function()

print "Let's lookup again..."
now = time.time()
titis = E(nom = 'Titi')
search_time = time.time() - now

print "'found", len(titis), "of them."
for e in titis:
	print "-", e, e.nom

print "in %6.4f seconds." % search_time


print "Done, closing"
db.commit()
db.close()
