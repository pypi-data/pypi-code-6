from PIL import Image, ImageDraw
# 각종부호 
class BtOpt(dict):
    
    pass
    
import re , functools

def get_fos_data(fos_string):
    a = re.findall("\([^)]+\)",fos_string)
    a = map(eval,a)
    a = functools.reduce( lambda a,b: a+b , a  )
    a = map(lambda i : i+150 ,a)
    return list(a)


fos_string=\
'''
-mousePressEvent
* (-30.0, -30.0)
px length 1
-mousePressEvent
* (-30.0, 30.0)
px length 2
-mousePressEvent
* (30.0, 30.0)
px length 3
-mousePressEvent
* (30.0, -30.0)
px length 4
-mousePressEvent
* (-30.0, -30.0)
px length 3
-mousePressEvent
* (-15.0, -15.0)
px length 4
-mousePressEvent
* (-15.0, 15.0)
px length 5
-mousePressEvent
* (15.0, 15.0)
px length 6
-mousePressEvent
* (15.0, -15.0)
px length 7
-mousePressEvent
* (-15.0, -15.0)
px length 6

'''
a = get_fos_data(fos_string)


im = Image.new('1',(300,300),color=255 )
draw = ImageDraw.Draw(im)

#a = [127.5, 30.0, 150.0, 30.0, 150.0, 15.0, 135.0, 0.0, 120.0, 0.0, 105.0, 15.0, 105.0, 37.5, 127.5, 60.0, 157.5, 60.0, 195.0, 22.5, 195.0, 15.0, 180.0, 15.0, 165.0, 30.0, 150.0, 37.5, 127.5, 37.5, 120.0, 30.0, 120.0, 15.0]
draw.polygon( a , fill = 0)

im.save("t04.png")




