from binkeul import kode

class BKode( kode.Kode ):
    
    def __new__(cls, num ) :
        return super().__new__(cls,'B',num)
        
    def __init__(self, num ) :
        super().__init__('B',num)
    

    
if __name__ == "__main__" : 
    pass

