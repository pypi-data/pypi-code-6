import pytest
from datetime import datetime

from apikey import QRZ_USERNAME, QRZ_PWD
from pyhamtools.lookuplib import LookupLib

from pyhamtools.exceptions import APIKeyMissingError

from pyhamtools.consts import LookupConventions as const

#Fixtures
#===========================================================

response_XX1XX = {
#    'u_views': u'17495', 
    'biodate': datetime(2014, 5, 14, 23, 28, 4), 
    'image': u'http://files.qrz.com/x/xx1xx/Fred_Ephesus.jpg', 
    'locator': u'KF05nx', 
    'addr2': u'Kingston Alleyx', 
    'addr1': u'DO NOT QSL', 
    'aliases': [u'YY1YY'], 
    'codes': u'TPS', 
    'zip': u'010101', 
    'lotw': True, 
    'state': u'JC', 
    'call': u'XX1XX', 
    'fname': u'Test My', 
    'latitude': -34.010735, 
    'longitude': 21.164476,
    'email': u'trucker2345@easymail.com', 
    'qslmgr': u'NO QSL - TEST CALLSIGN', 
    'bio': u'10381', 
    'ccode': 130, 
    'geoloc': u'user', 
    'eqsl': True,
    'mqsl': True, 
    'adif': 134, 
    'moddate': datetime(2014, 5, 8, 23, 0, 23), 
    'class': u'F', 
    'land': u'Kingman Reef', 
    'imageinfo': u'720:640:179050', 
    'name': 'Account', 
    'born': 2002, 
    'country': u'Jamaica'
}

 
response_XX2XX = {
    'bio': u'0', 
    'land': u'NON-DXCC', 
    'adif': 0, 
    'zip': u'23232', 
    'country': u'Anguilla', 
    'user': u'XX2XX', 
    'moddate': datetime(2014, 9, 19, 19, 36, 31), 
    'lotw': True, 
    'ccode': 9, 
    'geoloc': u'dxcc', 
    'state': u'GA', 
    'eqsl': True, 
    'addr2': u'Atlanta', 
#    'u_views': u'23', 
    'fname': u'Fran\xc3\xa7ois', 
    'addr1': u'123 Main St\xc3\xa3\xc3\xb6\xc3\xb8p\xc3\xaed', 
    'call': u'XX2XX', 
    'name': u'Soto Gonzalez \xc3\xb1',
    'mqsl': True
} 

response_XX3XX = {
#    'u_views': u'4698', 
    'biodate': datetime(2014, 8, 13, 15, 34, 57), 
    'image': u'http://files.qrz.com/x/xx3xx/IMG_8813.JPG', 
    'locator': u'FO51sj', 
    'addr2': u'Shady Circle Roads', 
    'addr1': u'1234 Main St.3', 
    'aliases': [u'XX3XX/W7'], 
    'zip': u'00033', 
    'lotw': False, 
    'state': u'JJ', 
    'call': u'XX3XX', 
    'fname': u'TEST\xdc\xdf\xf8x', 
    'latitude': 51.396953, 
    'email': u'fred@qrz.com', 
    'qslmgr': u'Via BURO or AA7BQ', 
    'bio': u'2420', 
    'ccode': 130, 
    'geoloc': u'user', 
    'eqsl': False, 
    'user': u'XX3XX', 
    'adif': 79, 
    'moddate': datetime(2014, 6, 6, 23, 0, 45), 
    'class': u'3', 
    'land': u'Guadeloupe', 
    'imageinfo': u'540:799:101014', 
    'name': u'CALLSIGN3', 
    'born': 2010, 
    'country': u'Jamaica', 
    'longitude': -68.41959,
    'mqsl': False
}

response_XX4XX = {
#    'u_views': u'7980', 
    'biodate': datetime(2014, 9, 17, 19, 46, 54), 
    'image': u'http://files.qrz.com/x/xx4xx/IMG_0032.JPG', 
    'locator': u'DM79mp', 
    'addr2': u'Getamap and Findit', 
    'addr1': u'Test Callsign for QRZ', 
    'imageinfo': u'1200:1600:397936', 
    'lotw': False, 
    'state': u'ZZ', 
    'call': u'XX4XX', 
    'fname': u'Arthur', 
    'latitude': 39.645, 
    'iota': u'NA-075', 
    'qslmgr': u'NO QSL - TEST CALLSIGN', 
    'bio': u'785', 
    'ccode': 34, 
    'geoloc': u'user', 
    'eqsl': False, 
    'user': u'XX2XX', 
    'adif': 64, 
    'moddate': datetime(2014, 3, 28, 20, 29, 42), 
    'name': u'Fay', 
    'land': u'Bermuda', 
    'zip': u'12345', 
    'country': u'Bermuda', 
    'longitude': -104.96,
    'mqsl': False
}

