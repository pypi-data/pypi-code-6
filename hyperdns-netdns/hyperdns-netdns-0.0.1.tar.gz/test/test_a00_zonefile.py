import os,unittest,json
import hyperdns.netdns as dns

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

    def test_00_translate_zonefile_to_json(self):
        with open(self.zf['large.com'],"r") as f:
            txt=f.read()
            r=dns.translate_zonefiletext_to_json(txt)
            assert len(r['resources'])==80
            assert r['fqdn']=='large.com.'
        
    def test_01_translate_json_to_zonefile(self):
        with open(self.js['large.com'],"r") as f:
            txt=json.loads(f.read())
            r=dns.translate_json_to_zonefiletext(txt)
            print(r)
            r=dns.translate_zonefiletext_to_json(r)
            print(r)
        raise Exception('A')