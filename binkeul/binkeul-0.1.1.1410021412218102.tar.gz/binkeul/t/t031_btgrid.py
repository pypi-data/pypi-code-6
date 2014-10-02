from binkeul.btgrid import * 
import pprint, pdb

pprint.pprint(BtGrid.L3BMAP)

BC30 = BtGrid(6)


l3val = 582314716142985563463246078

im = BC30.getImage(l3val,False)
im.save('btmg03.png')

pprint.pprint(BC30)
print( BC30.getRect(l3val) )

#-----------------#-----------------#-----------------

BC30 = BtGrid(30)
btm = BC30.getBtmg(582314716142985563463246078)

im = Image.new('1',(500,500),color=255 )
ofs = [200,200]
pil_draw = ImageDraw.Draw(im)

btm( pil_draw, ofs )

im.save('btmg04.png')

print( BC30.getHtmlImg(582314716142985563463246078) )
