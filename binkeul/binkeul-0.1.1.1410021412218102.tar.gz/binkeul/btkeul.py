'''
BtKeul 은 Keul 에 이미지 생성 기능이 추가된 클래스
'''
from binkeul._srchead import *
from binkeul.kode import * 

from binkeul.bkode import * 
from binkeul.hkode import * 
from binkeul.lkode import * 

from binkeul.btgrid import * 
from binkeul.btdeco import * 

from PIL import Image


class BtArea(Area):
    '''
    base_rect [Rect]: 전체 한계영역 rect
    last_rect [Rect: 마지막으로 추가한 (addRect) rect 
    pivot [Point]: 결합위치 
    '''
    def __init__(self, first_rect ):
        super().__init__()
        
        self.unionRect( first_rect )  
        #self.last_rect = Rect(self)
        self.pivot = Point([0,0])
        
    # add_dir 는 추가되는 방향 
    # 추가할때마다 pivot (offset) 이 변경된다.
    # base_rect 와 겹치지 않는 범위에서 
    # move 된 rect 를 반환한다.
    def addRect( self, rect, join_dir, pivot=None, base_rect=None ) :
        assert type(join_dir) == Dir
        
        if not base_rect : base_rect = self.rect
        if not pivot : pivot = self.pivot
        
        if join_dir == Dir.우   : move_p = ( base_rect.right - rect.left , self.pivot[1] )
        elif join_dir == Dir.좌 : move_p = ( base_rect.left - rect.right , self.pivot[1] )
        elif join_dir == Dir.하 : move_p = ( self.pivot[0] , base_rect.bottom - rect.top )
        elif join_dir == Dir.상 : move_p = ( self.pivot[0] , base_rect.top - rect.bottom )
        else : raise ValueError
            
        mv_rect = rect.move( move_p )
        self.pivot = Point([0,0]).move( move_p )
        
        self.unionRect( mv_rect ) 
        return mv_rect
        

# usize 와 쓰기방향을 설정한다.
# coldir  열 방향 
# rowdir  행 방향 (new line)
class BtConf(dict) :
    def __init__(self, 
            usize = 2 ,
            #coldir= Dir.하, 
            coldir= Dir.우, 
            rowdir= Dir.하 ) :
                
        self.update( {
            "B": BtOpt(usize),
            "H": BtTag(usize),
            "L": BtGrid(usize),
            "Q": None } )
        
        self.coldir = coldir
        self.rowdir = rowdir
    
    # btarea의 기본 limit 영역을 정한다.
    def btareaSetLimit(self,btarea) :
        if self.coldir in ( Dir.좌, Dir.우 ) :
            limit = self['L'].getLimit( Lo.세로 )
        elif self.coldir in ( Dir.상, Dir.하 ) :
            limit = self['L'].getLimit( Lo.가로 )
        btarea.unionRect(limit)
        
class BtKeul(Keul) :
    
    def __init__(self, kodes=[] , check=True, btconf = BtConf(4) ) :
        # Kode(추상) 의 구현클래스 LKode , BKode, HKode ..이여야 한다.
        #if check : assert all( map(lambda x: type(x) != Kode, kodes) )
        
        super().__init__( kodes, check )
        self.btconf = btconf
        if check : assert all( map(lambda x: type(x) != Kode, self) )
    
    def setBtConf(self, btconf ) : 
        self.btconf = btconf
        
    
    # btmg의 list 와 btarea 를 구한다 
    def get_btmgs_btarea(self) :
        
        btmglist = []
        first = True
        for kode in self :
            btmg = kode.getBtmg( self.btconf  ) # kode.getBtmg
            btmglist.append( btmg )
            if first :
                btarea = BtArea(btmg.rect)
                self.btconf.btareaSetLimit(btarea)
                first = False 
            else :
                btarea.addRect(btmg.rect, self.btconf.coldir )
            btmg.setPivot( btarea.pivot )
                
        return btmglist, btarea
    
    def getImage(self) :
        
        btmglist, btarea = self.get_btmgs_btarea()
        
        im = Image.new('1',btarea.size,color=255 )
        pil_draw = ImageDraw.Draw(im)
        
        for btmg in btmglist :
            btmg( pil_draw, offset=btarea.orign )
            #print(repr(kode))
        
        return im
    
    def getHtmlImg(self):
        im = self.getImage()
        kio = self.toKioZ3a2s()
        kio.seek(0)
        return pilimg2htmlimg(im, "Z3A2:{}".format(kio.read()) )
        
if __name__ == '__main__' :
    pass
    #kl = BtKeul( [ Kode('B',126), Kode('H',1234),Kode('L',51515),Kode('L',12345) ] )
    #kl.getImage()
