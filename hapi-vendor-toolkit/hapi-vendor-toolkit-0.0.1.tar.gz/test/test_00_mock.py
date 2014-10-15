import unittest
import hyperdns.vendor
from hyperdns.vendor.drivers.mock import HyperDNSDriver as MockDriver


class TestCase(unittest.TestCase):

    def setUp(self):
        MockDriver._reset_config({
            'username':'testkey'
        })
        MockDriver.merge_mock_data('mock',
            'test/zonestates/testkey_testzone.json')
        self.driver=MockDriver({
            'username':'testkey',
            'password':'testkey'
        })


    def tearDown(self):
        pass
        
    def test_00_import(self):
        from hyperdns.vendor.core.registry import driver_registry
        assert 'mock' in driver_registry.keys()

        
    def test_01_scan_zone_list(self):
        zl=self.driver.scanZoneList()
        assert len(zl)==1
        assert zl[0]['name']=='testzone.com.'

    def test_02_scan_absent_zone(self):
        zl=self.driver.scanZone('testzone.org.')
        assert zl==None
        
    def test_03_scan_zone(self):
        zl=self.driver.scanZone('testzone.com.')
        assert zl!=None
        assert zl['name']=='testzone.com.'
        assert len(zl['nameservers'])==4
        assert len(zl['resources'])==1

    def test_04_create_zone(self):
        zl1=self.driver.scanZoneList()
        self.driver.createZone('testzone.com.')
        zl2=self.driver.scanZoneList()
        self.driver.createZone('testzone.org.')
        zl3=self.driver.scanZoneList()
        assert len(zl1)==1
        assert len(zl2)==1
        assert len(zl3)==2

    def test_05_delete_zone(self):
        zl1=self.driver.scanZoneList()
        print(zl1)
        self.driver.deleteZone('testzone.org.')
        zl2=self.driver.scanZoneList()
        self.driver.deleteZone('testzone.com.')
        zl3=self.driver.scanZoneList()
        assert len(zl1)==1
        assert len(zl2)==1
        assert len(zl3)==0


        