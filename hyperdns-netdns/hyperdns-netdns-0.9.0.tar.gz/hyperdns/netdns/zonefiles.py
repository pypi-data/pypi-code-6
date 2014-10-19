import io,json
import dns.zone
import ipaddress
import hyperdns.netdns
from hyperdns.netdns import dotify,undotify,RecordType,RecordPool,RecordClass,RecordSpec,InvalidZoneFQDNException,IncorrectlyQualifiedResourceName,MalformedJsonZoneData,CorruptBindFile


class ResourceData(object):
    
    def __init__(self,zone,rname,recpool=None):
        self._zone=zone
        self._localname=undotify(rname)
        self._recpool=recpool
        if self._recpool==None:
            self._recpool=RecordPool()
        
        
    def add(self,spec_or_set):
        self._recpool.add(spec_or_set)
        
    @property
    def records(self):
        return self._recpool.records
        
    @property
    def zone(self):
        """Read only access to owning zone"""
        return self._zone
        
    @property
    def name(self):
        """Read only access to resource name"""
        return self._localname
        
    @property
    def fqdn(self):
        """Read only access to fqdn of this resource"""
        return "%s.%s" % (self.name,self.zone.fqdn)

    def _as_dict(self):
        return {
            "name":self._localname,
            "records":[rec.json for rec in self._recpool.records]
        }
        
    def _as_json(self):
        data=self._as_dict()
        return json.dumps(data,indent=4,sort_keys=True)
        

        
