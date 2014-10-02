import pdb 

from binkeul.btmg import * 

b = Area()
b.unionRect( (3,4,5,6) )
b.unionRect( (-5,-2,10,3) )

b.left = -11

print(b.rect)
print(b.size)

