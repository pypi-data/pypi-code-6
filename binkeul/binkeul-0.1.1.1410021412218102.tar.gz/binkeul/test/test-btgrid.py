'''
윈도우에서는 리눅스에서 만들어지는 이미지와 약간 다를 수 있다.
이런 경우 다음과 같이 pass ::

    if sys.platform == 'win32' : return 

'''
#python3 -m nose_check binkeul cmp


from nose.tools import * # eq_, ok_, nottest, istest
import __head

from binkeul._srchead import *
from binkeul.btgrid import *
from binkeul.lkode import *
from PIL import Image
import os,sys

class TestSuite( __head.ClsTest ):
    def setUp(self) :
        pass
        
    def test_01(self) :
        eq_( 
            BtGrid.L3BMAP , 
            ((-4, 4, 'P'), (-4, 2, 'P'), (-4, 0, 'P'), (-4, -2, 'P'), (-4, -4, 'P'), (-2, -4, 'P'), (0, -4, 'P'), (2, -4, 'P'), (-2, 4, 'P'), (0, 4, 'P'), (2, 4, 'P'), (4, 4, 'P'), (4, 2, 'P'), (4, 0, 'P'), (4, -2, 'P'), (4, -4, 'P'), (-3, 2, 'T'), (-3, 0, 'T'), (-3, -2, 'T'), (-2, -3, 'T'), (0, -3, 'T'), (2, -3, 'T'), (-2, 3, 'T'), (0, 3, 'T'), (2, 3, 'T'), (3, 2, 'T'), (3, 0, 'T'), (3, -2, 'T'), (-4, 3, 'T'), (-4, 1, 'T'), (-4, -1, 'T'), (-4, -3, 'T'), (-3, -4, 'T'), (-1, -4, 'T'), (1, -4, 'T'), (3, -4, 'T'), (-3, 4, 'T'), (-1, 4, 'T'), (1, 4, 'T'), (3, 4, 'T'), (4, 3, 'T'), (4, 1, 'T'), (4, -1, 'T'), (4, -3, 'T'), (-1, 3, 'R'), (-3, 3, 'R'), (-3, 1, 'R'), (-3, -1, 'L'), (-3, -3, 'L'), (-1, -3, 'L'), (1, 3, 'L'), (3, 3, 'L'), (3, 1, 'L'), (3, -1, 'R'), (3, -3, 'R'), (1, -3, 'R'), (-1, 3, 'L'), (-3, 3, 'L'), (-3, 1, 'L'), (-3, -1, 'R'), (-3, -3, 'R'), (-1, -3, 'R'), (1, 3, 'R'), (3, 3, 'R'), (3, 1, 'R'), (3, -1, 'L'), (3, -3, 'L'), (1, -3, 'L'), (-2, 0, 'P'), (-2, 2, 'P'), (-2, -2, 'P'), (0, -2, 'P'), (0, 2, 'P'), (2, 2, 'P'), (2, -2, 'P'), (2, 0, 'P'), (-1, 0, 'T'), (-2, 1, 'T'), (-1, 2, 'T'), (-2, -1, 'T'), (-1, -2, 'T'), (0, -1, 'T'), (0, 1, 'T'), (1, 2, 'T'), (2, 1, 'T'), (1, -2, 'T'), (2, -1, 'T'), (1, 0, 'T'), (-1, 1, 'R'), (-1, -1, 'L'), (1, 1, 'L'), (1, -1, 'R'), (-1, 1, 'L'), (-1, -1, 'R'), (1, 1, 'R'), (1, -1, 'L'))
        )
        
    
    def test_02(self) :
        #if sys.platform == 'win32' : return 
        
        imlist = lambda im : tuple(im.getdata())
        cntlist = lambda im : tuple( i for i , x in enumerate( imlist(im) ) if x == 0 )
        
        BC30 = BtGrid(30)
        
        L3val = 582314716142985563463246078
        
        im = BC30.getImage( LKode.L3toHack(L3val) )
        
        im2 = Image.open( os.path.join("_img","btgrid-02-1.png"))
        
        il_1 = imlist(im)
        il_2 = imlist(im2)
        eq_( len(il_1) , len(il_2) ) 
                
        eq_( imlist(im), imlist(im2) )
        
        im = BC30.getImage(L3val)
        im2 = Image.open( os.path.join("_img","btgrid-02-2.png"))
        eq_( imlist(im), imlist(im2) )
        
        
    def test_03(self) :
        #if sys.platform == 'win32' : return 
    
        BC30 = BtGrid(20)
        
        eq_( 
            BC30.getHtmlImg(582314716142985563463246078) ,
            '''<img title="L3:582314716142985563463246078" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMgAAADIAQAAAACFI5MzAAABOUlEQVR4nO3XMY6DMBCF4d+GgjI3SI7io/lozk3YG6R0gZgtjAkZD2022thFhOZThnmJhYwTTpY/g38odzdSP5xzzo2fM1uXdwkiIiKJQdTV38/W5Z37IJnloe+DrxL7eZD6Pvg6udcDQTkfhE+a7UMksZ5IpDljFhEgmrICyZQFmE3JwMOUx6atzFvHVtI2xXE5AXB1dP2dUouGrHtLLcs+hpa8j66l1LIhpc9iSLm3CuSELY4O5A+V2MgKAd8EEpEMiQGuclweyDggqkAeeOCBoAJ5YGYEbiqQBxITcNGBRASuiSHXZ/dzAoEbMKpAfotDG0gkgyQGUYE892n73SI/42u3uoHC62iecnPKGFomAC6GlNpkSOkzGhKel0oisP/nR6ml2EhtE9pu5voecf3duUuXLl329QtqhJqnNgH9sgAAAABJRU5ErkJggg==">'''
        )
        
        
    '''
    def test_(self)
        with assert_raises( AssertionError ):
            kio.Z3a2.split("aazzzDPEAX" , True)
            
        eq_( kio.Z3a2.split('aazzzDPS') , None )
    '''

    def test_04(self) :
        BC30 = BtGrid(20)
        eq_( BC30.getRect(626836596759435428317102080), (-60, -60, 20, 60) ) 
             

if __name__ == '__main__':
    import nose
    nose.main(defaultTest=__name__)
