#!env python
import pitted, os, glob

print 'drop in {d}'.format(d=pitted.drop_in())
for f in glob.glob(os.path.join(os.path.dirname(os.path.abspath(pitted.__file__)), 'gnar/*')):
    with open(f) as b:
        for l in b.readlines():
            print l
