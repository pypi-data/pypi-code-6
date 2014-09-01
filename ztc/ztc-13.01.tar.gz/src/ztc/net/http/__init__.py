#!/usr/bin/env python
'''
ZTC HTTP check class - used to query url

TODO: use this class on nginx and apache templates

Copyright (c) 2010-2011 Vladimir Rusinov <vladimir@greenmice.info>

Licensed under GPL v.3
'''

import urllib2
import time

from ztc.check import ZTCCheck, CheckFail

class HTTP(ZTCCheck):
    name = 'net'
    
    OPTPARSE_MAX_NUMBER_OF_ARGS = 2
    
    def _get(self, metric, *arg):
        if metric == 'ping':
            url = arg[0]
            return self.get_ping(url)
        else:
            raise CheckFail("uncknown metric: %s" % metric)
    
    def _myinit(self):
        self.timeout = self.config.get('timeout', 2)

    
    def get_ping(self, url):
        s = time.time()
        try:
            u = urllib2.urlopen(url, None, self.timeout)
        except TypeError:
            # Changed in version 2.6: timeout was added, versions < 2.6 does not
            # have last param
            u = urllib2.urlopen(url, None)
        return time.time()- s        