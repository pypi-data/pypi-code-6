# hyperdns/vendor/core/base.py
#
# Copyright (C) 2014 Eric Welton
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose with or without fee is hereby granted,
# provided that the above copyright notice and this permission notice
# appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND HYPERDNS DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL HYPERDNS BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
# OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#
import logging
import time
from  hyperdns.vendor.core import (
    login_required,
    ProfilePoint,
    HyperDNSDriverInterface,
    ZoneNotFoundException,
    ResourceNotFoundException,
    ZoneAlreadyExistsException,
    TransactionInProgressException,
    TransactionNotInProgressException,
    NotLoggedInException,
    LoginFailureException,
    ImplementationMissingException,
    RecordAlreadyExistsException,
    CommunicationsFailureException
) 
from hyperdns.netdns import (
    dotify,
    splitHostFqdn,
    is_valid_zone_fqdn,
    RecordType,RecordClass,RecordPool,
    CanNotMixARecordsAndCNAMES,
    CanNotMixAAAARecordsAndCNAMES
    )
from .abstract import AbstractDriver
        
class UnsupportedRecordType(Exception):
    def __init__(self,rdtype):
        msg="Currently we do not support manipulation of records of type:%s" % rdtype.name
        super(UnsupportedRecordType,self).__init__(msg)
        
