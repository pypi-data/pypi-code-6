from binkeul.kio import * 

for x in (-256,65535,1234,56779) : 
    a01e = Z3a2.pack(x,True)
    a01d = Z3a2.unpack(a01e,True)
    assert x == a01d 
        
    z3a2s = Z3a2.split( "aazzzDPEA" )

for x in (-256,65535,1234,56779) : 
    a01e = Z3a2.pack(x,True)
    a01d = Z3a2.unpack(a01e,True)
    assert x == a01d 
    

z3a2s = Z3a2.split( "aazzzDPEA" )


zz = KioZ3a2s()
zz.write("eiRthEDqcrorKEAEA")
zz.seek(0)
zz.read_z1()

