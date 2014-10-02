#python3 -m nose_check binkeul cmp

from nose.tools import * # eq_, ok_, nottest, istest
import __head
import os

from binkeul import *

class TestSuite( __head.ClsTest ):
    def setUp(self):
        pass
        
    def test_01(self) :
        
        ar = BtArea( Rect((-10,-10,10,10 )) )
        mr = ar.addRect( Rect((-10,-10,10,10 )) , Dir.우 )

        eq_( mr, Rect((10, -10, 30, 10)) )
        eq_( ar.rect, Rect((-10, -10, 30, 10)) )
        eq_( ar.pivot, Points((20, 0)) )

        mr = ar.addRect( Rect((-10,-10,10,10 )) , Dir.하 )
        
        eq_( mr, Rect((10, 10, 30, 30)) )
        eq_( ar.rect, Rect((-10, -10, 30, 30)) )
        eq_( ar.pivot, Points((20, 20)) )
        
        eq_( ar.size, Points((40, 40)) )
        
    def test_02(self) :
        k02 = BtKeul( [   
            LKode(1141119), 
            LKode(1933311), 
            LKode(6066683), 
            LKode(33626735), 
            LKode(324602), 
            LKode(1192831), 
            LKode(437532127), 
            LKode(84021119),
        ],  btconf=BtConf( 6 )  )
        
        imlist = lambda im : tuple(im.getdata())
        
        im1 = k02.getImage()
        im2 = Image.open( os.path.join("_img","btkeul-02-1.png"))
        eq_( imlist(im1), imlist(im2) )
        
        z02 = k02.toKioZ3a2s()
        z02.seek(0)
        eq_( z02.read(), "RytGfzzxhfujxOaYxUvoHQVXnedVnpGiWidxNutNbpOY" )
        

    def test_03(self) :
        
        ls = [56382,39862326,1319834,39862326,56382,69238826]
        LK = LKode
        kl01 = BtKeul( map(LK, ls) )
        
        zio = kl01.toKioZ3a2s()
        
        zio.seek(0)
        zz = zio.read()
        #print(zz)
        
        eq_( zz, 'yEbEDkjooHPmpgakjooHyEbEDJjPXG' )
        
        a = KioZ3a2s()
        a.write(zz)
        
        kl02 = BtKeul.fromKio(a)

        eq_( kl01, kl02 )
        
        
        
if __name__ == '__main__':
    import nose
    nose.main(defaultTest=__name__)
