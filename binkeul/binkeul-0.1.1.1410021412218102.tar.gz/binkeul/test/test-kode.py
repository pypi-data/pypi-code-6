#python3 -m nose_check binkeul cmp


from nose.tools import * # eq_, ok_, nottest, istest
import __head

from binkeul.kode import *

class TestSuite( __head.ClsTest ):
    def setUp(self):
        pass
        
    def test_Kode_01(self) : 
        
        k = Kode('H',567)
        b = k.toBytes()
        
        eq_( b, b'\xdd\x08' )

        kb = Keul([k]).toKioBytes()
        kb.seek(0)
        
        k2 = Kode.fromKioBytes(kb)
        eq_( k, k2 )
        
    def test_Kode_01(self) : 
        
        from binkeul import kio
        
        k = Kode('L',12345)
        b = k.toBytes()
        eq_( b , b'\xcb\x81\x01\x00' )
        
        kb1 = kio.KioBytes( )
        kb1.write( b'\xcb\x81\x01\x00' )
        
        kb2 = kio.KioBytes( )
        kb2.write( b'\x1b\x8a\xaf\x021234' )
        
        eq_(    Kode.fromKioBytes(kb1) , 
                Kode.fromKioBytes(kb2)  )
                
        
    def test_Kode_02(self) : 
        k1 = Kode('B',127)
        eq_( k1.toZ3a2s() , 'dP' )
        
        k2 = Kode('H',16383)
        eq_( k2.toZ3a2s() , 'zzy' )
        
        k3 = Kode('L',536870911)
        eq_( k3.toZ3a2s() , 'zzxzzz' )
        
        
    def test_Keul_01(self):
        kk = Keul([Kode('H',1234),Kode('L',51515)])
        
        kk += kk[:]
        eq_( kk , Keul([Kode('H',1234), Kode('L',51515), Kode('H',1234), Kode('L',51515)]) )
        
        kk[0] = Kode('B',123)
        eq_( kk , Keul([Kode('B',123), Kode('L',51515), Kode('H',1234), Kode('L',51515)]) )
        
        kk[0:2] = Keul([Kode('H',999)])
        eq_( kk , Keul([Kode('H',999), Kode('H',1234), Kode('L',51515)]) )

    def test_Keul_02(self):
        kk = Keul([Kode('H',1234),Kode('L',51515)])
        with assert_raises(AssertionError) : 
            kk[0] = 90
        
    def test_Keul_03(self):
    
        kl = Keul([Kode('H',12),Kode('L',51515),Kode('Q',21234567)])
        zz = kio.KioZ3a2s( kl )
        eq_( kl, Keul.fromKio(zz) )
        
        kl2 = Keul( [ Kode('B',126), Kode('H',1234),Kode('L',51515),Kode('L',12345) ] )
        bb = kio.KioBytes( kl2 )
        eq_( kl2, Keul.fromKio(bb) )
        
        
if __name__ == '__main__':
    import nose
    nose.main(defaultTest=__name__)
