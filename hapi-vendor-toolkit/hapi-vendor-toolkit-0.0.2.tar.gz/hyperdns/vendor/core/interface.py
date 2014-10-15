import abc
class HyperDNSDriverInterface(metaclass=abc.ABCMeta):
    """The HyperDNSDriver interface defines the methods and properties required
    of a HyperDNS Driver.  Vendors may implement this directly but are encouraged
    to subclass :class:`AbstractDriver`, BaseDriver, or HTTPDriver
    from this module instead, overriding only
    those methods they need to override.

    Interfaces are new'ish' in Python3 - check out: http://pymotw.com/2/abc/

    *Properties*
    The following class properties are defined for each driver.
    
    vkey
        The vendor key, used to identify and load the driver.  This should
        be a short, lowercase, alpha-only string and it should be the last
        segment of the python package implementing the driver.  For example,
        the vkey for the mock driver is `mock`, and it is fully qualified at
        hyperdns.vendor.drivers.mock.

    name
        This is the free form text naming the vendor, it may contain spaces
        and other characters.

    info
        This is a generic JSON structure which provides additional information
        for the drivers.  This includes ``settings`` which is a list of properties
        to be provided by automatic configuration tools.  For example, the
        mock driver contains::

           info={
             'settings':['username','password'],
             'angular':{
                 }
           }

    which causes the automatic configuration tools to prompt for a
    username and password, in that order, when requesting configuration
    information.


    *Transactions*
    Transactions are not nestable, and are implemented at the driver level,
    using the underlying transaction mechanism if the vendor provides it.  If
    the underlying driver does not provide native support for transactions,
    they will be simulated by the :class:AbstractDriver base class.



    """
    
    # properties
    #   vkey
    #   name
    #   info
    @classmethod
    @abc.abstractproperty
    def vkey(cls):
        """Return the vkey, a short, lower case, alpha only identifier for
        the vendor."""
        
    @classmethod
    @abc.abstractproperty
    def name(cls):
        """Name of the driver, which may contain any characters and is
        used for display purposes."""
        
    @classmethod
    @abc.abstractproperty
    def info(cls):
        """JSON data for the vendor.  It can contain anything that is useful,
        but currently only the 'settings' element is required.  The settings
        element is an array of property names required for configuration and
        login.
        
        For example, the mock driver contains::
        
             info={
                 'settings':['username','password'],
                 'angular': {
                     'username':{
                         'label':'Your Username for the Mock Driver',
                         'type':'text',
                         'placeholder':'Username'
                     },
                     'password':{
                         'label':'Your Password for the Mock Driver',
                         'type':'password',
                         'placeholder':'Password'
                     }
                 }
             }
         
        which causes the automatic configuration tools to prompt for a
        username and password, in that order, when requesting configuration
        information.  The angular information is used to create an input
        form for the mock-settings element directive.
        
        """
        return
        
    #
    # settings and session control
    #   - checksettings
    #   - login
    #   - logout
    @classmethod
    @abc.abstractmethod
    def checksettings(cls,settings):
        """Determine if we can log in with the given settings.  The settings
        are the same settings that would be given to the constructor to actually
        create a useable driver instance.
        
        :param json settings: the settings used to configure a driver
        :return: True if the settings allow access, False otherwise
        :rtype: boolean
        """

    @abc.abstractmethod
    def login(self):
        """Log in to the remote vendor, and return True or False.
        
        :return: True or False indicating whether login was successful.
        :rtype: boolean
        """
        
    @abc.abstractmethod
    def logout(self):
        """Logout from the remote session.
        
        :return: nothing
        :rtype: None
        """
    
    #
    # transaction management
    #   - startTransaction
    #   - rollbackTransaction
    #   - commitTransaction
    @abc.abstractmethod
    def inTransaction(self):
        """Returns true if a transaction is active against this vendor
        
        :return: True or False, depending on the transaction
        :rtype: None
        """
    @abc.abstractmethod
    def startTransaction(self,zone_fqdn):
        """Start a transaction on a current zone.  All calls to update the
        state of a zone will be buffered and executed at the end.  Some vendors
        support an underlying transactional model, others do not.  The
        :class:AbstractDriver provides support for transactions if the underlying
        vendor does not.
        
        :param str zone_fqdn: The fully qualified (dot-ending) zone name
        :return: Nothing
        :rtype: None
        """
        
    @abc.abstractmethod
    def rollbackTransaction(self,zone_fqdn):
        """Cancel a given transaction on a zone.
        :param str zone_fqdn: The fully qualified (dot-ending) zone name
        :return: Nothing
        :rtype: None
        """
        
        
    @abc.abstractmethod
    def commitTransaction(self,zone_fqdn):
        """Commit a given transaction on a zone.
        :param str zone_fqdn: The fully qualified (dot-ending) zone name
        :return: Nothing
        :rtype: None
        """
        
        

    #
    # Zone management
    #   - scanZoneList   - obtain a list of the zones
    #   - scanZone       - read all the informationa about a zone
    #   - hasZone        - true if we have a zone
    #   - createZone     - create a zone
    #   - deleteZone     - delete a zone
    @abc.abstractmethod
    def scanZoneList(self):
        """Returns an array of JSON objects describing zones.  Each zone element
        has two members, a 'name' and a 'vendor_data'.  The vendor data is open
        ended format for recording whatever additional data the vendor provides.
        Currently this is not passed back to the driver, but eventually it will
        be.
        
        The name should be the fqdn of the zone - including the trailing dot.
        
        :return: List of zones
        :rtype: JSON data formatted as
            ::
                    
                [{
                    'name':'zone1.com.',
                    'vendor_data':{}
                },{
                    'name':'zone1.org.',
                    'vendor_data':{}
                }
                ]
                
        """
        
    @abc.abstractmethod
    def hasZone(self,zone_fqdn):
        """Check to see if a zone exists.
        
        :param str zone_fqdn: The fully qualified (dot-ending) zone name
        :return: True if the zone exists, False otherwise
        :rtype: None
        """
    @abc.abstractmethod
    def scanZone(self,zone_fqdn):
        """Scan a zone and return all the resource descriptions for that zone.
        
        Return None if zone is not found on vendor, or the following JSON        
        
        :param str zone_fqdn: The fully qualified (dot-ending) zone name
        :return: None or zone information
        :rtype: JSON data formatted as::
                    
                {
                'name':zonename,
                'resources':resources,
                'nameservers':nameservers,
                'source':{
                        'type':'vendor',
                        'vendor':vkey
                        }
                }
        
            Where `resources[]` is a JSON array like::
                    
                [{
                    'name':hostname,
                    'records':[{
                        'ttl':record['ttl'],
                        'rdata':data,
                        'type':hyperdns.netdns.rd_type_as_int(record['record_type']),
                        'class':1
                        },....]
                },.....]
        
        """

    @abc.abstractmethod
    def createZone(self,zone_fqdn,default_ttl=800,admin_email=None):
        """Create the zone if the zone does not exist.

        Throws exception if there was trouble
        
        :param str zone_fqdn: The fully qualified (dot-ending) zone name
        :param int default_ttl: The default TTL for the zone if it is not
          set elsewhere (sometimes the default TTL is configured at the 
          account level, using the vendor's native UI)
           
        :param email admin_email: The administrative contact email in the
          SOA record if it is not set elsewhere (sometimes the admin_email is
          set at the account level, using the vendor's native UI)
          
        :return: Nothing
        :rtype: None
        """
        
    @abc.abstractmethod
    def deleteZone(self,zone_fqdn):
        """Delete this zone if it exists.
        
        :param str zone_fqdn: The fully qualified (dot-ending) zone name
        :return: Nothing
        :rtype: None
        """
        
    #
    # Resource management
    #   - hasResource
    #   - scanResource
    #   - deleteResource
    @abc.abstractmethod
    def hasResource(self,fqdn_or_rname,zone_fqdn=None):
        """Determine if a resource exists.  The zone is indicated
        either via the fqdn_or_rname parameter or passed explicitly in the
        zone_fqdn.  The zone must exist in both cases.  The two parameters are
        used in this way to accommodate cases where the zone is already known
        and we are working with resources relative to a specific zone, avoiding
        the need to form the resource fqdn each time.
        
        :param str fqdn_or_rname: If zone_fqdn is provided, this is interpreted
           as a resource name relative to the zone_fqdn, otherwise it is treated
           as the fqdn of a resource.
        
        :return: True if the resource exists, False otherwise
        :rtype: boolean   
        """
        
    @abc.abstractmethod
    def scanResource(self,fqdn_or_rname,zone_fqdn=None):
        """Returns the records associated with a single resource or None if that
        resource does not exist.  
            
        :param str fqdn_or_rname: STD f-o-r
        :param str zone_fqdn: STD z-f
        :return: JSON descriptor of the resource
        :rtype: The resource return format is

            ::
        
                {
                    'name':hostname,
                    'records':[{
                        'ttl':record['ttl'],
                        'rdata':data,
                        'type':hyperdns.netdns.rd_type_as_int(record['record_type']),
                        'class':1
                        },....]
                }
        """
        
    @abc.abstractmethod
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
    #
    # Record management
    #   - hasRecord
    #   - createRecord
    #   - deleteRecord
    @abc.abstractmethod
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


    @abc.abstractmethod
    def createRecord(self,fqdn_or_rname,spec,zone_fqdn=None):
        """Create a resource record from a record spec.  The zone is indicated
        either via the fqdn_or_rname parameter or passed explicitly in the
        zone_fqdn.  The zone must exist in both cases.  The two parameters are
        used in this way to accommodate cases where the zone is already known
        and we are working with resources relative to a specific zone, avoiding
        the need to form the resource fqdn each time.
        
        :param str fqdn_or_rname: If zone_fqdn is provided, this is interpreted
           as a resource name relative to the zone_fqdn, otherwise it is treated
           as the fqdn of a resource.
           
        :param RecordSpec spec: This is a record specification defined in
           the hyperdns.netdns.RecordSpec class.
        """

    @abc.abstractmethod
    def deleteRecord(self,fqdn_or_rname,spec,zone_fqdn=None,matchTTL=True):
        """Delete a resource record matching a record spec.  The zone is indicated
        either via the fqdn_or_rname parameter or passed explicitly in the
        zone_fqdn.  The zone must exist in both cases.  The two parameters are
        used in this way to accommodate cases where the zone is already known
        and we are working with resources relative to a specific zone, avoiding
        the need to form the resource fqdn each time.
        
        :param str fqdn_or_rname: If zone_fqdn is provided, this is interpreted
           as a resource name relative to the zone_fqdn, otherwise it is treated
           as the fqdn of a resource.
           
        :param RecordSpec spec: This is a record specification defined in
           the hyperdns.netdns.RecordSpec class.  All fields must match before
           the record is deleted, unless matchTTL is set to False.
           
        :param bool matchTTL: determines whether or not the TTL will be used
            to match the record
        """

    #
    # UI support
    @classmethod
    @abc.abstractmethod
    def returnAngularDirective(cls):
        """Return an angular directive supporting configuration
        """
 