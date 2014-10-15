import flasksupport
from hyperdns.hapi.flask import app
from hyperdns.hapi.client import HAPI
import httpretty

class TestCase(flasksupport.SimpleTestCase):

                
    def initializeCase1(self):
        with app.app_context():
            self.standard_context()
        H=self.hapi
        V=H.vendors['vtst_1']
        V.changePolicy('master')
        assert V.policy=='master'
        result=V.startScan()
        assert result==True

        zonename='omrad.org.'
        zonestate=self.load_zonestate('omrad')['testkey'][zonename]
        V.scan.reportZoneList([
            { 'name':zonename }
        ])
        V.scan.reportZoneInfo(zonename,zonestate)
        V.scan.complete()

        # just double-check that it all went through
        H._refresh_from_server()
        assert list(H.zones.keys())==[zonename]
        
        Z=H.zones[zonename]
        for rdef in zonestate['resources']:
            rname=rdef['name']
            assert rname in Z.resources.keys()
        
        
    def test_a01_scan(self):
        self.initializeCase1()
        zonename='omrad.org.'        
        zonestate=self.load_zonestate('omrad')['testkey'][zonename]
        H=self.hapi
        Z=H.zones[zonename]
        for rdef in zonestate['resources']:
            rname=rdef['name']
            assert rname in Z.resources.keys()
            R=Z.resources[rname]
            assert R.name==rname
            assert R.master!=None
            assert R.vendor_targets['vtst_1']!=None
            
        
        Z.ignore()
        Z.unignore()
        Z.delete()
        Z.undelete()
        

