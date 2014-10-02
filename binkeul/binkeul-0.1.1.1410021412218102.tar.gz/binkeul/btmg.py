'''

* 크기와 스케일 부호와 문자요소에 대한 좌표정보를 생성해낸다.

사각 30*30 
사선 
::

        super().__init__(-9,-40,18,80,parent)
        
        dx = 1 if k == Fo.DR else 0
        self.rotate(45 + dx*-90)
        self.moveBy(x*30,y*30)
        
        
Btmg

BtmgGrid
BtmgDeco
BtmgTag

'''
from PIL import Image, ImageDraw
from functools import lru_cache # @lru_cache
import tempfile, base64, sys 

from binkeul._srchead import *


# PIL 이미지 객체를 html inline image 로 변환 
def pilimg2htmlimg( im, title='' ) :
    with tempfile.TemporaryFile("w+b") as f :
        im.save(f, "PNG")
        f.seek(0)
        imstr = f.read()
        
    imb64 = base64.b64encode( imstr )
    
    return r'''<img title="{}" src="data:image/png;base64,{}">'''.format(
        title, 
        str(imb64,encoding='ascii') 
    )
    

class Points(tuple):
    '''
    ::
    
        >>> list(Points([1,2,3,4]).move((10,100)))
        [11, 102, 13, 104]

    '''
    def move(self,xy):
        return self.__class__( p + xy[i%2] for i, p in enumerate(self) )
        #for i, p in enumerate(self) :
        #    yield p + xy[i%2] 
        
    def __repr__(self) : 
        return "Points({})".format( super().__repr__() )
        
class Point(Points):
    def __init__(self, pts):
        super().__init__()
        assert len(self) == 2

class L_R_T_B : 
    idx = {
        "left" : 0,
        "top" : 1,
        "right" : 2,
        "bottom" : 3 }
        
    def __getattr__(self, attr ) :        
        return self[self.idx[attr]] 
        
    # orign [Point]: (0,0) 을 정하는 기준점으로 첫번째 Kode 의 중심점 lefttop 에서 상대적 좌표값 
    @property    
    def orign(self) : 
        return Points([ -self[0], -self[1] ])
    
        
class Rect(Points,L_R_T_B):
    def __init__(self, pts):
        super().__init__()
        assert len(self) == 4
    
    @property
    def width(self):
        return self[2] - self[0]
        
    @property
    def height(self):
        return self[3] - self[1]

    def __repr__(self) : 
        return "Rect({})".format( tuple(self) )

class Area(list,L_R_T_B) :

    def __init__(self):
        super().__init__([0,0,0,0])
        
    def __setattr__(self, attr, val ) :
        if attr in self.idx :
            self[self.idx[attr]] = val
        else :
            super().__setattr__(attr,val)
    
            
    def unionRect( self, rect ) :
        self[:2] = map( min, zip( self[:2], rect[:2] ) )
        self[2:] = map( max, zip( self[2:], rect[2:] ) )
        

        
    @property
    def rect( self ) : 
        return Rect(self)
        
    @property
    def size( self ) : 
        return ( self[2] - self[0],
                 self[3] - self[1] )
    
    @property             
    def width( self ) :
        return self.size[0]
    
    @property             
    def height( self ) :
        return self.size[1]
    
    def __repr__(self) : 
        return "Area({})".format( list(self) )
                 
        

#----------#----------#----------#----------#----------


# BtGird, BtOpt, BtTag 의 부모 클래스 
class Btfrm :
    def getBtmg(self,*a):
        raise NotImplementedError
    
    def getRect(self,*a):
        raise NotImplementedError
    
    
    
    
# 베틀문자가 있는 이미지 객체  

# 조합가능한 이미지 객체 
# 폭,크기,중심점,
class Btmg :
    def __init__( self, rect, draw_func ) :
        '''
        origin  원점 
        '''
        self.rect = rect
        self.draw_func = draw_func
        self.pivot = Point([0,0])
        
    def setPivot(self, pivot) :
        self.pivot = pivot
        
    def __call__(self, pil_draw, pivot=None, offset=None) :
        if not pivot : pivot = self.pivot
        if offset : pivot = pivot.move( offset )
        self.draw_func(pil_draw, pivot)
    
    '''
    # 영역을 차지하는 rect 절대좌표로 
    @property
    def absrect(self):
        pass
            
    def width(self):
        pass
        
    def height(self):
        pass
    
    def base64(self):
        pass
    
    def htmlimg(self):
        pass
    '''
        

if __name__ == "__main__" :
    pass
    
