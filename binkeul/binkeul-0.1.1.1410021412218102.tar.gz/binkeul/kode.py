'''
Keul은 편집가능한 메모리를 위한 

IO 는 두 가지 종류
    kbytes
    kz3a2 

'''

import struct, pdb
from binkeul import kio

# file load , parser
class Keul(list):
    '''kode 의 list
    '''
    
    def __init__(self,kodes=[],check=True):
        
        #if check : assert all( map(lambda x: isinstance(x, Kode) , kodes) )
        super().__init__(kodes)
        
        if check : assert all( map(lambda x: isinstance(x, Kode) , self) )
        
    def append(self,kode):
        assert isinstance( kode, Kode )
        super().append(kode)
        
    def extend(self,keul):
        assert isinstance( keul, Keul )
        super().extend(keul)
    
    def insert(self,idx,kode):
        assert isinstance( kode, Kode )
        super().insert(kode)
        
    def __iadd__(self,keul):
        assert isinstance( keul, Keul )
        return super().__iadd__(keul)
        
    def __setitem__(self,idx,kode):
        if type(idx) == slice  :
            assert isinstance( kode, Keul )
        else :
            assert isinstance( kode, Kode )
        
        super().__setitem__(idx,kode)
        
    def __getitem__(self,idx) :
        if type(idx) == slice  :
            return Keul( super().__getitem__(idx) ,False )
        else :
            return super().__getitem__(idx)
        
    def __repr__(self):
        return  "{}({})".format( self.__class__.__name__ , super().__repr__() ) 
        
    def toKioZ3a2s(self, kio_z3a2s = None):
        if kio_z3a2s : assert isinstance( kio_z3a2s, kio.KioZ3a2s )
        else :  kio_z3a2s = kio.KioZ3a2s()
        
        for k in self :
            kio_z3a2s.write( k.toZ3a2s() )
            
        return kio_z3a2s
                
    def toKioBytes(self, kio_bytes = None):
        if kio_bytes : assert isinstance( kio_bytes, kio.KioBytes )
        else :  kio_bytes = kio.KioBytes()
            
        for k in self :
            kio_bytes.write( k.toBytes() )
            
        return kio_bytes
        
    @classmethod
    def fromKio(cls, kio_obj) :
        #keul = Keul()
        keul = cls()
        kio_obj.seek(0)
        
        if isinstance( kio_obj, kio.KioZ3a2s ) :
            while 1 : 
                kd = Kode.fromKioZ3a2s( kio_obj )
                if not kd : break
                keul.append(kd)
        elif isinstance( kio_obj, kio.KioBytes ) :
            while 1 : 
                kd = Kode.fromKioBytes( kio_obj )
                if not kd : break
                keul.append(kd)
        else : raise ValueError
        
        return keul
        
#           # 10101011
_tofs = 0   # 3
_tflg = 1   # 011 (3)
_blen = 2   # 4(Byte)
_vmax = 3   # 2**(32-3)-1

