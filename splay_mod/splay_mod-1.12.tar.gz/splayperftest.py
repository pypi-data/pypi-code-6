#!/usr/bin/env python

import time
try:
	import psyco
except:
	pass
else:
	psyco.full()
import splay_mod
import random

n=1000000
tick = n / 10
splay = splay_mod.Splay()
t0 = time.time()
for i in xrange(n):
	if i % tick == 0:
		print '%5.1f%%...' % (float(i) / n * 100)
	splay.insert(int(random.random() * n), None)
print '%5.1f%%...' % (float(n) / n * 100)
t1 = time.time()
difference = t1 - t0
if difference > 50:
	print "Something's wrong - this usually takes about 30 to 40 seconds (on a 1795MHz Intel CPU)"
	print "But this time it took", difference, "seconds, which is more than 50 seconds"
else:
	print "Test passed - took", difference, "seconds"