class BaseDriver(AbstractDriver):
    """This utility class is a utility base class for HyperDNS HAPI drivers.
    It adds transaction support, creates a logger, provides utiltiy functions,
    default implementations of common functions, and decorators.

    """
    def __init__(self,settings,immediateLogin=True):
        super(BaseDriver,self).__init__(settings)
        
        self.stats={}
        for point in ['login','logout',
            'scanZone','scanZoneList','hasZone',
            'scanResource','hasResource','deleteResource',
            'createZone','deleteZone',
            'hasRecord','createRecord','deleteRecord'
            ]:
            self.stats[point]=ProfilePoint(point)

        # maintain a zone-id map, and a timestamp to know when to refresh
        # it - this is a mild speedup.
        self.zone_map=None
        self.zone_map_time=None
                
        # process login
        self.loggedIn=False
        if immediateLogin:
            if not self.login():
                raise LoginFailureException()
            self.loggedIn=True                



    ZONE_MAP_REFRESH_THRESHOLD=15
    """Expire the zone id map every 15 seconds."""

    def login(self):
        """Log in to the remote vendor, and return True or False.
        :return: True or False indicating whether login was successful.
        :rtype: boolean
        """
        raise ImplementationMissingException()
    
    def logout(self):
        """Logout from the remote session.
        :return: nothing
        :rtype: None
        """
        raise ImplementationMissingException()

 
    
    def __enter__(self):
        """Allow use in with statements and support automatically logging
        in and logging out.  For example
            
            with driver:
                driver.scanZoneList()
                
        which will automatically call driver.login() and driver.logout()
        """
        self.login()
        return self
        
    def __exit__(self ,type, value, traceback):
        """Allow use in with statements and support automatically logging
        in and logging out.  For example
            
            with driver:
                driver.scanZoneList()
                
        which will automatically call driver.login() and driver.logout()
        """
        self.logout()

    def _requireZone(self,zone_fqdn):
        """Obtains the vendor specific information for a zone or
        throws an exception.
        
        :param zone_fqdn: the FQDN of the zone that is required
        :raises ZoneNotFoundException: if zone_fqdn is not found
        :rtype: The internal vendor specific data structure for the zone
        :returns: The internal vendor specific data structure for the zone
        """
        zone=self._getZone(dotify(zone_fqdn))
        if zone==None:
            raise ZoneNotFoundException(zone_fqdn)
        return zone
    
    def _getMatchingRecord(self,rname,zone,spec,matchTTL):
        """Locate a specific record, optionally ignoring the TTL field
        and matching only on type and rdata.  Base provides a default
        interpretation that requires scanning the resource, which
        may be acceptable.
                
        :param rname: the local resource name relative to the zone
        :param zone: vendor specific record for zone
        :param spec: RecordSpec to locate
        :param matchTTL: determines whether or not to ignore TTL on match
        :returns: vendor specific data structure for the record
        :rtype json:
        """
        raise ImplementationMissingException()
        
    def _getZone(self,zone_fqdn):
        """Obtain the vendor specific information for a zone.  This must be
        implemented by the driver class.
        
    
        :param zone_fqdn: the FQDN of the zone that is required
         
        """
        self._scan_zonelist_if_needed()
        zone=self.zone_map.get(zone_fqdn)
        if zone==None:
            self._scan_zonelist_if_needed(force=True)
            zone=self.zone_map.get(zone_fqdn)
        return zone
    def _generate_logresult(self,obj):
        """Try to convert the log result into a string of no more than about
        40 characters in length - this lets us record results, but avoids dumping
        huge results into the log file wholesale.  If the object to be formatted
        is an exception, then the message is not truncated, and the string
        value of the exception is provided.
        
        :param any obj: the object to stringify
        :returns: string of object, truncated as required
        :rtype: string
        """
        msg=str(obj)
        if isinstance(obj,Exception):
            msg="Exception:%s" % msg
        else:
            if len(msg)>40:
                return '%s...%s' % (msg[:20],msg[-20:])
            else:
                return msg
    
    def _zone_map_is_current(self):
        if self.zone_map_time==None:
            return False
        now=time.time()
        return ((now-self.zone_map_time)<self.ZONE_MAP_REFRESH_THRESHOLD)
    
    def _scan_zonelist_if_needed(self,force=False):
        if force or not self._zone_map_is_current():
            self.zone_map={}
            self.perform_scanZoneList()
            self.zone_map_time=time.time()
            
    #
    # Zone management
    #   - scanZoneList   - obtain a list of the zones
    #   - scanZone       - read all the informationa about a zone
    #   - hasZone        - true if we have a zone
    #   - createZone     - create a zone
    #   - deleteZone     - delete a zone
    @login_required()
    def scanZoneList(self):
        """Obtain the list of zones, requiring login, generating statistics, and ensuring that
        a log entry will be produced.
        """
        stat=self.stats['scanZoneList']
        try:
            stat.start()
            self._scan_zonelist_if_needed()
            result=[{
                    'name':dotify(name)
                    } for name,zone in self.zone_map.items()]
            logresult=self._generate_logresult(result)
        except Exception as E:
            logresult=self._generate_logresult(E)
            raise
        finally:
            stat.end()
            self.log.debug("Zone list scan took %s, returning %s" % (stat.last_delta_string,logresult))
        return result
            
    def perform_scanZoneList(self):
        """This must be implemented by the subclass."""
        raise ImplementationMissingException()
    
    @login_required()
    def scanZone(self,zone_fqdn):
        """Scan a zone, requiring login, generating statistics, and ensuring that
        a log entry will be produced.
        
        :raises MalformedZoneFQDN: `zone_fqdn` is not a valid fqdn
        """
        stat=self.stats['scanZone']
        try:
            stat.start()
            if not is_valid_zone_fqdn(zone_fqdn):
                raise MalformedZoneFQDN(zone_fqdn)   
            zone=self._requireZone(zone_fqdn)
            
            result=self.perform_scanZone(zone)
            logresult=self._generate_logresult(result)
        except Exception as E:
            logresult=self._generate_logresult(E)
            raise
        finally:
            stat.end()
            self.log.debug("Zone scan took %s, returning %s" % (stat.last_delta_string,logresult))
        return result

    def perform_scanZone(self,zone):
        """This must be implemented by the subclass.
        
        :param zone zone: zone is the internal vendor record of the zone
            from :meth:`_getZone`
        """
        raise ImplementationMissingException()

    @login_required()
    def hasZone(self,zone_fqdn):
        """Check to see if a zone exists.
        :param str zone_fqdn: The fully qualified (dot-ending) zone name
        :return: True if the zone exists
        :rtype: None
        """
        stat=self.stats['hasZone']
        result=False
        try:
            stat.start()
            if not is_valid_zone_fqdn(zone_fqdn):
                raise MalformedZoneFQDN(zone_fqdn)   
            self._scan_zonelist_if_needed()
            result=self.perform_hasZone(zone_fqdn)
            logresult=self._generate_logresult(result)
        except Exception as E:
            logresult=self._generate_logresult(E)
            raise
        finally:
            stat.end()
            self.log.debug("hasZone(%s) took %s, returning %s" % (zone_fqdn,stat.last_delta_string,logresult))
        return result
            
    def perform_hasZone(self,zone_fqdn):
        """Check to see if a zone exists.
        :param str zone_fqdn: The fully qualified (dot-ending) zone name
        :return: True if the zone exists
        :rtype: None
        """
        return self.zone_map.get(zone_fqdn)!=None
        
            
        

    @login_required()
    def createZone(self,zone_fqdn,default_ttl=800,admin_email=None):
        """Create the zone if the zone does not exist, using the `default_ttl`
        and `admin_email` (for the SOA record) if those are not configured
        elsewhere, such as in the vendor's main account mgmt settings.
        
        :raises MalformedZoneFQDN: `zone_fqdn` is not a valid fqdn
        :raises ZoneAlreadyExistsException: the zone already exists
        
        :param str zone_fqdn: The fully qualified (dot-ending) zone name
        :param str default_ttl: defaults to 800
        :param str admin_email: defaults to None
        :return: Nothing
        :rtype: None
        """
        stat=self.stats['createZone']
        try:
            stat.start()
            if not is_valid_zone_fqdn(zone_fqdn):
                raise MalformedZoneFQDN(zone_fqdn)   
            
            if self.hasZone(zone_fqdn):
                raise ZoneAlreadyExistsException(zone_fqdn)

            self.perform_createZone(zone_fqdn,default_ttl,admin_email)
            self.zone_map[zone_fqdn]=self._getZone(zone_fqdn)
            logresult=self._generate_logresult(True)
        except Exception as E:
            logresult=self._generate_logresult(E)
            raise
        finally:
            stat.end()
            self.log.debug("createZone(%s,%s,%s) took %s, returning %s" % (zone_fqdn,admin_email,default_ttl,stat.last_delta_string,logresult))
        return True

    def perform_createZone(self,zone_fqdn,default_ttl,admin_email):
        """Only needs to implement the actual zone creation as we know
        that the zone does not exist and is valid.
        """
        raise ImplementationMissingException()
  
    @login_required()    
    def deleteZone(self,zone_fqdn):
        """Delete this zone if it exists, ignore zones that do not exist.
        
        :raises MalformedZoneFQDN: `zone_fqdn` is not a valid fqdn
        
        :param str zone_fqdn: The fully qualified (dot-ending) zone name
        """
        stat=self.stats['deleteZone']
        try:
            stat.start()
            if not is_valid_zone_fqdn(zone_fqdn):
                raise MalformedZoneFQDN(zone_fqdn)   
            
            zone=self._getZone(zone_fqdn)
            if zone!=None:
                self.perform_deleteZone(zone)
                if self.zone_map.get(zone_fqdn)!=None:
                    del self.zone_map[zone_fqdn]
                logresult=self._generate_logresult("Zone deleted")                
            else:
                logresult=self._generate_logresult("Zone did not exist")
        except Exception as E:
            logresult=self._generate_logresult(E)
            raise
        finally:
            stat.end()
            self.log.debug("deleteZone(%s) took %s, returning %s" % (
                zone_fqdn,
                stat.last_delta_string,logresult))
        
    def perform_deleteZone(self,zone):
        """Only needs to implement the actual zone deletion
        
        :param zone zone: the vendor internal zone representation
        """
        raise ImplementationMissingException()
        
    
    #
    # Resource management
    #   - hasResource
    #   - scanResource
    #   - deleteResource
    def hasResource(self,fqdn_or_rname,zone_fqdn=None):
        """Invokes :meth:`perform_hasResource` with the zone and rname extracted
        from `fqdn_or_rname` and `zone_fqdn`.  The invocation is timed.
        """
        stat=self.stats['hasResource']
        try:
            stat.start()
            (rname,zonename)=self._identify_names(fqdn_or_rname,zone_fqdn)
            zone=self._requireZone(zonename)
            result=self.perform_hasResource(rname,zone)
            logresult=self._generate_logresult(True)
        except Exception as E:
            logresult=self._generate_logresult(E)
            raise
        finally:
            stat.end()
            self.log.debug("hasResource(%s,%s) took %s and returned %s" % (
                fqdn_or_rname,zone_fqdn,
                stat.last_delta_string,logresult))            
        return result

    def perform_hasResource(self,rname,zone):
        """Must be implemented by a subclass but `rname` can be assumed to be
        a zone local name, which may or may not exist, and `zone` can be assumed
        to have the vendor specific zone structure.
        """
        raise ImplementationMissingException()
    
    def scanResource(self,fqdn_or_rname,zone_fqdn=None):
        """Invokes :meth:`perform_scanResource` with the zone and rname extracted
        from `fqdn_or_rname` and `zone_fqdn`.  The invocation is timed.
        """
        stat=self.stats['scanResource']
        try:
            stat.start()
            (rname,zonename)=self._identify_names(fqdn_or_rname,zone_fqdn)
            zone=self._requireZone(zonename)
            if self.perform_hasResource(rname,zone):
                result=self.perform_scanResource(rname,zone)
            else:
                result=None
            logresult=self._generate_logresult(result)
        except Exception as E:
            logresult=self._generate_logresult(E)
            raise
        finally:
            stat.end()
            self.log.debug("scanResource(%s,%s) took %s and returned %s" % (
                fqdn_or_rname,zone_fqdn,
                stat.last_delta_string,logresult))            
        return result

    def perform_scanResource(self,rname,zone):
        """Must be implemented by a subclass.  rname can be assumed to be
        a zone local name, which may or may not exist, and `zone` can be assumed
        to have the vendor specific zone structure.
        """
        raise ImplementationMissingException()
    
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
        stat=self.stats['deleteResource']
        try:
            stat.start()
            (rname,zonename)=self._identify_names(fqdn_or_rname,zone_fqdn)
            zone=self._requireZone(zonename)
            if not self.perform_hasResource(rname,zone):
                result=False
            else: 
                result=self.perform_deleteResource(rname,zone)
            logresult=self._generate_logresult(result)
        except Exception as E:
            logresult=self._generate_logresult(E)
            raise
        finally:
            stat.end()
            self.log.debug("deleteResource(%s,%s) took %s and returned %s" % (fqdn_or_rname,zone_fqdn,
                stat.last_delta_string,logresult))            
        return result
    
    def perform_deleteResource(self,rname,zone):
        raise ImplementationMissingException()
        
    #
    # Record management
    #   - hasRecord
    #   - createRecord
    #   - deleteRecord
    def hasRecord(self,fqdn_or_rname,spec,zone_fqdn=None,matchTTL=True):
        """check if record exists, swallow any exceptions, and return True
        or False depending on whether a record matching the spec is identified.
        The swallowing of exceptions is not mandatory, but is intended to support
        differences in underlying drivers, some of which throw exceptions when
        attempting to read a record that does not exist, while others indicate
        the absence of a record by returning a status code.
    
        :return: True or False if a record matching the spec is found
        :rtype: boolean
        """
        stat=self.stats['hasRecord']
        try:
            stat.start()
            (rname,zonename)=self._identify_names(fqdn_or_rname,zone_fqdn)
            zone=self._requireZone(zonename)
            if not self.perform_hasResource(rname,zone):
                result=False
            else:
                result=self.perform_hasRecord(rname,zone,spec,matchTTL)
            logresult=self._generate_logresult(result)
        except Exception as E:
            logresult=self._generate_logresult(E)
            raise
        finally:
            stat.end()
            self.log.debug("hasRecord(%s,%s,%s) took %s and returned %s" % (
                fqdn_or_rname,zone_fqdn,spec,
                stat.last_delta_string,logresult))            
        return result
        
    def perform_hasRecord(self,rname,zone,spec,matchTTL):
        """This can be optionally overridden - there is a default means of
        implementing this, which may not be the most efficient method
        for a given vendor.
        
        :param string rname: the non-qualified resource name
        :param zone zone: the internal zone record
        :param bool matchTTL: if True, records match only if TTL also matches
        :return: True if the record is matched
        :rtype: boolean
        """
        return self._getMatchingRecord(rname,zone,spec,matchTTL)!=None
        
    def _purge_A_and_AAAA_records(self,rname,zone,pool):
        if pool.has_selected_records(rdtype=RecordType.A):
            for rec in pool.selected_records(rdtype=RecordType.A):
                record=self._getMatchingRecord(rname,zone,rec,matchTTL=True)
                self.perform_deleteRecord(rname,zone,record)
                pool.remove(rec)
        if pool.has_selected_records(rdtype=RecordType.AAAA):
            for rec in pool.selected_records(rdtype=RecordType.AAAA):
                record=self._getMatchingRecord(rname,zone,rec,matchTTL=True)
                self.perform_deleteRecord(rname,zone,record)
                pool.remove(rec)                            
        
    def _purge_CNAME_records(self,rname,zone,pool):
        if pool.has_selected_records(rdtype=RecordType.CNAME):
            rec=pool.get_singleton_record(RecordType.CNAME)
            self.log.debug("PURGING CNAME, found=%s" % rec)
            record=self._getMatchingRecord(rname,zone,rec,matchTTL=True)
            self.log.debug("MATCH: %s" % record)
            self.perform_deleteRecord(rname,zone,record)
            pool.remove(rec)
        
    @login_required()
    def createRecord(self,fqdn_or_rname,spec,zone_fqdn=None,addrec=False):
        """Create a resource record from a record spec.  The zone is indicated
        either via the fqdn_or_rname parameter or passed explicitly in the
        zone_fqdn.  The zone must exist in both cases.  The two parameters are
        used in this way to accommodate cases where the zone is already known
        and we are working with resources relative to a specific zone, avoiding
        the need to form the resource fqdn each time.
    
        :param str fqdn_or_rname: If zone_fqdn is provided, this is interpreted
           as a resource name relative to the zone_fqdn it is treated
           as the fqdn of a resource.
       
        :param RecordSpec spec: This is a record specification defined in
           the hyperdns.netdns.RecordSpec class.
        :param str zone_fqdn: Optional zone_fqdn for the zone relative to
           which fqdn_or_rname is evaluated
        :param addrec: Controls the addition of A and AAAA records to a pool
           versus replacing them.  When True, existing A and AAAA records will
           be deleted, and when False a new record will be added.  If the ttls
           in the pool differ, the minimum will be used for the set.
        :type addrec: bool
        
        """
        stat=self.stats['createRecord']
        try:
            stat.start()
            
            # currently we only support a few types of records - for the moment
            # I'm only supporting A and CNAME records
            if not spec.rdtype in [RecordType.A,RecordType.CNAME,RecordType.AAAA,RecordType.NS,
                                    RecordType.TXT,RecordType.MX]:
                raise UnsupportedRecordType(spec.rdtype)
            
            #
            (rname,zonename)=self._identify_names(fqdn_or_rname,zone_fqdn)
            zone=self._requireZone(zonename)
            resource=None
            try:
                resource=self.perform_scanResource(rname,zone)
            except Exception as E:
                self.log.debug("Received Exception during scan:%s" % E)
                pass
                
            if resource==None:
                # our analysis is done, we can just create the record and
                # with it the resource
                self.perform_createRecord(rname,zone,spec,RecordPool())
                logresult=self._generate_logresult("Resource And Record Created")
            else:
                # since we have an existing record we need to analyze the
                # impact of this change
                pool=RecordPool.from_records(resource['records'])

                if pool.contains(spec,matchSource=False):
                    raise RecordAlreadyExistsException(spec)

                if spec.rdtype==RecordType.CNAME:
                    self._purge_CNAME_records(rname,zone,pool)
                    self._purge_A_and_AAAA_records(rname,zone,pool)
                elif spec.rdtype==RecordType.A:
                    self._purge_CNAME_records(rname,zone,pool)
                    if not addrec:
                        self._purge_A_and_AAAA_records(rname,zone,pool)
                elif spec.rdtype==RecordType.AAAA:
                    self._purge_CNAME_records(rname,zone,pool)
                    if not addrec:
                        self._purge_A_and_AAAA_records(rname,zone,pool)
                        
                    
                # this should tell us if the
                pool.add(spec)
                self.perform_createRecord(rname,zone,spec,pool)
            logresult=self._generate_logresult("Ok")
        except CommunicationsFailureException as E:
            logresult=self._generate_logresult(E)
            raise
        except Exception as E:
            logresult=self._generate_logresult("%s:%s" % (E.__class__.__name__,E))
            raise
        finally:
            stat.end()
            self.log.debug("createRecord(%s,%s,%s) took %s and returned %s" % (
                fqdn_or_rname,zone_fqdn,spec,
                stat.last_delta_string,logresult))            

    def perform_createRecord(self,rname,zone,spec,pool,addrec=False):
        """Placeholder method to create a record- this must be overridden
        
        :param rname: the local resource name for which the record is to be deleted
        :type rname: str
        :param zone: the vendor local data structure representing the zone
        :type zone: vendor specific
        :param spec: RecordSpec to add
        :type spec: RecordSpec
        :param pool: Existing records for resource
        :type pool: RecordPool
        :param addrec: Controls the addition of A and AAAA records to a pool
           versus replacing them.  When True, existing A and AAAA records will
           be deleted, and when False a new record will be added.  If the ttls
           in the pool differ, default_ttl be used for the set.
        :type addrec: bool
        :raises ImplementationMissingException: always
        """
        raise ImplementationMissingException()

    @login_required()
    def deleteRecord(self,fqdn_or_rname,spec,zone_fqdn=None,matchTTL=True):
        """Checks the integrity of the arguments, determines if the record
        exists, and if it does, times and invokes perform_deleteRecord to do the
        actual removal.
        :param fqdn_or_rname: the fqdn of the resource name, or, if zone_fqdn is
            provided, then the resource local name of the resource believe to have
            the attached record.
        
        :param spec: the RecordSpec of the record to be deleted
        :param zone_fqdn: the zone relative to which the fqdn_or_rname is
             interpreted.
        :param matchTTL: True or False indicating whether or not the ttl should
          be considered in record matching when finding the record to delete
        """
        stat=self.stats['deleteRecord']
        try:
            stat.start()
            (rname,zonename)=self._identify_names(fqdn_or_rname,zone_fqdn)
            zone=self._getZone(zonename)
            if zone!=None:
                record=self._getMatchingRecord(rname,zone,spec,matchTTL)
                if record==None:
                    result="Record was not found"
                else:
                    self.perform_deleteRecord(rname,zone,record)
                    result="Record deleted"
            else:
                result="Zone not found"
            logresult=self._generate_logresult(result)
        except CommunicationsFailureException as E:
            logresult=self._generate_logresult(E)
            raise
        except Exception as E:
            logresult=self._generate_logresult(E)
            raise
        finally:
            stat.end()
            self.log.debug("deleteRecord(%s,%s,%s,%s) took %s and returned %s" % (
                fqdn_or_rname,zone_fqdn,spec,matchTTL,
                stat.last_delta_string,logresult))            
                    
    def perform_deleteRecord(self,rname,zone,record):
        """Placeholder method - this must be overridden
        
        :param rname: the local resource name for which the record is to be deleted
        :type rname: str
        :param zone: the vendor local data structure representing the zone
        :type zone: vendor specific
        :param record: the vendor local data structure representing the record
        :type record: vendor specific
        :raises ImplementationMissingException: always
        """
        raise ImplementationMissingException()

 
    
