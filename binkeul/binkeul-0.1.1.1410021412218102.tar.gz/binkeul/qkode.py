from binkeul import kode

class QKode( kode.Kode ):
    
    def __new__(cls, num ) :
        return super().__new__(cls,'Q',num)
        
    def __init__(self, num ) :
        super().__init__('Q',num)
    

    
if __name__ == "__main__" : 
    pass

