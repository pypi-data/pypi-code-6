"""   
"""
import json
from hyperdns.hal.navigator import HALRoot
from hyperdns.netdns import RecordSpec

class HAPI(HALRoot):
    """This is basically our 'client' object - will eventually move to client.py
    """
                    
                    
    def __init__(self,jwt,baseUrl=None):
        super(HAPI,self).__init__(jwt,baseUrl)

    @property
    def active_vendors(self):
        """return the active vendors, iterable
        """
        for v in self.vendors.values():
            if v.active:
                yield v
    
    @property
    def inactive_vendors(self):
        """return the inactive vendors, iterable
        """
        for v in self.vendors.values():
            if not v.active:
                yield v

    @property
    def active_zones(self):
        """return only those zones that are not ignored
        """
        for z in self.zones.values():
            if not z.ignored:
                yield z

    @property
    def ignored_zones(self):
        """return only those zones that are ignored
        """
        for z in self.zones.values():
            if z.ignored:
                yield z
        
def json_safe_zoneinfo(zoneinfo):
    for res in zoneinfo['resources']:
        recs=[]
        for rec in res['records']:
            if isinstance(rec,RecordSpec):
                recs.append(rec.json)
            else:
                recs.append(rec)
        res['records']=recs
    return zoneinfo
   
from .account import *
from .vendor import *
from .zone import *
from .resource import *
from .pools import *