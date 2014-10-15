import logging
import json
import route53
import time
from hyperdns.netdns import (
    dotify,undotify,splitHostFqdn,RecordType,RecordClass,RecordSpec,ZoneData,ResourceData
    )
from hyperdns.netdns import (
    undotify,
    splitHostFqdn,
    RecordSpec,RecordType
)
from hyperdns.vendor.core import (
    BaseDriver,
    MissingRequiredConfigurationException,
    CommunicationsFailureException,
    CreateRecordException,
    DeleteRecordException,
    ZoneCreationException,
    ZoneDeletionException
)
class HyperDNSDriver(BaseDriver):
    """HyperDNSDriver for Amazon's Route 53 Managed DNS Service.  Our driver
    is a wrapper around the python-route53 package - the documentation of
    which can be found here: https://python-route53.readthedocs.org/en/latest/
       
    Note: The driver caches the route 53 HostedZone object for re-use,
    refreshing the zone list as controlled by a threshold setting.
    """
    vkey='r53'
    """This is the identifier used to reference this driver in the command
    line tools"""
    
    name='Route 53'
    """Full display name of the service"""
    
    info={
        'vendor':'Amazon',
        'service':'Route 53',
        'description':'Amazon\'s Route53 Managed DNS Service',
        'settings':['access_key_id','secret_access_key'],
        'angular':{
            'access_key_id':{
                'placeholder':'Your Amazon AWS Access Key Id',
                'type':'text',
                'label':"Access Key"
            },
            'secret_access_key':{
                'placeholder':'Your Amazon AWS Secret Key',
                'type':'password',
                'label':'Secret Key'
                
            }   
        }    
    }
    """See the hapi-vendor-toolkit documentation for information about this
    field.
    """            
    def __init__(self,settings,immediateLogin=True):
        """Create a new Route 53 Driver using provided settings and optionally
        logging in immediately.   Logging in actually performs a scan of
        the zonelist - without that action the connection is not fully established
        and we can not detect trouble.
        
        Settings should contain::
        
            {
                'access_key_id':
                'secret_access_key':
            }
        
        :param settings: driver configuration
        :type settings: json
        :param immediageLogin: When True automatically login as part
        of construction.
        :raises MissingRequiredConfigurationException: when one of the required
        parameters is absent.
        
        """
        self.loggedIn=False
        
        self.aws_access_key_id=settings.get('access_key_id')
        if self.aws_access_key_id==None:
            raise MissingRequiredConfigurationException('access_key_id')
            
        self.aws_secret_access_key=settings.get('secret_access_key')
        if self.aws_secret_access_key==None:
            raise MissingRequiredConfigurationException('secret_access_key')

        super(HyperDNSDriver,self).__init__(settings,immediateLogin)
            
    def login(self):
        """Log in and popuplate the zone_id map.  If no action is taken
        during login then you can't really tell if the connection was made.
        If an exception is thrown, it is logged as an error using the
        configured logger.
        """
        if self.loggedIn:
            return True
        try:
            self.conn=route53.connect(
                self.aws_access_key_id,
                self.aws_secret_access_key
                )
            # this actually causes an action to be taken against the
            # connection - and without this we can not determine if
            # the authentication credentials actually work
            self._scan_zonelist_if_needed()
            self.loggedIn=True
            return True
        except Exception as E:
            self.loggedIn=False
            self.log.error(E)
            raise
            return False

    def logout(self):
        """Terminate the connection
        """
        self.conn=None
        self.loggedIn=False


    def _attach_rr_set_to_resource(self,resource,rr_set):
        """Attach ResourceRecord set to resource
        """
        for rdata in rr_set.records:
            resource['records'].append(RecordSpec(json={
                'ttl':rr_set.ttl,
                'rdata':rdata,
                'type':RecordType.as_type(rr_set.rrset_type),
                'class':RecordClass.IN
            }))

    def _getZone(self,zone_fqdn):
        """Return the HostedZone for a given zone_fqdn
        
        Route53 returns zones with the following fields::
    
            'caller_reference',
            'comment',
            'connection',
            'create_a_record',
            'create_aaaa_record',
            'create_cname_record',
            'create_mx_record',
            'create_ns_record',
            'create_ptr_record',
            'create_spf_record',
            'create_srv_record',
            'create_txt_record',
            'delete',
            'id',
            'name',
            'nameservers',
            'record_sets',
            'resource_record_set_count'
    
        
        :param str zone_fqdn: the fully qualified name of the zone
          to be located
        :returns: None if the zone is not found, otherwise the Route 53
        HostedZone object corresponding to zone_fqdn
        
        """
        zone=self.zone_map.get(zone_fqdn)
        if zone==None:
            zone=self.conn.get_hosted_zone_by_id(zone_fqdn)
            if zone!=None:
                self.zone_map[zone.name]=zone
        return zone

    def _rrsets(self,rname,zone):
        """generator over RRSets matching a specific resource
        
        :param str rname: the local name of the resource, such as www, or
          ftp, without the trailing zone
        :param zone zone: the Route 53 hosted zone object
        
        """
        for rr_set in zone.record_sets:
            if rname!='@':
                fqdn='%s.%s' % (rname,zone.name)
            else:
                fqdn=zone.name
            if rr_set.name==fqdn:
                yield rr_set


    def perform_scanZoneList(self):
        """Obtain a list of all of the hosted zone records.
        
        Example response::
        
            {
            'caller_reference': '45d74235-81b8-4497-a2ea-219e7861f662',
            '_is_deleted': False,
            'resource_record_set_count': 6,
            'connection': <route53.connection.Route53Connection object at 0x10ada4b00>,
            'comment': None,
            'name': 'ubiquibot.com.',
            '_nameservers': [],
            'id': 'Z2AURFDVVKVFQE'
            }
        """

        r53_zones=self.conn.list_hosted_zones()
        if r53_zones!=None:
            for zone in r53_zones:
                self.zone_map[zone.name]=zone

        
    def perform_scanZone(self,zone):
        """Scan the zone and return zone description
        
        :param zone zone: the internal
        :returns: description of zone, nameservers, and all resources
        :rtype: JSON definition of zone - see interface for format
        """
        resourceMap={}
        for rr_set in zone.record_sets:
            (rname,zonename_check)=splitHostFqdn(rr_set.name)
            if rname==None:
                rname='@'
                
            resource=resourceMap.setdefault(rname,{
                'name':rname,'records':[]
                })
            
            self._attach_rr_set_to_resource(resource,rr_set)
            
        result={
            'name':dotify(zone.name),
            'resources':list(resourceMap.values()),
            'source':{
                    'type':'vendor',
                    'vendor':self.vkey
                    }
            }
        return result


    def perform_createZone(self,zone_fqdn,default_ttl,admin_email):
        """we are ignoring the admin_email, which is sometimes required for
        the SOA - it is not here because that information is attached to the
        account associated with the keys
        """
        (zone,info)=self.conn.create_hosted_zone(zone_fqdn)
        self.zone_map[zone_fqdn]=zone

    def perform_deleteZone(self,zone):
        """Execute the deletion
        
        :param zone zone: the Route53 Hosted Zone object for the zone
        """
        try:
            result=zone.delete(force=True)
            del self.zone_map[zone.name]
        except AttributeError as E:
            print(zone)
            raise Exception('deleteFailed: Zone is probably corrupt')
            

    def perform_scanResource(self,rname,zone):
        """Scan the resource
        
        :param str rname: the local name of the resource, such as www, or
          ftp, without the trailing zone
        :param zone zone: the vendor internal zone object
        
        See the interface docs for details about the return type
        """
        resource={
            'name':rname,'records':[]
            }
        fqdn="%s.%s" % (rname,zone.name)
        
        for rr_set in self._rrsets(rname,zone):
            self._attach_rr_set_to_resource(resource,rr_set)
                             
        return resource

    def perform_hasResource(self,rname,zone):
        """Return True if there is at least one matching RRset
        """
        for rr_set in self._rrsets(rname,zone):
            return True
        return False
        
    def perform_deleteResource(self,rname,zone):
        """Delete all RRsets matching the name
        """
        for rr_set in self._rrsets(rname,zone):
            rr_set.delete()
        

    def _getMatchingRecord(self,rname,zone,spec,matchTTL):
        """Locate a specific record, optionally ignoring the TTL field
        and matching only on type and rdata.
        
        Example Return Value::
        
            {'record_id': 116868002,
            'service_class':  Primary',
            'fqdn': 'ubiquibot.com',
            'rdata': {'nsdname': 'ns1.p27.dynect.net.'},
            'ttl': 86400,
            'record_type': 'NS',
            'zone': 'ubiquibot.com'}
        
        :param rname: the local resource name relative to the zone
        :param zone: Dyn json record for zone
        :param spec: RecordSpec to locate
        :param matchTTL: determines whether or not to ignore TTL on match
        :returns: Dyn json record specification 
        :rtype json:
        """
        for rrset in self._rrsets(rname,zone):
            if RecordType.as_str(rrset.rrset_type)==spec.rdtype.name:
                return rrset
                
        return None

    def perform_createRecord(self,rname,zone,spec,pool,addrec=False):
        """Create a specific record.
        
        :param rname: the local resource name for which the record is to be deleted
        :type rname: str
        :param zone: the vendor local data structure representing the zone
        :type zone: vendor specific
        :param spec: RecordSpec to add
        :type spec: RecordSpec
        :param pool: Existing records for resource
        :type pool: RecordPool
        :rtype: None
        
        """
        if rname=='@':
            fqdn=zone.name
        else:
            fqdn="%s.%s" % (rname,zone.name)
        rdata=spec['rdata']
        ttl=spec['ttl']
        if spec.rdtype==RecordType.A:
            zone.create_a_record(fqdn,[rdata],ttl=ttl)
        elif spec.rdtype==RecordType.AAAA:
            zone.create_aaaa_record(fqdn,[rdata],ttl=ttl)
        elif spec.rdtype==RecordType.NS:
            zone.create_ns_record(fqdn,[rdata],ttl=ttl)
        elif spec.rdtype==RecordType.MX:
            zone.create_mx_record(fqdn,[rdata],ttl=ttl)
        elif spec.rdtype==RecordType.PTR:
            zone.create_ptr_record(fqdn,[rdata],ttl=ttl)
        elif spec.rdtype==RecordType.SPF:
            zone.create_spf_record(fqdn,[rdata],ttl=ttl)
        elif spec.rdtype==RecordType.SRV:
            zone.create_srv_record(fqdn,[rdata],ttl=ttl)
        elif spec.rdtype==RecordType.TXT:
            zone.create_txt_record(fqdn,[rdata],ttl=ttl)
        elif spec.rdtype==RecordType.CNAME:
            if rdata=='@':
                rdata=zone.name
            zone.create_cname_record(fqdn,[rdata],ttl=ttl)
        else:
            raise Exception('Can not create records of type:%s yet' % spec.rdtype)
            

    def perform_deleteRecord(self,rname,zone,record):
        """Delete a specific record
        """
        record.delete()
