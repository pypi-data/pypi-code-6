"""
"""
import json,os
from hyperdns.vendor.core import BaseDriver,ZoneNotFoundException
import logging
from hyperdns.netdns import (
    RecordSpec,RecordClass,
    ZoneData,ResourceData
)

"""

Preparing to delete this method - don't think it is used.
@classmethod
def create_driver(cls,vkey,config=None):
    " ""Return a modified mock driver
    " ""
    cname="HyperDNSDriver_%s" % (vkey)
    cls=type(cname,(HyperDNSDriver,),{})
    cls.vkey=vkey
    cls.name="Mock %s" % vkey
    cls.info={
        'vendor':'HyperDNS Test',
        'service':vkey,
        'description':'This is a mock driver for %s' % vkey,
        'settings':['username','password','persistence_file']
        }
    return cls
"""


class HyperDNSDriver(BaseDriver):
    """ This generates a mock driver for vendor 'vkey', using the settings
    active in the database.  The index is the value of the settings key that
    corresponds to the account identifier - this allows the mock system to
    provide complete multi-user mock environments.  the
    """
    vkey='mock'
    name='Mock Driver'
    info={
        'vendor':'HyperDNS Test',
        'service':'Simple Mock Driver',
        'description':'This is a mock driver for %s' % vkey,
        'settings':['username','password','persistence_file'],
        'angular':{
            'username': {
                'label':'Mock Username',
                'type':'text',
                'placeholder':"User Name"
            },
            'password': {
                'label':'Mock Password',
                'type':'password',
                'placeholder':"Password (should be same as username)"
            },
            'persistence_file': {
                'label':'',
                'type':'hidden',
                'placeholder':""
            }
            
        }
    }
    
    # this is the active state for the driver.  it is organized by username
    # then zone
    state={}
    ismock=True
    
    @classmethod
    def add_user_to_vendor(cls,username):
        cls.state.setdefault(username,{})
    
    @classmethod
    def _reset_config(cls,settings):
        """Reset the driver configuration, restoring anything in a persistence
        file, regenerating the persistence file (in case it was missing), and
        loading any optional data.
        """
        cls.state={}
        pfile=settings.get('persistence_file','')
        if pfile!='':
            if os.path.exists(pfile):
                with open(pfile,'r') as openfile:
                    config=json.loads(openfile.read())
                config.setdefault(settings['username'],{})
            else:
                config={
                    settings['username']:{}
                }
            with open(pfile,'w') as openfile:
                openfile.write(json.dumps(config,sort_keys=True,
                              indent=4, separators=(',', ': ')))
        for fname in settings.get('data',[]):
            cls.merge_mock_data(cls.vkey,fname)
    
    @classmethod
    def merge_mock_data(cls,vkey,fname):
        """Load a json data file into the mock system to simulate contents being
        discovered on the vendor.
        
        Example:
            MockDriver.merge_mock_data('r53','test/zonestates/omrad.org')
        """
        zdata=cls.state
        with open(fname,"r") as infile:
            data=infile.read()
            accounts=json.loads(data)
            for account in accounts:
                for zone in accounts[account]:
                    if not account in zdata.keys():
                        zdata[account]={}
                    zdata[account][zone]=accounts[account][zone]
        
        
                
    @property
    def config(self):
        return self.__class__.state[self.id]

    def _load_config(self):
        if self.persistent==None:
            return
        with open(self.persistent,'r') as fin:
            self.__class__.state=json.loads(fin.read())
            
    def _save_config(self):
        
        class EnhancedJSONEncoder(json.JSONEncoder):
            def default(self, obj):
                if hasattr(obj,'json'):
                    return obj.json
                else:
                    return super().default(obj)
        
        #self.log.info("Saving Configuration:%s" % self.persistent)
        if self.persistent==None:
            return
        with open(self.persistent,'w') as fout:
            fout.write(json.dumps(self.__class__.state,
                    cls=EnhancedJSONEncoder,sort_keys=True,
                      indent=4, separators=(',', ': ')))
            #self.log.info("Done Saving Configuration:%s" % self.persistent)
            
        
    def __init__(self,settings,immediateLogin=True):
        """Creates a mock vendor bound to these settings.
        
        if settings['data'] contains a list of files, those files are
        loaded.
        
        if settings['persistent_file']
        
        Clear the transaction buffer.  Initialize the config
        """        
        self.username=settings.get('username')
        if self.username==None:
            raise MissingRequiredConfigurationException('username')
        self.id=settings['username']
        
        self.password=settings.get('password')
        if self.password==None:
            raise MissingRequiredConfigurationException('password')

        self.persistent=settings.get('persistence_file',
                            os.getenv('HYPERDNS_MOCK_PERSISTENCE_FILE_%s' % self.vkey,None))
        if self.persistent=='':
            self.persistent=None
        if self.persistent!=None and os.path.exists(self.persistent):
            self._load_config()
    
        super(HyperDNSDriver,self).__init__(settings,immediateLogin)

    def login(self):
        """Mock drivers allow login if the username and password match and
        if there is a 'virtual account' in the driver state.  A virtual account
        is present if the username is a top level key in the driver's state.
        """
        u=self.settings.get('username')
        p=self.settings.get('password')
        if u==None or p==None:
            return False
        return u==p and u in self.state.keys()
    
    def logout(self):
        """ does nothing
        """
        pass

    
    def perform_scanZoneList(self):
        """Return the zone list by reading the keys() out of the
        local config
        """
        result=[]
        for name in self.config.keys():
            result.append({
                'name':name
            })
        return result

    
    def perform_scanZone(self,zoneinfo):
        """Scan the zone and return zone description
        
        :param zone zone: the internal
        :returns: description of zone, nameservers, and all resources
        :rtype: JSON definition of zone - see interface for format
        """
        zoneinfo['source']={
            'type':'vendor',
            'vendor':self.vkey
            }
        return zoneinfo

    def _getZone(self,zonename):
        return self.config.get(zonename)

    def _getMatchingRecord(self,rname,zone,spec,matchTTL):
        """Locate a specific record, optionally ignoring the TTL field
        and matching only on type and rdata.
                
        :param rname: the local resource name relative to the zone
        :param zone: vendor specific record for zone
        :param spec: RecordSpec to locate
        :param matchTTL: determines whether or not to ignore TTL on match
        :returns: vendor specific data structure for the record
        :rtype json:
        """
        specs=self.perform_scanResource(rname,zone)
        if specs==None:
            return None
        for record in specs['records']:
            if self._match_rec(spec,record,matchTTL):
                return record
        return None
        
    def perform_scanResource(self,rname,zoneinfo):
        for resource in zoneinfo.get('resources'):
            if resource.get('name')==rname:
                return {
                    'name':rname,
                    'records':[RecordSpec(r) for r in resource['records']]
                    }
        return None
            
    def createZone(self,zone_fqdn,default_ttl=800,admin_email=None):
        zone=self._getZone(zone_fqdn)
        if zone==None:
            self.config[zone_fqdn]={
                'name':zone_fqdn,
                'resources':[]
            }
        self._save_config()
    
    def deleteZone(self,zonename):
        if zonename in self.config.keys():
            del self.config[zonename]
        self._save_config()
    

    def perform_createRecord(self,rname,zone,spec,pool,addrec=False):
        """Create a record from a record spec

        :param rname: the local resource name for which the record is to be deleted
        :type rname: str
        :param zone: the vendor local data structure representing the zone
        :type zone: vendor specific
        :param spec: RecordSpec to add
        :type spec: RecordSpec
        :param pool: Existing records for resource
        :type pool: RecordPool
        """
        #(rname,zonename)=self._identify_names(fqdn_or_rname,zone_fqdn,requireZone=True)
        #zone=self._getZone(zonename)
        zonename=zone['name']
        self.log.debug("Creating Record for %s:%s rec='%s'" % (rname,zonename,spec))
    
        recinfo={
            'ttl':spec['ttl'],
            'rdata':spec['rdata'],
            'type':spec['type'],
            'class':RecordClass.IN.name
        }
        
        # see if we have a record first, if so, then append
        for res in zone['resources']:
            if res['name']==rname:
                recs=res['records']
                recs.append(recinfo)
                self._save_config()
                return
                
        # if this is a new resource, then create it
        zone['resources'].append({
            'name':rname,
            'records':[spec]
        })
        self._save_config()
    
    
    def perform_deleteRecord(self,rname,zone,record):
        """
        """
        #(rname,zonename)=self._identify_names(fqdn_or_rname,zone_fqdn)
        #zone=self._getZone(zonename)
        zonename=zone['name']
        found=[r for r in zone['resources'] if r['name']==rname]
        if len(found)>0:
            resource=found[0]
            newrec=[]
            for rec in resource['records']:
                if rec!=record:
                    newrec.append(rec)
            resource['records']=newrec
        if len(resource['records'])==0:
            zone['resources']=[r for r in zone['resources'] if r['name']!=rname]
        self._save_config()
            

    def hasRecord(self,fqdn_or_rname,spec,zone_fqdn=None,matchTTL=True):
        (rname,zonename)=self._identify_names(fqdn_or_rname,zone_fqdn)
        zone=self._getZone(zonename)
        if zone!=None:
            found=[r for r in zone['resources'] if r['name']==rname]
            if len(found)>0:
                resource=found[0]
                for rec in resource['records']:
                    if self._match_rec(rec,spec,matchTTL):
                        return True
        return False
        
    def perform_hasResource(self,rname,zone):
        """Entirely delete a resource matching a given name.  The zone is indicated
        either via the fqdn_or_rname parameter or passed explicitly in the
        zone_fqdn.  The zone must exist in both cases.  The two parameters are
        used in this way to accommodate cases where the zone is already known
        and we are working with resources relative to a specific zone, avoiding
        the need to form the resource fqdn each time.
        
        :param str fqdn_or_rname: If zone_fqdn is provided, this is interpreted
           as a resource name relative to the zone_fqdn, otherwise it is treated
           as the fqdn of a resource.           
        """
        #(rname,zonename) = self._identify_names(fqdn_or_rname,zone_fqdn,requireZone=True)
        #zone=self._getZone(zonename)
        found=[r for r in zone['resources'] if r['name']==rname]
        return len(found)>0
        
    def deleteResource(self,fqdn_or_rname,zone_fqdn=None):
        """Entirely delete a resource matching a given name.  The zone is indicated
        either via the fqdn_or_rname parameter or passed explicitly in the
        zone_fqdn.  The zone must exist in both cases.  The two parameters are
        used in this way to accommodate cases where the zone is already known
        and we are working with resources relative to a specific zone, avoiding
        the need to form the resource fqdn each time.
        
        :param str fqdn_or_rname: If zone_fqdn is provided, this is interpreted
           as a resource name relative to the zone_fqdn, otherwise it is treated
           as the fqdn of a resource.           
        """
        (rname,zonename) = self._identify_names(fqdn_or_rname,zone_fqdn,requireZone=True)
        if self.hasResource(rname,zone_fqdn=zonename):
            zone=self._getZone(zonename)
            zone['resources']=[r for r in zone['resources'] if r['name']!=rname]
            self._save_config()
    
            



