import logging
import json
from  hyperdns.vendor.core import (
    HyperDNSDriverInterface,
    ZoneNotFoundException,
    TransactionInProgressException,
    TransactionNotInProgressException,
    NotLoggedInException
) 
from hyperdns.netdns import (
    dotify,undotify,
    splitHostFqdn,
    RecordType,RecordClass
    )

    
class AbstractDriver(HyperDNSDriverInterface):
    """This utility class should be a base class for any hyperdns HAPI drivers.
    It adds transaction support, creates a logger, provides utiltiy functions,
    default implementations of common functions, and decorators.

    """
    def __init__(self,settings):
        super(AbstractDriver,self).__init__()
        self.settings=settings
        self.transaction=None
        self.log=logging.getLogger('vendors.%s' % self.vkey)





    # transaction support - in progress, not complete
    def inTransaction(self):
        return self.transaction!=None
        
    def startTransaction(self):
        if self.transaction!=None:
            raise TransactionInProgressException()
        self.transaction=[]
        
    def commitTransaction(self):
        if self.transaction==None:
            raise TransactionNotInProgressException()
        txn=self.transaction
        self.transaction=None
        for entry in txn:
            print("Excecute ",entry)
        
    def rollbackTransaction(self):
        if self.transaction==None:
            raise TransactionNotInProgressException()
        self.transaction=None


    def DEPRECATED_match_rec(self,A,B,matchTTL):
        """determine if two records, A and B match where A and B are
        dict-style representations of two DNS records.  rec['class'],
        rec['type'], and rec['rdata'] are compared, and, if matchTTL
        is set to True, then rec['ttl'] must match.
        
        :param spec A: one of the two records to test
        :param spec B: one of the two records to test
        """
        try:
            matchType=RecordType.as_type(A['type'])==RecordType.as_type(B['type'])
            matchClass=RecordClass.as_class(A['class'])==RecordClass.as_class(B['class'])
            matchTTL=(not matchTTL) or (A['ttl']==B['ttl'])
            matchValue=A['rdata']==B['rdata']
        
            return matchType and matchClass and matchValue and matchTTL
        except Exception as E:
            self.log.error("Failed attempt to match two records, A=%s, B=%s" % (A,B))
            raise


    def _identify_names(self,fqdn_or_rname,zone_fqdn,requireZone=True):
        """Split a fqdn_or_rname and zone_fqdn into an rname and zone_fqdn
        and optionally throw an exception if the zone fails to exist.
        
        Example:
        _identify_names('a','b.com.') -> 'a','b.com.'
        _identify_names('a.b.c',None) -> 'a.b.c',None
        _identify_names('a.b.c.','b.c') -> 'a','b.c.'
        
        """
        if zone_fqdn!=None:
            zone_fqdn=dotify(zone_fqdn)
            fn=dotify(fqdn_or_rname)
            if zone_fqdn==fn:
                (rname,zonename)=('@',zone_fqdn)
            else:
                if fn.endswith(zone_fqdn):
                    (rname,zonename)=(fn[:-(len(zone_fqdn)+1)],zone_fqdn)
                else:
                    (rname,zonename)=(undotify(fqdn_or_rname),zone_fqdn)
        else:
            f=dotify(fqdn_or_rname)
            components=f.split(".")[:-1]
            ct=len(components)
            if ct<2:
                (rname,zonename)=(undotify(fqdn_or_rname),None)
            elif ct==2:
                (rname,zonename)=('@',f)
            else:
                # this is just a guess
                (rname,zonename)=('.'.join(components[:-2]),'.'.join(components[-2:])+'.')
            
        if requireZone:
            if not self.hasZone(zonename):
                raise ZoneNotFoundException(zonename)

        return (rname,zonename)


    
    #
    # settings and session control
    #   - checksettings
    #   - login
    #   - logout
    @classmethod
    def checksettings(cls,settings):
        """Determine if we can log in with the given settings.  A driver is
        created with the provided settings and the login method is called.
        If the login succeeds we return True, but if an exception is thrown
        or if there is any other problem, then we return False.  Any exception
        is logged.
    
        :param json settings: the settings used to configure a driver
        :return: True if the settings allow access, False otherwise
        """
        try:
            driver=cls(settings,immediateLogin=False)
            couldLogIn=driver.login()
            if couldLogIn:
                try:
                    driver.logout()
                except:
                    pass
            return couldLogIn
        except:
            return False


    #
    # Convenience methods and generators
    @property
    def available_zones(self):
        """Iterate over available zone names, returning just the
        names of the available zones.
        """
        zones=self.scanZoneList()
        for zone in zones:
            yield dotify(zone['name'])
            
    def validate_rname_in_zone(self,fqdn):
        """Take a single fqdn for a resource, find out if the fqdn is in
        an existing zone and split the name if there is a matching zone.
        The fqdn does not need to be dotified ahead of time, the trailing
        dot will be added if required.
        
        :rtype: Tuple
        :returns: (boolean,rname,zone_fqdn) as follows
          True,'@',zone_fqdn  : If rname is a zone fqdn
          True,rname,zone_fqdn: If fqdn matches an existing zone
          False,None,None     : If no matching zone is found
        """
        fqdn=dotify(fqdn)
        for z in self.available_zones:
            if fqdn==z:
                return True,'@',z
            if fqdn.endswith(z):
                return True,fqdn[:-(1+len(z))],z
        return False,None,None
        
    #
    # UI support
    @classmethod
    def returnAngularDirective(cls):
        """Returns an angular module hyperdns.vendor.<vkey> which provides
        an element directive of the form <vkey>-settings.
        """
        return """
        angular.module('hyperdns.vendor.%s',[])
        .directive('%sSettings',function() {
        	return {
        		restrict:'E',
        		transclude:true,
        		template:%s
        	}
        })
        """ % (cls.vkey,cls.vkey,json.dumps(cls.get_html_template()))
    
    @classmethod
    def get_html_template(cls):
        """Create a generic angular HTML template for configuring the
        vendor's login from the settings information.
        """
        template="""
        	<fieldset>
            """
        sinfo=cls.info.get('angular',{})
        settings=cls.info.get('settings',[])
        
        for setting in settings:
            info=sinfo.get(setting,{})
            label=info.get('label',setting)
            placeholder=info.get('placeholder',label)
            htype=info.get('type','text')
            template+="""
        		<div class="form-group">
        			<label for="%s" class="control-label">%s</label>
        			<div>
        			  <input required type="%s" class="form-control"
        			  		id="username" placeholder="%s"
        					ng-model="v.settings.%s">
        			</div>
        		</div>
            """ % (setting,label,htype,placeholder,setting)
        template+="""
        	</fieldset>
        """
        return template
