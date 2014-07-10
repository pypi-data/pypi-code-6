import unittest
import hyperdns.netdns as dns
import ipaddress

class TestCase(unittest.TestCase):

    def setUp(self):
        self.ns1_google=ipaddress.IPv4Address('216.239.32.10')
        self.eights=ipaddress.IPv4Address('8.8.8.8')
        pass 

    def tearDown(self):
        pass

    def test_a00_get_address_from_name(self):
        result=dns.get_address_for_nameserver('ns1.google.com')
        assert result==self.ns1_google
        
    def test_a01_get_address_from_addr(self):
        result=dns.get_address_for_nameserver('8.8.8.8')
        assert result==self.eights
        result=dns.get_address_for_nameserver(self.eights)
        assert result==self.eights

    def test_a02_quick_lookup(self):
        #result=dns.query_nameserver('www.google.com','8.8.8.8',recursive=True,triesRemaining=1)
        result=dns.quick_lookup('ns1.google.com')
        assert result!=[]
        assert result['AnswerSection'][0]['Address']=='216.239.32.10'

        
    def xtest_a02_query_nameserver(self):
        #result=dns.query_nameserver('www.google.com','8.8.8.8',recursive=True,triesRemaining=1)
        result=dns.query_nameserver('ns1.google.com','8.8.8.8',recursive=False,triesRemaining=3)
        print(result)
        result=dns.query_nameserver('ns1.google.com','8.8.8.8',recursive=False,triesRemaining=1)
        print(result)
        result=dns.query_nameserver('ns1.google.com','8.8.8.8',recursive=True,triesRemaining=1)
        print(result)
        result=dns.query_nameserver('ns1.google.com','8.8.8.8',recursive=True,triesRemaining=3)
        print(result)
        raise Exception('A')
        
    def xtest_a01_direct_json_query(self):
        #result=dns.query_nameserver('www.google.com','8.8.8.8',recursive=True,triesRemaining=1)
        result=dns.query_nameserver('www.google.com','8.8.8.8',recursive=False,triesRemaining=3,asjson=True)
        print(result)
        result=dns.query_nameserver('www.google.com','8.8.8.8',recursive=False,triesRemaining=1,asjson=True)
        print(result)
        result=dns.query_nameserver('www.google.com','8.8.8.8',recursive=True,triesRemaining=1,asjson=True)
        print(result)
        result=dns.query_nameserver('www.google.com','8.8.8.8',recursive=True,triesRemaining=3,asjson=True)
        print(result)
        #raise Exception('A')
