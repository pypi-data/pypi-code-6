'''
http://stackoverflow.com/questions/10615901/trim-whitespace-using-pil
'''
from PIL import Image, ImageDraw,  ImageChops

class Btmg :
    def __init__(self, usize ) :
        self.usize = usize
        
    def Draw( self, lkode ) :
        pass


class BtChr: 
    def __init__(self, usize ) :
        uz = self.usize = usize
        
        
        #uz = 28
        assert uz % 2 == 0 
        
        um = uz/2
        
        self.box = (0,0,uz*5,uz*5)
        
        self.rects = [] 
        self.lays = []
        self.rays = []
        
        px = lambda p,i : ( p[0]+i[0], p[1]+i[1] ) 
        
        for a in range(9):
            for b in range(9):
                if (a*b) % 2 :
                    
                    p0 = ( a*uz, b*uz )
                    p1 = ( (a+2)*uz-1, (b+2)*uz )
                    
                    self.rays.append( [
                        px( p0 , (um-1,0) ),
                        p0,
                        px( p0 , (0,um-1) ),
                        px( p1 , (-um+1,0) ),
                        p1,
                        px( p1 , (0,-um+1) ),
                    ] )
                    
                else :
                    
                    self.rects.append( ( a*uz+um, b*uz+um, (a+1)*uz+um-1, (b+1)*uz+um-1 ) )
                
        
                
        
        
bc = BtChr(4)

im = Image.new('L',(300,300),color=255 )
draw = ImageDraw.Draw(im)
for r in bc.rects :
    draw.rectangle(r, fill=0)

st = False
for r in bc.rays :
    if not st : 
        draw.polygon(r, fill=100)
        st = True
    else :
        draw.polygon(r, fill=150)
    


im.save("002.png")
