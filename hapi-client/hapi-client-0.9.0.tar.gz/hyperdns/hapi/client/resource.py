from hyperdns.hal.navigator import Navigator
from hyperdns.netdns import (
RecordSpec,RecordPool
)

@Navigator.attach_class()
class Resource(object):
    def overpresent_for_vendor(resource,vendor):
        for rec in resource.delta['overpresent'].get(vendor.vkey,[]):
            yield rec
            
    def missing_for_vendor(resource,vendor):
        for rec in resource.delta['missing'].get(vendor.vkey,[]):
            yield rec
            
    def pushMissing(resource,vendor):
        """Push missing records
        """
        return resource.post('/push',{
            'vkey':vendor.vkey
        })

    def pullOverpresent(resource,vendor):
        """Pull overpresent records
        """
        return resource.post('/pull',{
            'vkey':vendor.vkey
        })
            

    def adjust(resource):
        """Adjust a resource
        """
        return resource.post('/adjust')

    def scan(resource):
        resource.post('/scan')
    
    def reportVendorObservations(resource,vkey,info):
        """Resource
        """
        #print("INFO",info)
        return resource.post('/vendor_targets/%s' % vkey,{
            'records':info
        })
