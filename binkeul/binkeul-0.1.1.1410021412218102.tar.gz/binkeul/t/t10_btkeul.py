import pdb 

from binkeul.btkeul import * 

b = BtArea( Rect((-10,-10,10,10 )) )
b.unionRect( (3,4,5,6) )
b.unionRect( (-5,-2,10,3) )

b.left = -11
print(b.rect)
print(b.size)


k01 = BtKeul( [ BKode(126), HKode(1234),LKode(51515), LKode(12345) ] )

print( "-" *77)

ar = BtArea( Rect((-10,-10,10,10 )) )
mr = ar.addRect( Rect((-10,-10,10,10 )) , Dir.우 )

print("mr : " , mr)
print("ar.rect : " , ar.rect)
print("ar.pivot : " , ar.pivot)

mr = ar.addRect( Rect((-10,-10,10,10 )) , Dir.하 )

print("mr : " , mr)
print("ar.rect : " , ar.rect)
print("ar.pivot : " , ar.pivot)

print( "-" *77)

k02 = BtKeul( 
    [ LKode(1141119), LKode(1933311), LKode(6066683), LKode(33626735), LKode(324602), LKode(1192831), LKode(437532127), LKode(84021119),
          
      ] ,
    btconf=BtConf( 6 )
)
'''
k02 = BtKeul( 
    [ LKode(1141119), LKode(324602), ] ,
    btconf=BtConf( 10 )
)
'''
im = k02.getImage()
im.save("btkeul03.png")


