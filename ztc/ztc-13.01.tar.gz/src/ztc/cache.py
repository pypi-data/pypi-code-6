#!/usr/bin/env python
'''
Created on 17.12.2009

@author: vrusinov
'''

import os
import cPickle
import time 
import unittest

import ztc.commons

class Cache(object):
    """
    ZTC cache object
    
    used for caching results of heavy calls
    """
    
    def load(self, key, max_age=60):
        """
        Load data from cache. If no data in cache or it is too old, return None
        """
        tmpdir = ztc.commons.get_tmpdir()
        filename = os.path.join(tmpdir, "cache_%s" % (key, ))
        try:
            f = open(filename, 'r')
            co = cPickle.load(f)
            f.close()
            if co.age <= max_age:
                ret = co
            else:
                ret = None
        except:
            raise
            ret = None
        return ret
    
    def save(self, key, co):
        """
        Save cacheobject
        """
        tmpdir = ztc.commons.get_tmpdir()
        filename = os.path.join(tmpdir, "cache_%s" % (key, ))
        try:
            f = open(filename, 'w')
            cPickle.dump(co, f)
            f.close()
            return 1
        except:
            raise
            return 0
        
        

class CacheObject(object):
    """
    ZTC cache object
    """
    ctime = 0
    data = None
    
    def __init__(self):
        self.ctime = time.time()
    
    def get_age(self):
        return time.time() - self.ctime
    age = property(get_age)


###############################################################################
# Tests
    