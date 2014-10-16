from hyperdns.hal.navigator import Navigator
import re

@Navigator.attach_class()
class Account(object):

    def require_vendor(account,vkey):
        vendor=account.vendors.get(vkey)
        if vendor==None:
            account._refresh_from_server()
            vendor=account.vendors.get(vkey)
            if vendor==None:
                raise Exception('Failed to find requested vendor %s' % vkey)
        return vendor

    def require_zone(account,zone_fqdn):
        zone=account.zones.get(zone_fqdn)
        if zone==None:
            zone=account.zones.get(zone_fqdn)
            if zone==None:
                raise Exception('Failed to find requested zone %s' % zone_fqdn)
        return zone
    
    def update_vendor(account,vkey,setup):
        vendor=account.vendors.get(vkey)
        if vendor==None:
            account.configureVendor(vkey,setup)
            account._refresh_from_server()
            vendor=account.vendors.get(vkey)
        else:
            vendor.updateSetup(setup)
    
    def active_vendors(account):
        for v in account.vendors.values():
            if v.active:
                yield v    
        
    def active_zones(account):
        for z in account.zones.values():
            if not z.deleted and not z.ignored:
                yield z
        
    def require_zone_and_resource(account,zone_fqdn,rname):
        zone=account.zones.get(zone_fqdn)
        if zone==None:
            raise Exception('Failed to find requested zone %s' % zone_fqdn)
        resource=zone.resources.get(rname)
        if resource==None:
            raise Exception('Failed to find resource %s in zone %s' % (rname,zone_fqdn))
        return (zone,resource)
    
    def adjust(account):
        """Adjust a resource
        """
        return account.post('/adjust')

    def submitZoneFile(account,zonefile):
        """post a zonefile to the account, the name will be matched up
        on the server side, so no local parsing is required.
        """
        halObject=account.post('/zonefile',{'zonefile':zonefile})

        #print(halObject)
    
    def processZoneFile(account,zonefile):
        """post a zonefile to a zone
        """
        for line in zonefile.split("\n"):
            origin=re.compile('^\$ORIGIN\W+(.*)\W*').match(line)
            if origin!=None:
                fqdn=origin.group(1)
                if not fqdn.endswith("."):
                    fqdn=fqdn+"."
    
        zone=account.zones.get(fqdn)
        if zone==None:
            halObject=account.post('/zones/%s' % fqdn,{'fqdn':fqdn,'zonefile':zonefile})
        else:
            halObject=zone.uploadZonefile(zonefile)

        #print(halObject)

    def ensureZone(account,fqdn):
        """Make sure that a zone exists.
        """
        zone=account.zones.get(fqdn)
        if zone==None:
            account.post('/zones/%s' % fqdn,{'fqdn':fqdn})
            account._refresh_from_server()
            zone=account.zones.get(fqdn)
            
        return zone

    def configureVendor(account,vkey,settings):
        """Configure a vendor for this account
        """
        vendor=account.vendors.get(vkey)
        if vendor==None:
            print("Vendor not found, creating")
            halObject=account.post('/vendors/%s' % vkey,settings)
        else:
            vendor.updateSettings(settings)
        return vendor
