import unittest
import hyperdns.netdns as dns
import hyperdns.netdns
from hyperdns.netdns import RecordSpec,MalformedRecordException,MalformedTTLException

class TestCase(unittest.TestCase):

    def setUp(self):
        self.rec1={'type': 'A', 'ttl': 3, 'rdata': '1.2.3.4', 'class': 'IN'}
        pass 

    def tearDown(self):
        pass

    def test_00(self):
        r=RecordSpec(json={
            'ttl':3,
            'rdata':'1.2.3.4',
            'type':'A',
            'class':'IN'
        })
        assert r.json==self.rec1
        old=r
        
        r=RecordSpec(json={
            'ttl':3,
            'rdata':'1.2.3.4',
            'type':'A'
        })
        
        str_r="%s" % r
        assert r.key=='{1.2.3.4}{3}{1}{1}'
        assert str_r=='{"class": "IN", "rdata": "1.2.3.4", "ttl": 3, "type": "A"}'        
        assert r.json==self.rec1        
        assert r==self.rec1
        assert r==old
        assert r.ttl==3
        assert r.rdata=='1.2.3.4'
        assert r.rdtype==1
        assert r.num_rdtype==1        
        assert r.str_rdtype=='A'      
        assert r.rdclass==1
        assert r.num_rdclass==1        
        assert r.str_rdclass=='IN'
        
        def massive_ttl():
            r.ttl=198438290489328908

        self.assertRaises(MalformedTTLException,massive_ttl)

    def test_01_arec(self):
        recmaker=hyperdns.netdns.spec.ipv4_a_record
        rec=recmaker('1.2.3.4')
        assert rec=={"class": "IN", "rdata": "1.2.3.4", "ttl": 86400, "type": "A"}
        self.assertRaises(MalformedTTLException,recmaker,'1.2.3.4',ttl=-1)
        self.assertRaises(MalformedTTLException,recmaker,'1.2.3.4',ttl=123123123123)
        self.assertRaises(ValueError,recmaker,'not-ip')
        
        
        
