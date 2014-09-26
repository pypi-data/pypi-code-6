#!/usr/bin/env python

import time
import py_treap as treap
import random

n=100000
tick = n / 10
t = treap.treap()
t0 = time.time()
for i in xrange(n):
    if i % tick == 0:
        print '%5.1f%%...' % (float(i) / n * 100)
    t[int(random.random() * n)] = None
print '%5.1f%%...' % (float(n) / n * 100)
t1 = time.time()
difference = t1 - t0
if difference > 20:
    print "Something's wrong - this usually takes about 4 to 8 seconds (on a 1795MHz Intel CPU"
    print "But this time it took", difference, "seconds, which is more than 20 seconds"
else:
    print "Test passed - took", difference, "seconds"