class Kode( int ) :
    # _tofs : top bit offset
    # (_tofs,_tflg,_blen,_vmax)
    KTYPE = {
        'B':(1,0,1,2**7-1),
        'H':(2,1,2,2**14-1),
        'L':(3,3,4,2**29-1), 
        'Q':(4,7,8,2**60-1), 
        } 
        
    EXVAL = {
        1   :   "B",
        3   :   "H",
        7   :   "L",
        15  :   "Q",
    }
    
    # ktype B,H,L byte 수
    def __new__(cls, ktype, num ) :
        return super().__new__(cls,num)
        
    def __init__(self, ktype, num ) :
        self.ktype = ktype
        assert  num <= self.vmax
        
    def __repr__(self):
        return "Kode('{}',{})".format(self.ktype,self.numerator)
        
    def __hash__(self):
        return hash(self.toTuple())
        
    def __eq__(self,o):
        return self.ktype == o.ktype and self.numerator == o.numerator 
    
    def __ne__(self,o):
        return not self.__eq__(o)
        
    def getBtmg(self, btfrm ):
        raise NotImplementedError
    
    @property
    def tofs(self):
        return self.KTYPE[self.ktype][_tofs]
    
    @property 
    def tflg(self):
        return self.KTYPE[self.ktype][_tflg]

    @property 
    def blen(self):
        return self.KTYPE[self.ktype][_blen]
        
    @property 
    def vmax(self):
        return self.KTYPE[self.ktype][_vmax]
        
    @property 
    def nums(self):
        return str( self.numerator )
    
    # Byte 의 정수값 
    @property 
    def byval(self):
        byval = self.numerator << self.tofs
        byval |= self.tflg
        return  byval
    
    # binary 값은 rflg 를 추가한 값이다.
    def toBytes(self) :
        #return struct.pack(self.ktype, self.byval )
        return struct.pack( *self.toTuple(True) )
        
    def toTuple(self, byte_val=False ) :
        return (self.ktype, self.byval if byte_val else self.numerator  )
        
    def toZ3a2s(self):
        
        if self.blen == 1 :
            return kio.Z3a2.pack( self.byval, False )
            
        elif ( self.blen % 2 ) == 0 :
            bys = self.toBytes()
            assert len(bys)%2 == 0 
            
            z3a2s = ''
            for i in range(0,len(bys),2) :
                z3a2s += kio.Z3a2.pack(struct.unpack('H',bys[i:i+2])[0],True)
                
            return z3a2s
            
    @classmethod
    def fromKio(cls, kio_obj ):
        assert isinstance( kio_obj, kio.Kio )
            
        if isinstance( kio_obj, kio.KioZ3a2s ) :
            return fromKioZ3a2s(cls, kio_obj )
        elif isinstance( kio_obj, kio.Kio ) :
            return fromKioBytes(cls, kio_obj )
        
    @classmethod
    def fromKioZ3a2s(cls, kio_z3a2s ):
        '''
        '''
        assert type( kio_z3a2s ) == kio.KioZ3a2s
        
        z1 = kio_z3a2s.read_z1()
        if z1 == '' : return None
        
        byval = kio.Z3a2.unpack( z1 )
        
        if byval < 0 : byval += 256 
        else : assert byval != 65535 
        
        ktype = cls.getKtype(byval)
        blen = cls.KTYPE[ktype][_blen]
        for x in range( 1, blen//2 ) : 
            z1 = kio_z3a2s.read_z1()
            byval += kio.Z3a2.unpack( z1 ) * (65536**x)
        
        
        num = byval >> cls.KTYPE[ktype][_tofs]
        return cls.getKclass(ktype)(num)
        

    # 사용허지 않음
    # 테스트 필요, 중복제거
    # z3a2s 가 하나의 Kode 와 대응할 때 
    @classmethod
    def fromZ3a2s(cls, z3a2s ):
        zlist = kio.Z3a2.split( z3a2s, True )
        zlist = [ kio.Z3a2.unpack( z ) for z in zlist ]
        
        if len(zlist) == 1 :
            if zlist[0] < 0 : 
                blen = 1
                byval = zlist[0] + 256
            else : 
                blen = 2
                byval = zlist[0] 
        elif len(zlist) == 2 :
            assert zlist[0] >= 0 and zlist[0] >= 0
            blen = 4
            byval = zlist[1]*65536 + zlist[0]
        
        ktype = cls.getKtype(byval)
        tofs = cls.KTYPE[ktype][_tofs]
        
        num = byval >> tofs
        return cls.getKclass(ktype)(num)
        
    @classmethod
    def getKtype(cls, byval ):
        exval = (byval + 1) ^ byval 
        assert exval in cls.EXVAL 
        return cls.EXVAL[exval]

    @classmethod
    def getKclass(cls, ktype):
        from binkeul import bkode,hkode,lkode,qkode
        return {
            'B':bkode.BKode,
            'H':hkode.HKode,
            'L':lkode.LKode,
            'Q':qkode.QKode}[ktype]
            
    @classmethod
    def fromKioBytes(cls, kio_bytes ):
        """
        bts 의 시작부터 매치되는 곳까지만 구한다.
        나머지는 구해진 kode 의 blen 바이트수를 계산해야 함 
        """
        assert type( kio_bytes ) == kio.KioBytes
        
        byval_1B = kio_bytes.read(1)
        
        if len(byval_1B) == 0 : return None
            
        #byval_1B = bts[0] # ord(bts[0:1])
        assert byval_1B != 255 # 11111111 은 다음 바이트로 확장됨, 현재 기능없음 
        
        ktype = cls.getKtype(struct.unpack('B' , byval_1B)[0])
        tofs = cls.KTYPE[ktype][_tofs]
        blen = cls.KTYPE[ktype][_blen]
        
        byval = struct.unpack(ktype, byval_1B + kio_bytes.read(blen-1) )[0] # bts[0:blen]
        num = byval >> tofs
        
        return cls.getKclass(ktype)(num)

    
if __name__ == "__main__" : 
    pass
    

