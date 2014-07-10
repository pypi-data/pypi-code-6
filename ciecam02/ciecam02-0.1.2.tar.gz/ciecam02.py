"""a set of function convert colorspace among rgb ciexyz ciecam02.
functions:
xyz2rgb(xyz):
    convert xyz 2 rgb mode
    Args:
        xyz: a list like [x, y, z]  0<x<95.047, 0<y<100.0 0<z<108.883
    Returns:
        a list contains rgb value like [r,g,b]
        the rgb value type is integer range from  0  to 255

rgb2xyz(list rgb):
    convert rgb 2 xyz mode
    Args:
        rgb: a list like [r,g,b]  r,g,b is integer value range from 0 to 255
    Returns:
        a list contains x,y,z value like [x,y,z]
        the xyz value is float  0<x<95.047, 0<y<100.0 0<z<108.883

xyz2cam02(list XYZ,XwYwZw=[95.05,100.00,108.88],Nc=0.9,c=0.59,F=0.9,LA=80.0,Yb=16.0):
convert xyz 2 cam02 data

Args:
    XYZ:    contains [X,Y,Z] value
    XwYwZw: target white point xyz, provide a default value
    Nc,c,F: environment parameter
            CIE defined 3 environments which named
                dim:     0.9, 0.59, 0.9  for display device
                average: 1.0, 0.69, 1.0  for normal print
                dark:    0.8, 0.525,0.8  for project device
            which are not imutable
    LA:     light indensity by unit lcd/cm2
    Yb:     the background light indensity in the scene
Returns:
    retvalue: [h,H,J,Q,C,M,s]

        h,H:  Hue value
              h: the same procedure as CIELAB ranging 0 to 360
              H: hue quadrature value ranging from 0  to 400
        J,Q:  Lightness and Brightness
        C,M,s: C:chroma, M:Colorfulness, s:saturation

def rgb2jch(list color):
    provide a quick convertion from rgb to cam02 JCH value

    XwYwZw default to [95.05,100.00,108.88]
    Nc,c,F default to dim mode 0.9,0.59,0.9
    LA,Yb  default to 80.0 16.0

    Args:
        color: need to provide [r,g,b] list ranging from 0 to 255 integer

    Returns:
        [J,C,H]
         J: Lightness ranging from 0 to 100 float
         C: Chroma
         H: Hue quadrature ranging from 0 to 400

def jch2xyz(list jch):
    provide a quick convertion from cam02 JCH value to xyz

    XwYwZw default to [95.05,100.00,108.88]
    Nc,c,F default to dim mode 0.9,0.59,0.9
    LA,Yb  default to 80.0 16.0

    Args:
         jch: need to provide [J,C,H] list
            J: Lightness ranging from 0 to 100 float
            C: Chroma
            H: Hue quadrature ranging from 0 to 400
    Returns:
         XYZ list like [X,Y,Z]

def jch2rgb(list jch):
    provide a quick convertion from cam02 JCH value to rgb

    XwYwZw default to [95.05,100.00,108.88]
    Nc,c,F default to dim mode 0.9,0.59,0.9
    LA,Yb  default to 80.0 16.0

    Args:
         jch: need to provide [J,C,H] list
            J: Lightness ranging from 0 to 100 float
            C: Chroma
            H: Hue quadrature ranging from 0 to 400
    Returns:
         RGB list like [R,G,B]


"""
__all__ = ["xyz2rgb","rgb2xyz","xyz2cam02","rgb2jch","jch2xyz","jch2rgb"]

from ciecam02x import xyz2rgb,rgb2xyz,xyz2cam02,rgb2jch,jch2xyz,jch2rgb
