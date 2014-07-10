#!/usr/bin/env python

import pinv
import inspect


detected = []
run = []

for item, value in inspect.getmembers(pinv):

    if not item.startswith('__'):
        detected.append(item)
        if '__pinv__' in  dir(value):
            if value.__pinv__:
                run.append(value)

print "detected modules", detected

print "will run modules", [i.__name__ for i in run]

for i in run:
    i.main()


