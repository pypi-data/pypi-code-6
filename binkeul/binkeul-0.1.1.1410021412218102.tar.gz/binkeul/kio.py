# from --> C:\_ik\py\pyProj\devsrc\bitggal\core
'''
kode를 위한 z3a2 형식의 엔코딩 디코딩 모듈

* z3a2 : 2Byte(양수)와 1Byte(음수) 값을  엔코딩한다. (-256 ~ 65536)
    
* kz3a2 : bkode, hkode, lkode 를 엔코딩한다.

'''

import re, io, pprint, __main__
import pdb 

    
class Z3a2 :

    DIV = 896
    MAX = 65792 
    
    ec9dc= lambda ls : ( ls , dict( [ (c,i) for i,c in enumerate( ls ) ] ) ) ; 
    
    ec_Z, dc_Z = ec9dc( "OoPpQqRrSsTtUuVvWwXxYyZz" )
    ec_N, dc_N = ec9dc( "AaBbCcDdEeFfGgHhIiJjKkLlMmNn" )
    ec_A, dc_A = ec9dc( "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz" )

    PAT = r"([A-N][A-P])|([O-Z][A-Z][A-Z])"
    REGPAT = re.compile(PAT, re.I)
    
    @classmethod
    def split(cls, z3a2s, strict=False ) :
        zlist = []
        
        mpos = 0 
        g = True 
        
        while g : 
            g = cls.REGPAT.match( z3a2s , mpos )
            if g :
                z = g.group(0)
                zlist.append(z)
                mpos += len(z)
        else :
            if strict :
                assert z3a2s[:mpos] == z3a2s 
            elif z3a2s[:mpos] != z3a2s :
                return None
                
        return zlist
    
    @classmethod
    def pack( cls, val, div0 = True ):
        if div0 : val += 256
        
        assert 0 <= val < cls.MAX, "0 <= {} < {}".format(val,cls.MAX)
         
        if 0 <= val < cls.DIV :
            mv , mr  = divmod( val , 32 )
            return cls.ec_N[ mv ] + cls.ec_A[ mr ]
                
        elif cls.DIV <= val < cls.MAX :
            val -=  cls.DIV
            mv , mr = divmod( val , 2704 ) #52*52
            nv , nr = divmod( mr , 52 )
            
            return cls.ec_Z[mv] + cls.ec_A[nv] + cls.ec_A[nr]
        
    @classmethod
    def unpack( cls, z3a2, div0 = True ):
        DIVV = 256 if div0 else 0
        
        m = re.match( cls.PAT + "$", z3a2, re.I )
        assert m
        
        if m.group(1) :
            mv,mr = m.group(1)
            return cls.dc_N[mv]*32 + cls.dc_A[mr] - DIVV
            
        elif m.group(2) : 
            mv,nv,nr = m.group(2)
            return cls.dc_Z[mv]*2704 + cls.dc_A[nv]*52 + cls.dc_A[nr]+ cls.DIV - DIVV 

## Keul
class Kio :
    '''256 유닛 단위마다 카운터를 달아서 
    seek 와 tell 을 구현한다.'''
    def __init__(self, keul=None ):
        from binkeul import kode
        
        if keul == None : keul = kode.Keul() 
        
        assert type(keul) == kode.Keul 
        
        super().__init__()
        self.writek( keul )
        
    def readk(self):
        keul = Keul.fromKio(self)
        return keul
        
class KioBytes(Kio,io.BytesIO):
    def writek(self, keul ) :
        keul.toKioBytes( self )

class KioZ3a2s(Kio,io.StringIO):
    
    def read_z1(self):
        z_2s = self.read(2)
        if z_2s == '' :
            return z_2s
        elif Z3a2.REGPAT.fullmatch( z_2s ) :
            return z_2s
        else :
            z_3s = z_2s + self.read(1)
            if Z3a2.REGPAT.fullmatch( z_3s ) :
                return z_3s
            
            raise ValueError
            
    
    def writek(self, keul ) :
        keul.toKioZ3a2s( self )
    
    
#__TEST__
if __name__ == '__main__' : 
    pass
    
    
