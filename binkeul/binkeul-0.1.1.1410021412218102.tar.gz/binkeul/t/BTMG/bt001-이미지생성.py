'''
http://stackoverflow.com/questions/10615901/trim-whitespace-using-pil
'''
from PIL import Image, ImageDraw,  ImageChops

im = Image.new('RGB',(100,100) )
jm = Image.new('RGB',(100,100) )

draw = ImageDraw.Draw(im)
draw.rectangle([0,0,70,70] ,fill=(100,100,255))

draw = ImageDraw.Draw(jm)
draw.rectangle([30,30,100,100] ,fill=(100,255,100))

xm = Image.blend( im, jm , 0.5 ) 
xm.save("aa.png")
