from hyperdns.hal.navigator import Navigator

@Navigator.attach_class()
class Zone(object):
    def require_resource(zone,rname):
        """ return the resource `rname` if it exists in this zone, or
        throw an exception if it does not exist.
        """
        resource=zone.resources.get(rname)
        if resource==None:
            raise Exception('Failed to find resource %s in zone %s' % (rname,zone.fqdn))
        return resource

    def downloadZonefile(zone):
        """download a zonefile for this zone.
        """
        return zone.get('/zonefile',raw=True)


    def ensureResource(zone,name):
        """Return any existing resource or create a resource if it
        does not exist.
        """
        r=zone.resources.get(name)
        if r==None:
            r=zone.post('/resources/%s' % name,{'name':name})
        return r

    def resetMasterFromVendor(zone,vkey):
        """Change the master record for this zone to match the
        records from vendor vkey.
        """
        return zone.post('/reset',{
            'vkey':vkey
        })
    
    def pushMissing(zone,vkey=None):
        """Push missing records from master into the specified vendor, or
        if vkey is None, push any missing records into all vendors.
        """
        if vkey==None:
            return zone.post('/push')
        else:
            return zone.post('/push',{
                'vkey':vkey
            })

    def pullOverpresent(zone,vkey=None):
        """Pull overpresent records from the specified vendor, or if vkey
        is None, from all vendors, into the current zone. 
        """
        if vkey==None:
            return zone.post('/pull')
        else:
            return zone.post('/pull',{
                'vkey':vkey
            })

    def scan(zone):
        """Scan a zone on all vendors
        """
        return zone.post('/scan')

    def adjust(zone):
        """Adjust a zone by apply all pending changes.
        """
        return zone.post('/adjust')

    def assessment(zone):
        """Update the assessment for a zone
        """
        return zone.get('/assessment')

    def ignore(zone):
        """Ignore a zone
        """
        return zone.post('',{
            'ignore':True
        })

    def unignore(zone):
        """Unignore a zone
        """
        return zone.post('',{
            'ignore':False
        })

    def undelete(zone):
        """Undelete a zone
        """
        return zone.post('',{
            'delete':False
        })
    
    def delete(zone):
        """Delete a zone
        """
        return zone.delete()