class ZoneData(object):

    def __init__(self,fqdn=None,source=None):
        """Create a zone model
        """
        self._nameservers=set()
        self._soa=None
        self._fqdn=fqdn
        self._resources={}
        self._source=source

    def _local_rname(self,rname):
        """Return the local name of a resource, checking to see if it is part
        of this zone, and trimming it if not.  Raise an exception if the resource
        is fully qualified and part of another zone.
        """
        if rname.endswith("."):
            # this is fully qualified, check that zones match, and if
            # not then automatically bong this
            if not rname.endswith(self.fqdn):
                raise IncorrectlyQualifiedResourceName(rname,self.fqdn)
                
            # otherwise just trim rname to be the local name, sans zone
            rname=rname[:-len(self.fqdn)]
        return rname

    def _full_rname_or_addr(self,name):
        """Return a fully qualified name in this zone if the name is local"""
        try:
            ipaddress.ip_address(name)
            return name
        except:
            pass
        if name.endswith("."):
            return name
        return "%s.%s" % (self._local_rname(name),self.fqdn)
        
    def hasResource(self,rname):
        """return true if this resoruce or resource name is part of this
        zone.
        """
        if isinstance(rname,ResourceData):
            rname=rname.name
            
        if rname.endswith("."):
            # this is fully qualified, check that zones match, and if
            # not then automatically bong this
            if not rname.endswith(self.fqdn):
                return False
                        
        return self._resources.get(self._local_rname(rname))!=None
        

    def addResourceData(self,rname,spec_or_set):
        """rname can be either local (no trailing dot), or fully
        qualified.  If it is fully qualified, then the suffix of the
        name must match the fqdn of the zone.
        """
        
        if rname.endswith("."):
            # this is fully qualified, check that zones match
            if not rname.endswith(self.fqdn):
                raise IncorrectZoneScope(rname)
        
        rd=self._resources.get(self._local_rname(rname))
        if rd==None:
            rd=ResourceData(self,rname)
            self._resources[rname]=rd
        
        if spec_or_set.rdtype==RecordType.NS:
            if isinstance(spec_or_set,RecordSpec):
                self._nameservers.add(self._full_rname_or_addr(spec_or_set.rdata))
            else:
                for rec in spec_or_set:
                    self._nameservers.add(self._full_rname_or_addr(rec.rdata))
        elif spec_or_set.rdtype==RecordType.SOA:
            self._soa=spec_or_set
            self._nameservers.add(self._full_rname_or_addr(self.soa_nameserver_fqdn))
            
        rd.add(spec_or_set)
        
    def addResource(self,resource):
        return self.addResourceData(resource.name,resource)
        
    @classmethod
    def is_valid_zone_fqdn(cls,zone_fqdn):
        if zone_fqdn==None:
            return False
        return zone_fqdn.endswith(".")       


    @classmethod
    def fromDict(cls,jsondata):
        zd=ZoneData()
        
        zd._fqdn=jsondata.get('fqdn')
        if zd._fqdn==None:
            zd._fqdn=jsondata.get('name')
        if not cls.is_valid_zone_fqdn(zd._fqdn):
            raise InvalidZoneFQDNException(zd._fqdn)
            
        for resource in jsondata.get('resources'):
            for r in resource['records']:
                zd.addResourceData(resource['name'],RecordSpec(json=r))
        return zd
        
    @classmethod
    def fromJsonText(cls,jsontext):
        """Load a ZoneData object from json as a text
        """
        try:
            jsondata=json.loads(jsontext)
        except Exception as E:
            raise MalformedJsonZoneData(E)
        return cls.fromDict(jsondata)
        
        
    @classmethod
    def fromZonefileText(cls,zone_text):
        """Generate a ZoneData instance from the text of a BIND zone file.
        """
        try:
            pyzone = dns.zone.from_text(zone_text,check_origin=False);
        except dns.zone.UnknownOrigin:
            raise CorruptBindFile()
            
        zonename=dotify(pyzone.origin.to_text()).lower()
        zd=ZoneData()          
        zd._fqdn=zonename
        zd._resources={}

        resources=zd._resources
        for key, r in pyzone.items():            
            for rdataset in r:
                rdtype = rdataset.rdtype
                rdclass = rdataset.rdclass
                ttl = rdataset.ttl
                for record in rdataset:
                    rdata=record.to_text()
                    spec=RecordSpec(rdtype=rdtype,rdclass=rdclass,ttl=ttl,rdata=rdata)
                    zd.addResourceData(key.to_unicode(),spec)
                

        return zd
        

    @property
    def zonefile(self):
        """Generate a zonefile
        """
        origin=dns.name.Name(self.fqdn.split('.')[:-1])
        pyzone = dns.zone.Zone(origin)
    
        for resource in self.resources:
            for r in resource.records:
                #rdtype = dns.rdatatype.from_text(r['type'])
                rdtype = r['type'] #rd_type_as_int(r['type'])
                #stuff = ' '.join([str(x) for x in r[]])
                rdata = dns.rdata.from_text(RecordClass.IN, rdtype, r['rdata'])
                n = pyzone.get_rdataset(resource.name, rdtype, create=True)
                n.ttl=r['ttl']
                n.add(rdata)
    
        output=io.StringIO()
        pyzone.to_file(output,sorted=True)
        return "$ORIGIN %s\n%s" % (self.fqdn,output.getvalue())

    # zone fqdn, including trailinig dot, lowercased, and validated against
    # known tld entries
    @property
    def fqdn(self):
        """Return the zone fqdn, including the trailing dot, lowercased, and
        validated against all known TLD entries (see .tld file)
        """
        return self._fqdn

    @property
    def nameservers(self):
        """Return the IP address of the NS records"""
        for ns in self._nameservers:
            yield ns
    
    @property
    def soa(self):
        """The RecordSpec for the soa record - this is where you find the soa TTL
        and soa class entries
        """
        return self._soa

    @property
    def soa_nameserver_is_internal(self):
        """Returns true if the nameserver listed in the SOA record is internal
        to the zone."""
        return self.soa_nameserver_fqdn.endswith(self.fqdn)
        
    @property
    def soa_nameserver_fqdn(self):
        """This is the Nameserver from the SOA record.  This is a fqdn, which may
        or may not be within this zone - see soa_nameserver_is_internal() to check
        if this nameserver is internal
        """
        if self._soa==None:
            return None
        return self._soa.soa_nameserver_fqdn
        
    @property
    def soa_email(self):
        """This is the soa email address as an email address.  SOA email addressess have
        the @ symbol replaced by a dot, which makes for some very confusing parsing.  This
        provides the soa email as an actual email address, with all parsing and substitution
        completed.
        """
        if self._soa==None:
            return None
        return self._soa.soa_email
        
    @property
    def soa_serial(self):
        """Serial number - 2004123001 - This is a sort of a revision numbering system to show the changes made to the DNS Zone. This number has to increment , whenever any change is made to the Zone file. The standard convention is to use the date of update YYYYMMDDnn, where nn is a revision number in case more than one updates are done in a day. So if the first update done today would be 2005301200 and second update would be 2005301201.
        """
        if self._soa==None:
            return None
        return self._soa.soa_serial
        
    @property
    def soa_refresh(self):
        """Refresh - 86000 - This is time(in seconds) when the slave DNS server will refresh from the master. This value represents how often a secondary will poll the primary server to see if the serial number for the zone has increased (so it knows to request a new copy of the data for the zone). It can be written as ``23h88M'' indicating 23 hours and 88 minutes. If you have a regular Internet server, you can keep it between 6 to 24 hours.
        """
        if self._soa==None:
            return None
        return self._soa.soa_refresh
        
    @property
    def soa_retry(self):
        """Retry - 7200 - Now assume that a slave tried to contact the master server and failed to contact it because it was down. The Retry value (time in seconds) will tell it when to get back. This value is not very important and can be a fraction of the refresh value.
        """
        if self._soa==None:
            return None
        return self._soa.soa_retry
        
    @property
    def soa_expiry(self):
        """Expiry - 1209600 - This is the time (in seconds) that a slave server will keep a cached zone file as valid, if it can't contact the primary server. If this value were set to say 2 weeks ( in seconds), what it means is that a slave would still be able to give out domain information from its cached zone file for 2 weeks, without anyone knowing the difference. The recommended value is between 2 to 4 weeks.
        """
        if self._soa==None:
            return None
        return self._soa.soa_expire
        
    @property
    def soa_minimum(self):
        """Minimum - 600 - This is the default time(in seconds) that the slave servers should cache the Zone file. This is the most important time field in the SOA Record. If your DNS information keeps changing, keep it down to a day or less. Otherwise if your DNS record doesn't change regularly, step it up between 1 to 5 days. The benefit of keeping this value high, is that your website speeds increase drastically as a result of reduced lookups. Caching servers around the globe would cache your records and this improves site performance.
        """
        if self._soa==None:
            return None
        return self._soa.soa_minttl

    
    def has_resource(self,rname):
        """Return true if this zone has the resource
        """
        return self._resources.get(rname)!=None
        
    @property
    def resources(self):
        """Generator over resources associated with this zone"""
        for r in self._resources.values():
            yield r

    def __getitem__(self,rname):
        return self._resources.get(rname)

    def __delitem__(self,rname):
        raise Exception("Not implemeneted correctly")
        if self._resources.get(rname)!=None:
            del self._resources[rname]

    def __setitem__(self,rname,value):
        if not isinstance(value,ResourceData):
            raise Exception("Zones can only contain resources")
            
        self._resources[rname]=value
        
    def _as_dict(self):
        """return the zone data as a dict"""
        return {
            'fqdn':self._fqdn,
            'resources':[x._as_dict() for x in self._resources.values()]
        }
        
    def _as_json(self):
        """Return the zone data as json text"""
        data=self._as_dict()
        return json.dumps(data,sort_keys=True,indent=4)



