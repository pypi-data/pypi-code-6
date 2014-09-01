#!/usr/bin/env python

"""
    ZTC Hardware monitoring package
    
    Copyright (c) 2010-2011 Vladimir Rusinov <vladimir@greenmice.info>
    Copyright (c) 2010 Murano Software [http://muranosoft.com]
    Copyright (c) 2011 Parchment Inc. [http://www.parchment.com]
"""

#from ztc.commons import mypopen, get_config

from ztc.check import ZTCCheck, CheckFail
from ztc.myos import mypopen

class RAID_3Ware(ZTCCheck):
    """
        Class for monitoring 3ware raid.
        Requirements:
            * tw_cli tool installed
            * run as root, or have permissions to run tw_cli
    """
    
    name = 'hw_raid_3ware'
    
    def _get(self, metric):
        if metric == 'status':
            return self.get_status()
        else:
            raise CheckFail('uncknown metric')
    
    def get_status(self, c=0, u=0):
        cmd = "%s info c%i u%i status" % (self.config.get('tw_cli_path', '/opt/3ware/tw_cli'), c, u)
        ret = mypopen(cmd).readlines()[0]
        return ret.split()[3]

if __name__ == '__main__':
    # test
    tw = RAID_3Ware()
    print tw.get_status()