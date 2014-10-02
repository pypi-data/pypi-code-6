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

BtGrid
BtDeco
BtTag
'''
from PIL import Image, ImageDraw
from functools import lru_cache # @lru_cache
import tempfile, base64, sys 
#import collections

import functools

from binkeul._srchead import *
from binkeul.btmg import *

BTMG_JSON = 'btgrid.json'


# 베틀문자의 이미지 생성클래스
class BtGrid(dict, Btfrm) :
    
    L3BMAP = tuple( tuple(i) for i in binkeul_load_json( BTMG_JSON ) )
    
    # 윈도우즈OS의 경우 좌표가 약간 달라진다.
    ifw1 = 1 if sys.platform == "win32" else 0

    def __init__(self, usize ) :
        assert usize % 2 == 0
        uz = self.uz = usize
        um = self.um = uz/2
        
        self.width = self.height = uz*10
        
        # 경계 
        self.limit = Rect([-uz*5,-uz*5,uz*5,uz*5])
        
        for u in range(-4,5):
            for v in range(-4,5):
                if (u*v) % 2 :
                    self.mksasun(u,v)
                else :
                    self[ u,v,{0:'P',1:'T'}[(u+v)%2] ] = Points( [ (u-0.5)*uz, (v-0.5)*uz, (u+0.5)*uz -1, (v+0.5)*uz -1 ] ) 
        
    def mksasun(self,u,v):
        uz, um  = self.uz , self.um
        ifw1 = self.ifw1
        
        xl, xr, yt, yb = (u-1)*uz, (u+1)*uz-1, (v-1)*uz, (v+1)*uz - ifw1
        
        p0 = Points( [ xl, yb ] )
        p1 = Points( [ xr, yt ] )
        
        self[ u,v,'L'] = Points( 
            p0.move( (um-1,0) ) +
            p0 +
            p0.move( (0,-um+1) ) +
            p1.move( (-um+1,0) ) +
            p1 +
            p1.move( (0,um-1) )
        )
        
        p0 = Points( [ xl, yt ] )
        p1 = Points( [ xr, yb ] )
        
        self[ u,v,'R' ] = Points( 
            p0.move( (um-1,0) ) +
            p0 +
            p0.move( (0,um-1) ) +
            p1.move( (-um+1,0) ) +
            p1 +
            p1.move( (0,-um+1) )
        )
    
    def getBtmg(self, l3val ) :
        rect = self.getRect( l3val )
        draw_func = functools.partial( self.drawhwk, l3val )
        return Btmg( rect, draw_func )
        
    def drawhwk( self, l3val, pil_draw, ofs ) : 
        for i in range( l3val.bit_length() ) : # 0 ~ 96
            if l3val & (1 << i) :
                l3bmap = self.L3BMAP[i]
                
                drawdata = self[l3bmap].move( ofs )
                
                if l3bmap[2] in "PT" : 
                    pil_draw.rectangle(drawdata, fill=0)
                elif l3bmap[2] in "RL" :
                    pil_draw.polygon(drawdata, fill=0)
        
        # 중심점을 그린다.
        pil_draw.rectangle(self[0,0,'P'].move(ofs) , fill=0)
                    
    
    # 가상함수 구현, getImagefromL3 와 분리!!
    # getImage(self, lkode )!!
    def getImage( self, l3val, crop = False ) :
        
        if crop :
            rc = self.getRect( l3val )
            im = Image.new('1',(rc.width, rc.height),color=255 )
            ofs = rc.orign 
            
        else :
            im = Image.new('1',(self.width,self.height),color=255 )
            
            ofs = self.limit.orign #[self.width//2,self.height//2]
        
        pil_draw = ImageDraw.Draw(im)
        self.drawhwk( l3val, pil_draw, ofs ) 
        
        return im 
        
    # getHtmlImgfromL3 와 분리
    def getHtmlImg( self, l3val ) :
        im = self.getImage( l3val )
        return pilimg2htmlimg( im , "L3:{}".format(l3val) )
        

    # 최소 크기영역과 중심점의 위치를 구한다.
    # mode ; (True,False) : 가로로 Crop, (False,True) : 세로로  Crop
    def getRect( self, l3val ) :
        '''
        (-4,-4 )- (4,4)
        '''
        
        fomin = [0,0]
        fomax = [0,0]
        
        #for i in range({Che.핵체:68,Che.정체:0}[che],l3val.bit_length() ) : # 0 ~ 96
        
        for i in range( l3val.bit_length() ) : # 0 ~ 96
            if l3val & (1 << i) :
                fx,fy,fk = self.L3BMAP[i]

                rx = fx%2
                ry = fy%2
                fxs = [fx-rx,fx+rx]
                fys = [fy-ry,fy+ry]

                fomin[0] = min( fomin[0] , *fxs )
                fomin[1] = min( fomin[1] , *fys )
                fomax[0] = max( fomax[0] , *fxs )
                fomax[1] = max( fomax[1] , *fys )
        
        pomin = self[fomin[0],fomin[1],'P']
        pomax = self[fomax[0],fomax[1],'P']
        
        um = self.um
        return Rect( map( int , (
            pomin[0] - um,
            pomin[1] - um,
            pomax[2] + um + 1,
            pomax[3] + um + 1
        )))
    
    # 그리는 바탕의 한계 영역을 구한다.
    def getLimit(self, limitLo = Lo.가로 | Lo.세로 ) :
        sl = self.limit 
        if limitLo == Lo.가로 : 
            return Rect(( sl[0], 0, sl[2], 0 ))
        elif limitLo == Lo.세로 : 
            return Rect(( 0, sl[1], 0, sl[3] ))
        elif limitLo == Lo.가로 | Lo.세로  :
            return sl
        
if __name__ == "__main__" :
    pass
    
