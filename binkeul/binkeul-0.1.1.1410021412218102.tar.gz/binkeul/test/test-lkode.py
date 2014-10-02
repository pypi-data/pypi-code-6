#python3 -m nose_check binkeul cmp


from nose.tools import * # eq_, ok_, nottest, istest
import __head

from binkeul import lkode

class TestSuite( __head.ClsTest ):
    def setUp(self) :
        pass
        
    def test_01(self) :
        
        h = lkode.LKode(534774270)
        eq_( h.getL3() ,  78918752767158813259789762560 )
        assert_false( h.isJung() )
        
        j = lkode.LKode(534774271)
        eq_( j.getL3() , 78918752833740030150835197978 )
        assert_true( j.isJung() )
        
        eq_( h.jung , int(j) )
        
        x = lkode.LKode(534774273)
        eq_( x.getL3() , None ) 
            

if __name__ == '__main__':
    import nose
    nose.main(defaultTest=__name__)
