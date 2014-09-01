#!/usr/bin/env python
""" ZTC Store class
Used for storing temporary values & cache

Copyright (c) 2010-2011 Vladimir Rusinov <vladimir@greenmice.info>
Copyright (c) 2011 Wrike, Inc. [http://www.wrike.com]
"""

import os
import time
import cPickle as pickle

class ZTCStore(object):
    """ class for storing data in key files """
    
    ## properties
    ttl = 7200 # default TTL for entry: 2 hours
    
    def __init__(self, name, options, ttl=7200):
        """ Args:
        * name - name of store item
        * options = optparse options object. Needed for getting path of tmpdir
        """
        self.mydir = os.path.join(options.tmpdir, 'store')
        self.myfile = os.path.join(self.mydir, name)
        if not os.path.isdir(self.mydir):
            os.makedirs(self.mydir)
        self.ttl = ttl
    
    def _mktmpdir(self, dir):
        """ check & make tmp dir """
        if not os.path.isdir(dir):
            os.makedirs(dir)        
    
    def get(self):
        """ retirn stored object """
        ret = None
        if os.path.isfile(self.myfile):
            if time.time() - os.stat(self.myfile).st_mtime > self.ttl:
                # do not store for more then ttl seconds
                self.clear()
            else:        
                f = open(self.myfile, 'r')
                ret = pickle.load(f)
                f.close()
        return ret
    
    def set(self, val):
        """ set value """
        try:
            f = open(self.myfile, 'w')
            pickle.dump(val, f)
            f.close()
        except:
            pass # set should never fail
    
    def clear(self):
        os.unlink(self.myfile)

if __name__ == '__main__':
    # some tests
    class C:
        tmpdir = '/tmp/ztc'
    c = C()
    s = ZTCStore('test', c)
    data = "test data"
    
    print "set - get test:"
    s.set(data)
    print s.get()
    
    print "set - get test, ttl 60"
    s.ttl = 60
    print s.get()
    
    print "set - get test, ttl 1"
    s.ttl = 1
    from time import sleep
    sleep(2)
    print s.get()