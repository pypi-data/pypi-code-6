from binkeul.btgrid import * 
import pprint, pdb

pprint.pprint(BtGrid.L3BMAP)

BC30 = BtGrid(30)

im = BC30.getImage(582314716142985563463246078)
im.save('btmg01.png')


import pprint
pprint.pprint(BtGrid.L3BMAP)

BC30 = BtGrid(20)
    
im = BC30.getImage(582314716142985563463246078,True)
im.save('btmg02.png')

print( BC30.getHtmlImg(582314716142985563463246078) )

print( BC30.getRect(626836596759435428317102080) )

#genCropImage
#getCropSize
    


from binkeul.btgrid import *
import os
def test_btmg_02() :

    imlist = lambda im : tuple(im.getdata())
    cntlist = lambda im : ( i for i , x in enumerate( imlist(im) ) if x == 0 )

    BC30 = BtGrid(30)

    L3val = 582314716142985563463246078

    im = BC30.getImage(L3val,Che.핵체)
    im2 = Image.open( os.path.join("../test/_img","btgrid-02-1.png"))


    il_1 = imlist(im)
    il_2 = imlist(im2)
    assert len(il_1) == len(il_2) 

    aaa = []
    for x in range( len(il_1) ):
        if il_1[x] != il_2[x] : aaa.append(x)
            
    #assert cntlist(im) == cntlist(im2)
    
    return il_1 , il_2, aaa
    
il_1 , il_2, aaa = test_btmg_02()

    
