import flasksupport
from hyperdns.hapi.flask import app
from hyperdns.hapi.client import HAPI
import httpretty

class TestCase(flasksupport.SimpleTestCase):

                
    def test_a00_scan(self):
        with app.app_context():
            self.standard_context()
        H=self.hapi
        V=H.vendors['vtst_1']
        result=V.startScan()
        assert result==True

        zonename='omrad.org.'
        zonestate=self.load_zonestate('omrad')['testkey'][zonename]
        
        scan=V.scan
        self.assertRaises(scan.BadCall,scan.reportZoneInfo,'anyzone',{})

        scan.reportZoneList([
            { 'name':zonename }
        ])
        scan.reportZoneInfo(zonename,zonestate)
        scan.complete()
        
        # this is the call that stalls it
        H._refresh_from_server()
        assert list(H.zones.keys())==[zonename]
        
        Z=H.zones[zonename]
        for rdef in zonestate['resources']:
            rname=rdef['name']
            assert rname in Z.resources.keys()
        
        
    def test_a01_scan(self):
        zonename='omrad.org.'
        zonestate=self.load_zonestate('omrad')['testkey'][zonename]
        
        self.test_a00_scan()
        
        H=self.hapi
        V=H.vendors['vtst_1']
        assert V.policy=='peer'
        Z=H.zones[zonename]
        for rdef in zonestate['resources']:
            rname=rdef['name']
            assert rname in Z.resources.keys()
            R=Z.resources[rname]
            assert R.name==rname
            assert R.master==None
            assert R.vendor_targets['vtst_1']!=None
            
        V.changePolicy('master')
        assert V.policy=='master'
        
        Z=H.zones[zonename]
        for rdef in zonestate['resources']:
            rname=rdef['name']
            assert rname in Z.resources.keys()
            R=Z.resources[rname]
            #print("RESOURCE",R,R.master,R.vendor_targets)
            R._refresh_from_server()
            #print("RESOURCE",R,R.master,R.vendor_targets)
            
            assert R.master!=None

