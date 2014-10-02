from binkeul._srchead import * 
from binkeul.btgrid import *
from binkeul.kode import *
from binkeul.btmg import *

import pdb 

class LKode( Kode ):
    
    # '0b111111111111111111111111111100000000000000000000000000000000000000000000000000000000000000000000'
    # int( "1" * 28 + "0"* 68  ,2 )
    l3hackmask = 79228162219116432414191124480
    
    
    l3dic = { int(k): v for k, v in binkeul_load_json('l3dic.json').items() }
    
    def __new__(cls, num ) :
        return super().__new__(cls,'L',num)
        
    def __init__(self, num ) :
        super().__init__('L',num)
    
    def isJung(self) :
        return True if self.numerator & Che.정체 else False
    
    # 정체값 
    @property
    def jung(self) :
        return self.numerator | Che.정체

    # L3 값을 핵체의 L3 값으로 바꿈 
    @classmethod
    def L3toHack(cls, L3val ):
        return L3val & cls.l3hackmask 
    
    def getL3(self) :
        if self.isJung() :
            if self.numerator in self.l3dic :
                return self.l3dic[ self.numerator ]
            else : 
                return None
        else : 
            return self.numerator << 67
            
    # btfrm 는 BtGrid
    def getBtmg(self, btconf  ) :
        btfrm = btconf[self.ktype]
        L3val = self.getL3()
        return btfrm.getBtmg( L3val )
        
    
class L3Val( int ):
    
    pass
    
if __name__ == "__main__" : 
    pass

