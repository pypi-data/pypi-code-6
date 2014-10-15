from hyperdns.hal.navigator import Navigator
from hyperdns.hapi.client import json_safe_zoneinfo
import datetime,json

def _deleteScan(scan,reason):
    try:
        if scan!=None:
            scan.delete('?reason=%s' % (reason))
            return True
    except Exception as E:
        raise E
        return False
    return True

    
    

@Navigator.attach_class()
class Vendor(object):
    
    def company_name(vendor):
        return vendor.definition.info['vendor']
        
    def service_name(vendor):
        return vendor.definition.info['service']
        
    def title(vendor):
        """Return the string "{vkey}:{vname} from {sname}" where vname is the
        name of the service provider and sname is the name of the service
        provide by that vendor.
        """
        vname=vendor.company_name()
        sname=vendor.service_name()
        return "%s:%s from %s" % (vendor.vkey,sname,vname)
        
    def resetMaster(vendor):
        vendor.post('/reset')
        vendor._refresh_from_server()
        
    def adjust(vendor):
        vendor.post('/adjust')
        vendor._refresh_from_server()

    def pushMissing(vendor):
        vendor.post('/push')
        vendor._refresh_from_server()

    def pullOverpresent(vendor):
        vendor.post('/pull')
        vendor._refresh_from_server()

    def reportZoneList(vendor,zonelist):
        vendor.post('/zonelist',zonelist)
        vendor._refresh_from_server()

    def reportZoneInfo(vendor,zonename,zoneinfo):
        zoneinfo=json_safe_zoneinfo(zoneinfo)
        data={
                'name':zonename,
                'info':zoneinfo
            }
        vendor.post('/zoneinfo/%s' % zonename,data,includes_refresh=True)

    def changePolicy(vendor,newpolicy):
        vendor.post('',{
                'policy':newpolicy
            })
        vendor._refresh_from_server()

    def activate(vendor,settings):
        vendor.post('',{
                'active':True,
                'settings':settings
            })
        vendor._refresh_from_server()

    def deactivate(vendor):
        vendor.post('',{
                'active':False
            })
        vendor._refresh_from_server()
    
    def updateSettings(vendor,settings):
        vendor.post('',{
                'settings':settings
            })
        vendor._refresh_from_server()

    def updateSetup(vendor,setup):
        vendor.post('',setup)
        vendor._refresh_from_server()
    
    def runScan(vendor):
        vendor.post('/runscan')
        vendor._refresh_from_server()
    
    def startScan(vendor):
        try:
            if vendor.scan!=None:
                return False
            vendor.post('/scan')
        except Exception as E:
            return False
        vendor._refresh_from_server()
        return True
    
    def pruneScan(vendor,minutes=10):
        """remove the scan if it is too old
        """
        if vendor.scan!=None:
            # 2014-09-21 13:52:23.327234
            #print("vendor.scan.start_time",vendor.scan.start_time)
            start_time = datetime.datetime.strptime(vendor.scan.start_time,"%Y-%m-%d %H:%M:%S.%f")
            age = datetime.datetime.now() - start_time
            if age > datetime.timedelta(minutes=minutes):
                _deleteScan(vendor.scan,"prune")        
                return True
            return False

@Navigator.attach_class()
class ActiveVendorScan(object):

    def reportZoneList(scan,zonelist):
        scan.post('/zonelist',zonelist)

    def reportZoneInfo(scan,zonename,zoneinfo):
        zoneinfo=json_safe_zoneinfo(zoneinfo)
        scan.post('/zoneinfo/%s' % zonename,{
                'name':zonename,
                'info':zoneinfo
            })

    def kill(scan):
        """ remove the scan if it is running
        """
        return _deleteScan(scan,"kill")
    
    def complete(scan):
        """ complete and remove the scan if it is there.
        """
        return _deleteScan(scan,"complete")

