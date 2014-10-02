#python3 -m nose_check binkeul cmp

from nose.tools import * # eq_, ok_, nottest, istest
import __head

from binkeul.btmg import *

class TestSuite( __head.ClsTest ):
    def setUp(self):
        pass
        
    def test_area_01(self) :
        
        b = Area()
        b.unionRect( (3,4,5,6) )
        b.unionRect( (-5,-2,10,3) )

        b.left = -11
        
        eq_( b.rect, (-11, -2, 10, 6) )
        eq_( b.size, (21, 8) )

        
if __name__ == '__main__':
    import nose
    nose.main(defaultTest=__name__)
