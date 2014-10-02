from binkeul import kode

class HKode( kode.Kode ):
    
    def __new__(cls, num ) :
        return super().__new__(cls,'H',num)
        
    def __init__(self, num ) :
        super().__init__('H',num)
    

    
if __name__ == "__main__" : 
    pass
