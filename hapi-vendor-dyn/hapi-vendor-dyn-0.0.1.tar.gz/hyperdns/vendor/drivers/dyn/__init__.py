import json
import datetime
from http.client import HTTPSConnection
from hyperdns.netdns import (
    dotify,undotify,splitHostFqdn,
    RecordType,RecordClass,RecordSpec
    )
from hyperdns.vendor.core import (
    HTTPDriver,
    MissingRequiredConfigurationException,
    CommunicationsFailureException,
    CreateRecordException,
    DeleteRecordException,
    ZoneCreationException,
    ZoneDeletionException,
    RESTResourceeDisappearanceException,
    ResourceDeletionFailure,
    CanNotUpdateSOARecordsException,
    UnsupportedRecordTypeException 
)

    
class HyperDNSDriver(HTTPDriver):
    """
    """

    vkey = 'dyn'
    """The internal DNS service identifier for DynECT Managed DNS"""
    
    name = 'Dynect DNS'
    """Display name for this driver on the UI"""
    
    info = {
        'vendor':'Dyn Inc.',
        'service':'DynECT Managed DNS',
        'description':'Dyn\'s DynECT Managed DNS Service',
        'settings':['customer_name','user_name','password','host','port'],
        'angular':{
            'customer_name': {
                'label':'DynECT Customer Name',
                'type':'text',
                'placeholder':"Customer Name"
            },
            'user_name': {
                'label':'DynECT User Name',
                'type':'text',
                'placeholder':"User Name"
            },
            'password': {
                'label':'DynECT Password',
                'type':'password',
                'placeholder':"Password"
            },
            'host': {
                'label':'DynECT API Host',
                'type':'text',
                'placeholder':"API Endpoint - try api.dynect.net"
            },
            'port': {
                'label':'DynECT API Port',
                'type':'text',
                'placeholder':"API Endpoint - try 443"
            }
            
        }
    }
    """Definition of vendor for UI"""

    ZONE_MAP_REFRESH_THRESHOLD=300
    
    def __init__(self,settings,immediateLogin=True):
        """Create a new DynECT driver, optionally logging in immediately
        
        REST API documentation is at from https://help.dynect.net/rest-resources/
        
        The settings object should contain the following fields::
        
            {
                'customer_name': -> The DynECT Customer Name
                'user_name':     -> The DynECT User Name
                'password':      -> The DynECT password
                'host':          -> should be api.dynect.net
                'port':          -> should be 443
            }
        
        
        
        host and port, if they are missing, will default to api.dynect.net
        and 443.  HTTPDriver handles the host and port settings, and will
        throw a MissingRequiredConfigurationException if we can not find
        a value.
        
        :param settings: JSON settings
        :param immediateLogin: whether or not to delay login
        
        :raises MissingRequiredConfigurationException: if the customer_name,
           username, or password are missing
        """
        settings.setdefault('host','api.dynect.net')
        settings.setdefault('port',443)

        # obtain mandatory settings
        self.customer=settings.get('customer_name')
        if self.customer==None:
            raise MissingRequiredConfigurationException('Customer Name')

        self.username=settings.get('user_name')
        if self.username==None:
            raise MissingRequiredConfigurationException('Username')

        self.password=settings.get('password')
        if self.password==None:
            raise MissingRequiredConfigurationException('Password')
                    
        # optional overrides of defaults for dynect
        #self.api_version=settings.get('api_version','current')
        self.api_version='current'

        super(HyperDNSDriver,self).__init__(settings,immediateLogin)


    def login(self):
        """Execute a POST to /REST/Session using the security credentials
        from settings and record the Auth-Token
        """
        if self.loggedIn:
            return True
        
        # Build headers
        self.headers['API-Version']=self.api_version

        success,response = self._execute('/REST/Session', 'POST', {
            'customer_name':self.customer,
            'user_name':self.username,
            'password':self.password
        })
        if not success:
            return False

        self.headers['Auth-Token'] = response['data']['token']                    
        self.loggedIn=True
        return True
        

    def logout(self):
        """Execute a DELETE against /REST/Session and clear out our
        memory of the Auth-Token
        """
        if not self.loggedIn:
            # Log out, to be polite
            self._execute('/REST/Session', 'DELETE')
            self.conn=None
            del self.headers['Auth-Token']
            self.loggedIn=False

    def _publish(self,zone):
        """Execute a PUT against /REST/<zone_fqdn>&publish
        
        :param zone: the Dyn internal zone structure
        :returns: True if the publication succeded, false otherwise
        :rtype: boolean
        """
        url='/REST/Zone/%s' % zone['zone']
        (success,result)=self._execute(url,'PUT',request_data={
            'publish':True
        })
        if success:
            return True
        return result
        
    def _resource_uri(self,uri,rname,zone):
        """Return the uri of a specific resource
        
        :param uri: The resource type to access
        :type uri: str
        :param rname: The local resource name or @
        :type rname: str
        :param zone: The Dyn Zone datastructure
        :type zone: JSON returned by _getZone
        :returns: A uri of the form /base/zone/fqdn
        """
        if rname=='@':
            fqdn=zone['zone']
        else:
            fqdn="%s.%s" % (rname,zone['zone'])
        uri='/REST/%s/%s/%s' % (uri,zone['zone'],fqdn)
        return uri

    def _grab(self,uri):
        """ simple get - Dyn returns answers of the form below - several
        of the fields are job control related, the the core data is in the
        'data' field, so we strip that out
        
        Example::
        
            {   
            'job_id': 1022847901,
            'msgs': [{
                'LVL': 'INFO',
                'INFO': 'get: Found the record',
                'ERR_CD': None,
                'SOURCE': 'API-B'}],
            'data': {'zone': 'ubiquibot.com',
                    'fqdn': 'ubiquibot.com',
                    'record_type': 'SOA',
                    'serial_style': 'increment',
                    'record_id': 116868001,
                    'rdata': {'rname': 'eric@dnsmaster.io.',
                        'minimum': 1800,
                        'retry': 600,
                        'mname': 'ns1.p27.dynect.net.',
                        'refresh': 3600,
                        'expire': 604800,
                        'serial': 0},
                    'ttl': 800},
             'status': 'success'
             }
        """
        res=super(HyperDNSDriver,self)._grab(uri,exceptionIfNotFound=False)
        if res==None:
            return None
        return res['data']

    
    def perform_scanZoneList(self):
        """Obtain a list of all of the zones, skipping the collection of
        zone data.   Dyn returns lists of URIs to zone resources - these are
        then queried to get the zone result.  This process tends to take
        a long time.
        
        :raises RESTResourceeDisappearanceException: if the zone can not be read
          even though the result of the zone list query listed it as a resource. 
        """
        for resource in self._grab('/REST/Zone'):
            # resource is a URI for the zone, we have to request each one
            # to get the zone info
            zone=self._grab(resource)
            if zone==None:
                raise RESTResourceeDisappearanceException('Zone appears to have disappeared')
            zonename=dotify(zone['zone'])
            self.zone_map[zonename]=zone


    def _unpack_record(self,record):
        """Convert a Dyn record return structure into a RecordSpec.  This
        is complicated by the fact that the rdata field name depends upon
        the record type.  For examples, both A and AAAA record have their
        rdata stored under record['rdata']['address'] while an NS record
        has it's information stored under record['rdata']['nsdname'].
        
        This function normalizes Dyn responses into RecordSpec elements.
        
        Example Dyn return::
        
            {'record_id': 116868001, 'fqdn': 'ubiquibot.com', 'rdata': {'minimum': 1800, 'serial': 0, 'retry': 600, 'rname': 'eric@dnsmaster.io.', 'mname': 'ns1.p27.dynect.net.', 'expire': 604800, 'refresh': 3600}, 'ttl': 800, 'record_type': 'SOA', 'zone': 'ubiquibot.com', 'serial_style': 'increment'}
            {'record_id': 116868002, 'service_class': 'Primary', 'fqdn': 'ubiquibot.com', 'rdata': {'nsdname': 'ns1.p27.dynect.net.'}, 'ttl': 86400, 'record_type': 'NS', 'zone': 'ubiquibot.com'}
            {'record_id': 116868003, 'service_class': 'Primary', 'fqdn': 'ubiquibot.com', 'rdata': {'nsdname': 'ns2.p27.dynect.net.'}, 'ttl': 86400, 'record_type': 'NS', 'zone': 'ubiquibot.com'}
            {'record_id': 116868004, 'service_class': 'Primary', 'fqdn': 'ubiquibot.com', 'rdata': {'nsdname': 'ns3.p27.dynect.net.'}, 'ttl': 86400, 'record_type': 'NS', 'zone': 'ubiquibot.com'}
            {'record_id': 116868005, 'service_class': 'Primary', 'fqdn': 'ubiquibot.com', 'rdata': {'nsdname': 'ns4.p27.dynect.net.'}, 'ttl': 86400, 'record_type': 'NS', 'zone': 'ubiquibot.com'}
        
        :param record: JSON structure as in the examples
        :rtype: RecordSpec
        :returns: The RecordSpec corresponding to the Dyn record.
        """
        fqdn=dotify(record['fqdn'])
        if fqdn==record['zone']:
            rname='@'
        else:
            (rname,z)=splitHostFqdn(fqdn)
        
        rdtype=RecordType.as_type(record['record_type'])
        ttl=record['ttl']
        rdclass=RecordClass.IN
        if rdtype==RecordType.A:
            rdata=record['rdata']['address']
        elif rdtype==RecordType.AAAA:
            rdata=record['rdata']['address']
        elif rdtype==RecordType.CNAME:
            rdata=record['rdata']['cname']
        elif rdtype==RecordType.NS:
            rdata=record['rdata']['nsdname']
        elif rdtype==RecordType.TXT:
            rdata=record['rdata']['txtdata']
        elif rdtype==RecordType.MX:
            rdata="%s %s" % (
                record['rdata']['exchange'],
                record['rdata']['preference']
                )
        elif rdtype==RecordType.SOA:
            #{'expire': 604800, 'serial': 1, 'refresh': 3600, 'retry': 600, 'mname': 'ns1.p27.dynect.net.', 'minimum': 1800, 'rname': 'eric@dnsmaster.io.'}
            data=record['rdata']
            data['email']=data['rname'].replace("@",".")
            rdata="%(mname)s %(email)s %(serial)s %(refresh)s %(retry)s %(expire)s %(minimum)s" % data
        else:
            self.log.debug("Unknown Record Structure:%s" % record)
            raise UnsupportedRecordTypeException(rdtype,"unpacking")
        return RecordSpec(json={
            'class':rdclass,
            'type':rdtype,
            'rdata':rdata,
            'ttl':ttl
            })
            
    def perform_scanZone(self,zone):
        """Scan a zone and return the zone description as JSON.  During the
        zone translation, records with a resource fqdn equivalent to the zone
        name will be replaced by `@.<zone_fqdn`
        
        :param zone zone: the internal
        :returns: description of zone, nameservers, and all resources
        :rtype: JSON definition of zone - see interface for format
        
        """
        rmap={}
        zonename=zone['zone']
        zone_fqdn=dotify(zonename)
        uri='/REST/AllRecord/%s/' % zonename
        for record in [self._grab(r) for r in self._grab(uri)]:
            (rname,zn)=self._identify_names(record['fqdn'],zone_fqdn)
            resource=rmap.setdefault(rname,{
                'name':rname,
                'records':[]
            })
            resource['records'].append(self._unpack_record(record))
            
        resources=list(rmap.values())
        return {
            'name':zone_fqdn,
            'resources':resources,
            'source':{
                    'type':'vendor',
                    'vendor':self.vkey
                    }
            }

    def perform_scanResource(self,rname,zone):
        """Scan the resource, returning a JSON element recording all of the
        records in the zone.
        
        See the interface docs for details about the return type
        
        :param str rname: the local name of the resource, such as www, or
          ftp, without the trailing zone
        :param zone zone: the DynEct zone structure
                """
        resource={
            'name':rname,'records':[]
            }
        uri=self._resource_uri('ANYRecord',rname,zone)
        result=self._grab(uri)
        if result==None:
            raise Exception("Resource not found")
        for record_uri in result:
            record=self._grab(record_uri)
            resource['records'].append(self._unpack_record(record))
        return resource
        
    def perform_hasResource(self,rname,zone):
        """Return True if there is at least one matching RRset
        
        :param rname: The local name of the resource
        :param zone: The Dyn structured returned by _getZone()    
        :returns: True if there is at least one matching RRSet
        :rtype: boolean  
        """
        uri=self._resource_uri('ANYRecord',rname,zone)
        result=self._grab(uri)
        if result==None:
            return False
        return True
        
    def perform_deleteResource(self,rname,zone):
        """Entirely delete a resource matching a given name by issuing
        a DELETE against /REST/Node/<zone_fqd>/<rname>
          
        :param rname: The local name of the resource
        :param zone: The Dyn structured returned by _getZone()
        
        :raises ResourceDeletionFailure: if we can not delete the resource.   
        """
        uri=self._resource_uri('Node',rname,zone)
        (success,result)=self._execute(uri, 'DELETE',{})
        if not success:
            raise ResourceDeletionFailure(result.status_code,result.content,
                        "Failed to delete '%s.%s'" % zone['zone'])

    def perform_createZone(self,zone_fqdn,default_ttl,admin_email):
        """Create the zone if the zone does not exist.

        
        :param zone_fqdn: the fully qualified zone name
        :param default_ttl: the default ttl for the zone
        :param admin_email: an email address for the zone contact in the SOA record
        :raises ZoneCreationException: if the attempt to create the zone fails
        :rtype: None
        :returns: None
        
        """
        zonename=undotify(zone_fqdn)
        arguments={
            "rname":admin_email,
            "serial_style":"increment",
            "ttl":int(default_ttl)
            }
        (success,result) = self._execute('/REST/Zone/%s/' % (zonename),
                                 'POST',arguments)
        if not success:
            raise ZoneCreationException(result.status_code,result.content,
                    "Unable to create zone '%s'" % zonename)
        
    def perform_deleteZone(self,zone):
        """Delete this zone if it exists by issuing a DELETE to
        /REST/Zone/<zone_fqdn>.
        
        :param zone: The Dyn response zone structure
        :raises ZoneDeletionFailure: if the zone deletion fails
        :rtype: None
        :returns: None
        """
        zonename=zone['zone']
        (success,resp)=self._execute('/REST/Zone/%s/' % (zonename), 'DELETE',{})
        if not success:
            raise ZoneDeletionFailure(resp.status_code,resp.content,
                    "Unable to delete zone '%s'" % zonename)

    def perform_createRecord(self,rname,zone,spec,pool,addrec=False):
        """Create a record on DYN.  Dyn's model uses a unique communication
        structure for each record type, but there is standardization around
        the url
        
        :param rname: The name of the resource within the zone
        :type rname: str
        :param zone: The Dyn zone specification for the zone
        :type zone: dict
        :param spec: The RecordSpec of the record to be created
        :type spec: RecordSpec
        :returns: nothing
        :raises CreateRecordException: if there was an error POSTing the
        create request or publishing the change set.
        """
        url=self._resource_uri(spec.rdtype.name+'Record',rname,zone)
        record={
            'ttl':spec.ttl,
            'rdata':{}
        }
        
        if spec.rdtype==RecordType.A:
            record['rdata']['address']=spec.rdata
        elif spec.rdtype==RecordType.AAAA:
            record['rdata']['address']=spec.rdata
        elif spec.rdtype==RecordType.CNAME:
            record['rdata']['cname']=spec.rdata
        elif spec.rdtype==RecordType.NS:
            record['rdata']['nsdname']=spec.rdata
        elif spec.rdtype==RecordType.MX:
            record['rdata']={
                'exchange':spec.mx_exchange,
                'preference':spec.mx_priority
            }
        elif spec.rdtype==RecordType.TXT:
            record['rdata']['txtdata']=spec.rdata
        elif spec.rdtype==RecordType.SOA:
            raise CanNotUpdateSOARecordsException()
        else:
            raise UnsupportedRecordTypeException(spec.rdtype,
                        "Can not create records of this type:")
        
        (success,resp)=self._execute(url,'POST',record)
        if not success:
            raise CreateRecordException(resp.status_code,resp.content,"Pre-commit record creation failure")
        
        resp=self._publish(zone)
        if resp!=True:
            raise CreateRecordException(resp.status_code,resp.content,"Commit failure")
            
    
    def _getMatchingRecord(self,rname,zone,spec,matchTTL):
        """Locate a specific record, optionally ignoring the TTL field
        and matching only on type and rdata.
        
        We first get the record result.  The result['data'] field contains
        a set of URLs which identify the resources.  We then get those
        resources, one at a time, looking to see if we can find a record
        match.  If we find one we return it.
        
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
        :raises CommunicationException: if we get an unexpected result.
        """
        url=self._resource_uri(spec.rdtype.name+'Record',rname,zone)
        (success,result)=self._execute(url,'GET')
        if not success:
            raise CommunicationException("Unable to check for existing record")
        if result==None:
            return None
        
        for record_url in result['data']:
            (success,result)=self._execute(record_url,'GET')
            if not success:
                raise CommunicationException("Unable to check for existing record")
            
            rec=RecordSpec(json=self._unpack_record(result['data']))
            if rec.match(spec,matchTTL=matchTTL):
                return result
                
        return None
        
    def perform_deleteRecord(self,rname,zone,record):
        """Delete a specific record.
        
        Example Dyn record::
            {'data': {'rdata': {'address': '1.2.3.4'}, 'fqdn': 'testhost.xtestzone.com', 'record_id': 129137183, 'ttl': 123, 'zone': 'xtestzone.com', 'record_type': 'A'}, 'msgs': [{'LVL': 'INFO', 'SOURCE': 'API-B', 'INFO': 'get: Found the record', 'ERR_CD': None}], 'status': 'success', 'job_id': 1187589339}
        
        :param rname: the local resource name relative to the zone
        :param zone: Dyn json record for zone
        :param record: Dyn record representation
        """
        data=record['data']
        record_id=data['record_id']
        rdtype=data['record_type']
        url=self._resource_uri(rdtype+'Record',rname,zone)
        url="%s/%s" % (url,record_id)
        
        (success,resp)=self._execute(url,'DELETE',record)
        if not success:
            raise DeleteRecordException(resp.status_code,resp.content,"Pre-commit record deletion failure")
        
        resp=self._publish(zone)
        if resp!=True:
            raise DeleteRecordException(resp.status_code,resp.content,"Commit failure")
        


        
#