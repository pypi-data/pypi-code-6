""" Test the OFF module, the underlying F2 storage engine. 
    Th. Estier - sept 2004
"""

import F2
OFF = F2.OFF

try:
	os = OFF.OFFStore('file:test_off.db')
	print "test_off: existing storage."
except OFF.F2StorageError, e:
	OFF.db_root['F2_Signature'] = { }
	os = OFF.currentOFFStore
	print "test_off: empty storage."

f1 = OFF.AttributeStorage(1, is_reversed = False)
f2 = OFF.AttributeStorage(2, is_reversed = True)
f3 = OFF.AttributeStorage(3, is_reversed = False) # but will become True later.

for x in xrange(100):
	f1[x] = (x * x) % 63
	f2[x] = (x * x) % 31
	f3[x] = (x * x) % 15

print "f1: x -> (x*x) % 63"
print "f2: x -> (x*x) % 31"
print "f3: x -> (x*x) % 15"

print "f1[10] = ", f1[10]; assert f1[10] == 37
print "f2[10] = ", f2[10]; assert f2[10] == 7
print "f3[10] = ", f3[10]; assert f3[10] == 10

print "f1.find(37) = ", f1.find(37); assert f1.find(37) == [10, 17, 46, 53, 73, 80]
print "f2.find(7)  = ", f2.find(7);  assert f2.find(7) ==  [10, 21, 41, 52, 72, 83]
print "f3.find(10) = ", f3.find(10); assert f3.find(10) == [5, 10, 20, 25, 35, 40, 50, 55, 65, 70, 80, 85, 95]

print "longueur des cles: "
for x in f1.keys():
	l = len(f1.find(x))
	if l:
		print x,"->", '#'*l
		
print "now late reversing f3..."
f3.set_reverse()
print "just checking same results."
print "f3[10] = ", f3[10]; assert f3[10] == 10
print "f3.find(10) = ", f3.find(10); assert f3.find(10) == [5, 10, 20, 25, 35, 40, 50, 55, 65, 70, 80, 85, 95]

print "now measuring time to retrieve values."

import time

NB_VAL = 500000
print "creating f4 with %d values." % NB_VAL
f4 = OFF.AttributeStorage(4, is_reversed = True)
now = time.time()
for x in xrange(NB_VAL):
	f4[x] = x
f4[1] = -1
f4[10] = -1
f4[100] = -1
f4[1000] = -1
f4[10000] = -1
print "...took me %6.4f seconds" % (time.time()-now)

print "now retrieving 4 values among %d..." % NB_VAL
now = time.time()
res = f4.find(-1)
print "...took me %6.4f seconds" % (time.time()-now)
print "f4.find(-1) =", res


os.close()
