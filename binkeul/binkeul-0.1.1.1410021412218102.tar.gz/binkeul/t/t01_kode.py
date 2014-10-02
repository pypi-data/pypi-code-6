from binkeul.kode import * 

print("----"*14)

k = Kode('H',567)
b = k.toBytes()
print(b)

k = Kode('L',12345)
b = k.toBytes()
print(b)

kl = Keul( [ Kode('B',126), Kode('H',1234),Kode('L',51515),Kode('L',12345) ] )
bts = kio.KioBytes( kl )
bts.seek(0)
print(repr(Kode.fromKioBytes( bts )))
print(repr(Kode.fromKioBytes( bts )))
print(repr(Kode.fromKioBytes( bts )))
print(repr(Kode.fromKioBytes( bts )))

#assert k == Kode.fromKioBytes(  b  )


assert Kode('B',3) != Kode('L',3)

kk = Keul([Kode('H',1234),Kode('L',51515)])
print(kk)

assert Kode.fromZ3a2s("Wum") == Kode('H',11515)
assert Kode.fromZ3a2s("UvpOAx") == Kode('L',5632323)
assert Kode.fromZ3a2s('dM') == Kode('B',124)

kio.KioBytes( Keul([Kode('H',1234),Kode('L',51515)]) )

zz = kio.KioZ3a2s( Keul([Kode('H',1234),Kode('L',51515)]) )
zz.seek(0)
a = Kode.fromKioZ3a2s(zz)
b = Kode.fromKioZ3a2s(zz)
print(a)
print(b)

zz = kio.KioZ3a2s( Keul([Kode('H',12),Kode('L',51515),Kode('Q',21234567)]) )
zz.seek(0)
print(zz.read())
zz.seek(0)
a = Kode.fromKioZ3a2s(zz); print(a)
b = Kode.fromKioZ3a2s(zz); print(b)
c = Kode.fromKioZ3a2s(zz); print(c)

zz = kio.KioZ3a2s( Keul([Kode('H',12),Kode('L',51515),Kode('Q',21234567)]) )

assert (
    Keul.fromKio(zz) ==  Keul([Kode('H',12), Kode('L',51515), Kode('Q',21234567)]) 
)


kl = Keul( [ Kode('B',126), Kode('H',1234),Kode('L',51515),Kode('L',12345) ] )
bts = kio.KioBytes( kl )