response_333 = {
    const.COUNTRY: u'Iraq', 
    'cc': u'IQ', 
    const.LONGITUDE: 44.362793, 
    const.CQZ: 21, 
    const.ITUZ: 39, 
    const.LATITUDE: 33.358062, 
    'timezone': 3.0, 
    const.ADIF: 333, 
    const.CONTINENT: u'AS', 
    'ccc': u'IRQ'
}

#TESTS
#===========================================================


class TestQrzConstructur:
    
    def test_get_session_key(self):
        lib = LookupLib(lookuptype="qrz", username=QRZ_USERNAME, pwd=QRZ_PWD)
        assert len(lib._apikey) == 32
    
    def test_get_session_key_with_invalid_username(self):
        with pytest.raises(ValueError):
            lib = LookupLib(lookuptype="qrz", username="hello", pwd=QRZ_PWD)
        
    def test_get_session_key_with_invalid_password(self):
        with pytest.raises(ValueError):
            lib = LookupLib(lookuptype="qrz", username=QRZ_USERNAME, pwd="hello")

    def test_get_session_key_with_empty_username_and_password(self):
        with pytest.raises(ValueError):
            lib = LookupLib(lookuptype="qrz", username="", pwd="")


class TestQrz_Callsign_Lookup: 
    
    def test_lookup_callsign(self, fix_qrz):
        data = fix_qrz._lookup_qrz_callsign("xx1xx", fix_qrz._apikey)
        data.pop('u_views', None)
        assert data == response_XX1XX #check content 
        assert len(data) == len(response_XX1XX) #ensure all fields are included
        
        data = fix_qrz._lookup_qrz_callsign("XX1XX", fix_qrz._apikey)
        data.pop('u_views', None)
        assert data == response_XX1XX
        
        data = fix_qrz._lookup_qrz_callsign("XX2XX", fix_qrz._apikey)
        data.pop('u_views', None)
        assert data == response_XX2XX
        assert len(data) == len(response_XX2XX)
        
        data = fix_qrz._lookup_qrz_callsign("XX3XX", fix_qrz._apikey)
        data.pop('u_views', None)
        assert data == response_XX3XX
        assert len(data) == len(response_XX3XX)
        
        data = fix_qrz._lookup_qrz_callsign("XX4XX", fix_qrz._apikey)
        data.pop('u_views', None)
        assert data == response_XX4XX
        assert len(data) == len(response_XX4XX)
        
    def test_lookup_callsign_with_unicode_escaping(self, fix_qrz):
        data = fix_qrz._lookup_qrz_callsign("XX2XX", fix_qrz._apikey)
        data.pop('u_views', None)
        assert data == response_XX2XX
        
    def test_lookup_callsign_does_not_exist(self, fix_qrz):
        with pytest.raises(KeyError):
            fix_qrz._lookup_qrz_callsign("XX8XX", fix_qrz._apikey)
    
    def test_lookup_callsign_with_empty_input(self, fix_qrz):
        with pytest.raises(ValueError):
            fix_qrz._lookup_qrz_callsign("", fix_qrz._apikey)
        
    def test_lookup_callsign_with_invalid_input(self, fix_qrz):
        with pytest.raises(AttributeError):
            fix_qrz._lookup_qrz_callsign(3, fix_qrz._apikey)


class TestQrz_DXCC_Lookup: 
    
    def test_lookup_dxcc_with_int(self, fix_qrz):
        data = fix_qrz._lookup_qrz_dxcc(333, fix_qrz._apikey)
        assert data == response_333 #check content 
        assert len(data) == len(response_333) #ensure all fields are included
        
    def test_lookup_dxcc_with_string(self, fix_qrz):
        data = fix_qrz._lookup_qrz_dxcc("333", fix_qrz._apikey)
        assert data == response_333 #check content 
        assert len(data) == len(response_333) #ensure all fields are included

    def test_lookup_dxcc_does_not_exist(self, fix_qrz):
        with pytest.raises(KeyError):
            fix_qrz._lookup_qrz_dxcc('854', fix_qrz._apikey)
            
    def test_lookup_dxcc_wrong_input(self, fix_qrz):
        with pytest.raises(ValueError):
            fix_qrz._lookup_qrz_dxcc('', fix_qrz._apikey)

    def test_lookup_dxcc(self, fix_qrz):
        data = fix_qrz.lookup_entity(333)
        assert data == response_333 #check content 
        