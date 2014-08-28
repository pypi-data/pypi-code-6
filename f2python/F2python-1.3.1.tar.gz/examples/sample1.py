""" test.py
"""
import sys, F2

db_url = 'rpc:127.0.0.1:8080'
if len(sys.argv) > 1:
	db_url = sys.argv[1]
db = F2.connect(db_url)

P = db.CLASS(className = 'Person')
E = db.CLASS(className = 'Employee')

if P:
	print "Class Person seems to already exist"
	P = P[0]
	joe = P(nom='joe') or P.create(nom='joe')
	toto = P(nom='toto')
	if not toto:
		E = E[0]
		toto = E.create(nom='toto', manager=joe)
else:
	print "Create a class Person"
	P = db.class_create('Person', schema={'nom':db.String})
	print "P =", P
	print "Create a sub-class Employee of Person"
	E = db.class_create('Employee', superClass=P, schema={'manager':P})
	print "E =", E
	joe = P.create(nom='joe')
	toto = E.create(nom='toto', manager=joe)
	
print "All persons:", P().nom
print "All employees:", E().nom
	
try:
	D = db.Department
	print "Class Department seems to already exist"
	marketing = D(nom='Marketing')
	if not marketing:
		marketing = D.create(nom = 'Marketing')
except:
	print "Create a class Department"
	D = db.class_create('Department', schema = {'nom':db.String })
	work = db.Attribute.create(attributeName = 'work_in', 
	                           domainClass = P, 
	                           rangeClass = D)
	marketing = D.create(nom = 'Marketing')

print "Initially, Joe worked in:", joe.work_in
joe.work_in = marketing
print "Now, Joe works in:", joe.work_in.nom

allMetaK = db.CLASS.all_subclasses()
print "all meta K = ", allMetaK

allPs = P.all_subclasses()
print "all kind of persons =", allPs

print "now trying to remove department marketing..."
db.Department.leave(marketing)

print "Now Class Department is:", D().nom
print "... then persons are:", P().nom
print "... and employees are:", E().nom

print "Now joe.work_in = ", joe.work_in, "and toto works for:", toto.manager.nom

print "Lets change a little things: build a new department (finance)"
finance = D.create(nom = 'Finance')
print "finance = ", finance
joe.work_in = finance

print "and lets assign minimum cardinality to some attributes: Employee.manager and Person.work_in"
F2.F2_Attribute('manager', db.Employee).minCard = 1
F2.F2_Attribute('work_in', db.Person).minCard = 1

print "...and lets try again !"

print "joe works in:", joe.work_in
print "toto works for joe is:", (toto.manager == joe)

D.leave(finance)
print "Now Class Department is:", D().nom
print "... then persons are:", P().nom
print "... and employees are:", E().nom


print "Now making the test repeatable by deleting these classes"
db.CLASS.leave(D); db.CLASS.leave(P); db.CLASS.leave(E)
print "Done, closing"
db.close()
