import os,unittest,json
from hyperdns.netdns import ZoneData

class TestCase(unittest.TestCase):

    def setUp(self):
        zbase=os.path.dirname(__file__)+'/zonefiles/db.'
        jbase=os.path.dirname(__file__)+'/zonejson/'
        self.zf={}
        self.js={}
        for z in ['large.com','example.com']:
            self.zf[z]="%s%s" % (zbase,z)
            self.js[z]="%s%s.json" % (jbase,z)

    def tearDown(self):
        pass

    def notest_00_translate_zonefile_to_json(self):
        with open(self.zf['large.com'],"r") as f:
            txt=f.read()
            r=ZoneData.fromZonefileText(txt)
            assert len(r['resources'])==80
            assert r['fqdn']=='large.com.'
        
    def notest_01_translate_json_to_zonefile(self):
        with open(self.js['large.com'],"r") as f:
            txt=ZoneData.fromJsonText(f.read())

