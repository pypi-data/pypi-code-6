import sys, time

db_url = 'rpc:127.0.0.1:8080'
if len(sys.argv) > 1:
	db_url = sys.argv[1]

import F2

print "First I will create a new F2 class: SpecialObject"
db = F2.connect(db_url)
testBase = db.Database(name='test') or db.Database.create(name='test')

so = db.CLASS(className='SpecialObject')
if so:
	for c in so:
		db.CLASS.leave(c)
	
special_object = db.class_create('SpecialObject', database=testBase,
                                schema={'specialLabel':db.String} )
db.close()

#####################################

print "Now I will define python methods of this class, and will register it."

class SpecialObject(F2.F2_Object):
	"Let's define a class of F2 objects with a special (redefined) display method"
	def __str__(self):
		return '<Special Object.%s(%s)>' % (self._rank, self.specialLabel)

F2._RegisterPythonClass('SpecialObject', SpecialObject)

#####################################

db = F2.connect(db_url)

monObjet = special_object.create(specialLabel = 'premier')
monObjet = special_object.create(specialLabel = 'second')
monObjet = special_object.create(specialLabel = 'troisieme')

for so in special_object():
	print so

print "Now I will create a sub class of SpecialObject"

very_special = db.class_create('VerySpecial', superClass=special_object,
                                             database=testBase,
                              schema={'otherAttr':db.Int} )

monObjet = very_special.create(specialLabel='special', otherAttr=1)

print "monObjet =", monObjet
print "monObjet.__class__ =", monObjet.__class__
if monObjet.__class__ is not SpecialObject:
	print "test failed."
	
db.close()