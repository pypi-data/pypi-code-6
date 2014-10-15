"""This class implements a driver for the VENDOR_NAME service.
"""
import json
import datetime
from hyperdns.netdns import (
    dotify,undotify,
    RecordType,
    RecordClass,
    RecordSpec
    )
import requests
from hyperdns.vendor.core import (
    HTTPDriver,
    login_required,
    MissingRequiredConfigurationException,
    CommunicationsFailureException,
    ZoneCreationException,
    ZoneDeletionException
)

        

class HyperDNSDriver(HTTPDriver):
    """
    """

    vkey='ultra'
    """This is the identifier used to reference this driver in the command
    line tools"""
    
    name='Neustar UltraDNS'
    """Full display name of the service"""
    
    info={
        'vendor':'Neustar',
        'service':'UltraDNS',
        'description':'Neustar\'s UltraDNS Managed DNS Service',
        'settings':['endpoint','account_name','username','password'],
        'angular':{
            'endpoint':{
                'placeholder':'Your Neustar API Endpoint',
                'type':'text',
                'label':"API Endpoint"
            },
            'account_name':{
                'placeholder':'Your Neustar Account Name',
                'type':'text',
                'label':"Account Name"
            },
            'username':{
                'placeholder':'Your Neustar Username',
                'type':'text',
                'label':"User Name"
            },
            'password':{
                'placeholder':'Your Neustar Password',
                'type':'password',
                'label':'Password'
                
            }   
        }    
    }
    """See the hapi-vendor-toolkit documentation for information about this
    field.
    """

    def __init__(self,settings,immediateLogin=False):        
        """Create a new UltraDNS Driver
        
        Example Settings::
            {
                'account_name':
                'username':
                'password':
                'endpoint':
            }
        :type settings: json
        :param immediateLogin: When True automatically login as part
        of construction.
        :type immediateLogin: bool
        :raises MissingRequiredConfigurationException: when one of the required
        parameters is absent.
        """
        self.loggedIn=False
        
        self.username=settings.get('username')
        if self.username==None:
            raise MissingRequiredConfigurationException('username')
            
        self.password=settings.get('password')
        if self.password==None:
            raise MissingRequiredConfigurationException('password')
        
        self.account_name=settings.get('account_name')
        if self.account_name==None:
            raise MissingRequiredConfigurationException('account_name')
        
        self.endpoint=settings.get('endpoint')
        if self.endpoint==None:
            raise MissingRequiredConfigurationException('endpoint')
        
        
        while self.endpoint.endswith('/'):
            self.endpoint=self.endpoint[:-1]
        
        self.access_token = ""
        self.refresh_token = ""
        self.loggedIn=False

        self.authUrl="%s/v1/authorization/token" % self.endpoint
        self.headers={}

        settings['host']=""
        settings['port']=443
        super(HyperDNSDriver,self).__init__(settings,immediateLogin)
        self.uriPrefix=self.endpoint
        
    def DEPRECATED_execute(self, uri, method, request_data=None, body=None):
        """Execute a call against Ultra and check for standard responses.  The
        configured endpoint is prepended on the uri and the established authentication
        headers are used.
        
        :param uri: URI relative to endpoint
        :param method: HTTP Method to use
        :param body: data to pass as method body
        :type body: str or dict
        :rtype: tuple
        :returns: status code and message body, if any
        """
        url="%s%s" % (self.endpoint,uri)
        
        self.log.debug("Executing '%s' on %s'" % (method,url))
        if isinstance(body,dict):
            body=json.dumps(body)
        
        r1 = requests.request(method, url, request_data=params, data=body, headers=self.headers)
        # bad access token = status 400,
        # body = {"errorCode":60001,"errorMessage":"invalid_grant:token not found, expired or invalid"}
        if r1.status_code == requests.codes.NO_CONTENT:
            return (True,None)
        json_body = r1.json
        if r1.status_code==requests.codes.OK:
            return (True,json_body)
        if r1.status_code==requests.codes.CREATED:
            return (True,json_body)
            
        self.log.debug("Got bad status code: %s, content=%s" % (r1.status_code,r1.content))
        #print("DATA:",r1.content)
        return (False,r1)
        
    def login(self):
        """
        Authentication
        We need the ability to take in a username and password and get
        an auth token and a refresh token. If any request fails due
        to an invalid auth token, refresh must be automatically invoked, the
        new auth token and refresh token stored, and the request tried again
        with the new auth token.
        """
        r1 = requests.post(self.authUrl,data={
            "grant_type":"password",
            "username":self.username,
            "password":self.password})
        if r1.status_code != requests.codes.OK:
            return False
            
        json_body = r1.json()
        self.access_token = json_body.get(u'accessToken')
        self.refresh_token = json_body.get(u'refreshToken')
        if self.access_token==None or self.refresh_token==None:
            return False
        self.headers={
            "Content-type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer " + self.access_token
            }
        self.loggedIn=True
        return True

    def logout(self):
        self.headers={}
        self.loggedIn=False


    def perform_scanZoneList(self):
        """Obtain a list of all of the zones
        """
        uri = "/v1/accounts/" + self.account_name + "/zones"
        for zone_type in ['PRIMARY']: #,'SECONDARY','ALIAS']:
            (success,result)=self._execute(uri,'GET',request_data={
                'zone_type':zone_type
                })
            if success:
                for zone in result['zones']:
                    self.zone_map[zone['properties']['name']]=zone
    
    def perform_scanZone(self,zone):
        """Scan a zone and return the zone description as JSON.  During the
        zone translation, records with a resource fqdn equivalent to the zone
        name will be replaced by `@.<zone_fqdn`
        
        
        """
        zone_fqdn=zone['properties']['name']
        uri = "/v1/zones/" + zone_fqdn + "/rrsets"
        (success,rrsets)=self._execute(uri,'GET',request_data={"limit":10000})
        rmap={}
        if success:
            for rrset in rrsets['rrSets']:
                rdtype=rrset['rrtype'].split(" ")[0]
                ttl=int(rrset['ttl'])
                (rname,zn)=self._identify_names(rrset['ownerName'],zone_fqdn)
                resource=rmap.setdefault(rname,{
                    'name':rname,
                    'records':[]
                })
                for rdata in rrset['rdata']:
                    resource['records'].append(
                        RecordSpec(rdtype=rdtype,rdata=rdata,ttl=ttl))
        return {
            'name':zone_fqdn,
            'resources':list(rmap.values())
            }
            
    def perform_createZone(self,zone_fqdn,default_ttl,admin_email):
        """Create a zone
        
        :raises Exception: if we can not create the zone
        """
        zone_properties = {
            "name": zone_fqdn,
            "accountName": self.account_name,
            "type": "PRIMARY"
        }
        primary_zone_info = {
            "forceImport": True,
            "createType": "NEW"
        }
        zone_data = {
            "properties": zone_properties,
            "primaryCreateInfo": primary_zone_info
        }
        
        (success,result)=self._execute("/v1/zones", 'POST', body=zone_data)
        if not success:
            raise ZoneCreationException(result.status_code,result.content,
                                'Failed to create zone: %s' % zone_fqdn)
    
    
    def _getZone(self,zone_fqdn):
        #uri = "/v1/zones/" + zone_fqdn + "/rrsets"
        #(success,rrsets)=self._execute(uri,'GET',request_data={})
        uri = "/v1/zones/" + zone_fqdn
        (success,result)=self._execute(uri,'GET',request_data={})
        if not success:
            return None
        return result
        
    def perform_deleteZone(self,zone):
        """Execute the deletion
        
        :param zone zone: the Route53 Hosted Zone object for the zone
        """
        zone_fqdn=zone['properties']['name']
        url="/v1/zones/%s" % zone_fqdn
        (success,result)=self._execute(url, 'DELETE')
        if not success:
            raise ZoneDeletionException(result.status_code,result.content,
                                    'Failed to delete zone: %s' % zone_fqdn)

    def _get_records(self,zone_fqdn,rname,rdtype):
        url='/v1/zones/%s/rrsets/%s/%s' % (zone_fqdn,rdtype,rname)
        
        (success,result)=self._execute(url, 'GET')
        if not success:
            raise CommunicationsFailureException(result.status_code,
                result.content,'Unable to read resource: %s.%s' % (rname,zone_fqdn))
        
        records=[]
        for rrset in result['rrSets']:
            (rdtype,num)=rrset['rrtype'].split(" ")
            ttl=rrset['ttl']
            for rdata in rrset['rdata']:
                records.append(RecordSpec(json={
                    'ttl':ttl,
                    'rdata':rdata,
                    'type':RecordType.as_type(rdtype),
                    'class':RecordClass.IN
                }))
        return records
                
    def perform_scanResource(self,rname,zone):
        """Scan the resource
        
        :param str rname: the local name of the resource, such as www, or
          ftp, without the trailing zone
        :param zone zone: the vendor internal zone object
        
        See the interface docs for details about the return type
        
        Example Return:
            {
                'queryInfo':
                    {'reverse': False, 'limit': 100, 'sort': 'OWNER'},
                'resultInfo': {'offset': 0, 'totalCount': 1, 'returnedCount': 1},
                'rrSets': [
                    {'rrtype': 'CNAME (5)',
                    'rdata':[
                        '88d974e24ad4d6e2a30b.r79.cf1.rackcdn.com.'],
                    'ttl': 2592000,
                    'ownerName': 'rackspace.webrum.com.'}
                    ],
                'zoneName': 'webrum.com.'}
        """
        zone_fqdn=zone['properties']['name']
        records=self._get_records(zone_fqdn,rname,'ANY')                
        resource={
            'name':rname,'records':records
            }
        return resource

    def perform_hasResource(self,rname,zone):
        """Return True if there is at least one matching RRset
        """
        zone_fqdn=zone['properties']['name']
        url='/v1/zones/%s/rrsets/ANY/%s' % (zone_fqdn,rname)
        
        (success,result)=self._execute(url, 'GET')
        if not success:
            return False
        return True
        


    def perform_deleteResource(self,rname,zone):
        """Delete all RRsets matching the name
        """
        zone_fqdn=zone['properties']['name']
        url='/v1/zones/%s/rrsets/ANY/%s' % (zone_fqdn,rname)
        
        (success,result)=self._execute(url, 'DELETE')
        if not success:
            raise Exception('Unable to delete resource: %s.%s' % (rname,zone_fqdn))


    def perform_createRecord(self,rname,zone,spec):
        """Create a record
        POST /zones/{zoneName}/rrsets/{type}/{ownerName}
        
        Required Body:
        {
        zoneName
        ownerName
        title
        version
        rrtype
        ttl
        rdata
        rrsigs
        rrsigs/algorithm
        }
        """
        zone_fqdn=zone['properties']['name']
        post_info={
            #'zoneName':zone_fqdn,
            #'ownerName':rname,
            #'version':1,
            #'rrtype':1, #spec.rdtype,
            'rdata':[spec.rdata],
            'ttl':spec.ttl
        }
        url='/v1/zones/%s/rrsets/%s/%s' % (zone_fqdn,spec.rdtype.value,rname)
        (success,result)=self._execute(url, 'POST',body=post_info)
        if not success:
            raise Exception('Unable to create record: %s.%s rec=%s' % (rname,zone_fqdn,spec))
        

    def perform_deleteRecord(self,rname,zone,spec,matchTTL):
        """Delete a record
        """
        zone_fqdn=zone['properties']['name']
        records=self._get_records(zone_fqdn,rname,spec.rdtype.value)
        newrecs=[]     
        for r in records:
            if r!=spec:
                newrecs.append(r)
        title="default"
        url='/v1/zones/%s/rrsets/%s/%s' % (zone_fqdn,spec.rdtype.value,rname)
        if len(newrecs)==0:
            (success,result)=self._execute(url, 'DELETE')
            if not success:
                raise Exception('Unable to delete record: %s.%s rec=%s' % (rname,zone_fqdn,spec))
        else:
            ttl=newrecs[0].ttl
            post_info={
                'ttl':ttl,
                'rdata':[rec.rdata for rec in newrecs]
            }
            (success,result)=self._execute(url, 'PUT',body=post_info)
            if not success:
                raise Exception('Unable to delete record: %s.%s rec=%s' % (rname,zone_fqdn,spec))
        
        