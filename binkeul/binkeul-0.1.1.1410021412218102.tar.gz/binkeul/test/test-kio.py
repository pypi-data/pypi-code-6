#python3 -m nose_check binkeul cmp


from nose.tools import * # eq_, ok_, nottest, istest
import __head

from binkeul import kio

class TestSuite( __head.ClsTest ):
    def setUp(self) :
        pass
        
    def test_Z3A2_01(self) :
        
        for x in (-256,65535,1234,56779) : 
            a01e = kio.Z3a2.pack(x)
            a01d = kio.Z3a2.unpack(a01e)
            eq_( x, a01d )
    
    def test_Z3A2_02(self) :
        
        eq_( kio.Z3a2.pack(0), 'EA' )
        
        eq_( kio.Z3a2.pack(-256), 'AA' )
        eq_( kio.Z3a2.pack(0,False), 'AA' )

        eq_( kio.Z3a2.pack(65535), 'zzz' )
        eq_( kio.Z3a2.pack(65791,False), 'zzz' )
        
        
    def test_Z3A2_03(self) :
        with assert_raises( ZeroDivisionError ) :
            45/ 0 
        
        ff = lambda : 45/ 0 
        assert_raises( ZeroDivisionError , ff )
        
        with assert_raises( AssertionError ):
            kio.Z3a2.pack(65536)
            
        with assert_raises( AssertionError ):
            kio.Z3a2.pack(-1,False)
            
    def test_Z3A2_04(self) :
        z3a2s = kio.Z3a2.split( "aazzzDPEA" )
        eq_( z3a2s, ['aa', 'zzz', 'DP', 'EA'] )
        
        with assert_raises( AssertionError ):
            kio.Z3a2.split("aazzzDPEAX" , True)
            
        eq_( kio.Z3a2.split('aazzzDPS') , None )

            

if __name__ == '__main__':
    import nose
    nose.main(defaultTest=__name__)
