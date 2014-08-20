#!/usr/bin/python
'''
  sprites.py
  ~~~~~~~~~~

  A tools for css sprites. Suport import Photoshop layer data as
  sprites. Pick by prefix, merge them up and output a css and png
  files.

  Example usage for command line:

  # import layer whose name starts with "icon-" from page1.psd,
  # reposition them, output the css with width and height
  # for each sprite to "page1.css", and output the merged png to
  # "page1.png"
  $ pysprites -i page1.psd -m icon- -b -r -c page1.css -o page1.png

  $ pysprites -i page*.psd -a icons/*.png -m icon- -b\
              -r -c icon.css -o icon.png

  For more detail see the sprites function.

'''

import warnings

try:
    from psd_tools import PSDImage
    from psd_tools.user_api.psd_image import Group, Layer
    from PIL import ImageCms
except ImportError :
    warnings.warn('no psd_tools')
    PSDImage = Group = Layer = None

from PIL import Image
import sys
import math

def isgroup(d) :
    '''Check if is a PSD Group Layer.'''
    return type(d) == Group

def islayer(d) :
    '''Check if is a normal layer.'''
    return type(d) == Layer

class GSP :

    '''
    General Sprite Process Group. Every fields is public.

    :param width: the width of this group.
    :param height: the height of this group.
    :param args: arguments, maybe set or read in some processing.
    :param padding: the padding of the sprites in output.
    :param prefix: filter sprite, only name startswith prefix will be hold.
    :param img : a array of list sprite data [name, [width, height],
                 [left, top], PIL_object]
    '''

    def __init__(self, width, height, args, prefix, padding, img=None) :
        if not img :
            img = []
        self.width = width
        self.height = height
        self.padding = padding
        self.img = img
        self.prefix = prefix
        self.args = args

def gsp_import_psd(gsp, *psds):
    '''
    Import psd layer as img into a GSP. Only import the layer startswith
    gsp.prefix. This will just place the layer as same as in the psd file.
    And the width and height of gsp will just be set to the max value
    of sprites.

    :param gsp: a GSP instance to process
    :param psds: a filename list of psd files
    '''
    def f(psd, prefix, buf) :
        for r in psd.layers :
            if not r.visible :
                continue
            if isgroup(r) :
                f(r, prefix, buf)
            elif islayer(r) and r.bbox.width > 0 and\
                 r.bbox.height > 0 :
                if not prefix or r.name.startswith(prefix) :
                    buf.append([r.name, [r.bbox.width, r.bbox.height],
                                [r.bbox.x1, r.bbox.y1], r.as_PIL()])
    for fn in psds :
        psd = PSDImage.load(fn)
        gsp.width = max(gsp.width, psd.header.width)
        gsp.height = max(gsp.height, psd.header.height)
        f(psd, gsp.prefix, gsp.img)

class EdgeLines :

    '''
    EdgeLines data struct for the repoisiton algorithm.
    For more details about this algorithm, see the document.
    '''
    
    def __init__(self, length) :
        self._e = [0] * length

    def inc(self, start, end, c) :
        for i in range(start, end+1) :
            self._e[i] += c
        return self._e[start]

    def up(self, start, end) :
        m = None
        if (start > 0) and (self._e[start-1] > self._e[start]) :
            m = self._e[start-1]
        if end + 1 < len(self._e) and (self._e[end+1] > self._e[end]) :
            if (m is None) or (m > self._e[end+1]) :
                m = self._e[end+1]
        if m is not None :
            self.inc(start, end, m - self._e[start])
        else :
            raise ValueError('No m')

    def lowest(self) :
        ls = None
        lr = None
        ts = 0
        e = self._e
        el = len(self._e) - 1
        for i in range(len(self._e)) :
            if i > 0 and e[i-1] != e[i] :
                ts = i
            elif (i == el) or (e[i] != e[i+1]) :
                if (ls == None) or\
                   (e[i] < e[ls]) or\
                   ((e[i] == e[ls]) and ((i - ts) > (lr - ls))) :
                    ls = ts
                    lr = i
        return ls, lr, e[ls]

def gsp_reposition(gsp) :
    '''
    Reposition images.
    For more details about this algorithm, see the document.
    '''
    padding = gsp.padding
    img = gsp.img
    if padding :
        for x in img :
            x[1][0] += padding *2
            x[1][1] += padding *2
    height = [x[1][1] for x in img]
    height.sort(reverse=True)
    height = sum(height[:2])
    e= EdgeLines(height)
    def cmp_rec(a, b):
        if a[1][0] > b[1][0] : return -1
        if b[1][0] > a[1][0] : return 1
        if a[1][1] > b[1][1] : return -1
        if b[1][1] > a[1][1] : return 1
        return 0
    img.sort(cmp=cmp_rec)
    gsp.img = ret = []
    width = 0
    while img :
        l = e.lowest()
        he = l[1] - l[0] + 1
        for index, ele in enumerate(img) :
            if ele[1][1] <= he :
                width = max(width, e.inc(l[0], l[0] + ele[1][1] - 1, ele[1][0]))
                ele[2][0], ele[2][1] = l[2] + padding, l[0] + padding
                ele[1][0] -= padding * 2
                ele[1][0] -= padding * 2
                ret.append(ele)
                del img[index]
                break
        else :
            e.up(l[0], l[1])
    gsp.width = width
    gsp.height = height

def gsp_save(gsp, filename) :
    '''
    Save the image as a png file.
    '''
    cc = Image.new('RGBA', (gsp.width, gsp.height))
    for ele in gsp.img :
        cc.paste(ele[3], tuple(ele[2]))
    cc.save(filename)

def gsp_gencss(gsp, filename) :
    '''
    Generate a css of this gsp, save to filename.
    '''
    img = gsp.img
    prefix = gsp.args.get('cp', 'icon-')
    withsize = 'b' in gsp.args
    buf = []
    buf.append(', '.join('.%s%s' % (prefix, x[0]) for x in img))
    buf.append('''{
    /* common */
    background-image: url();
    display: inline-block;
    background-repeat: no-repeat;
}

''')
    for x in img :
        buf.append('''.%s%s{
        background-position: -%spx -%spx;''' % (prefix, x[0], x[2][0], x[2][1]))
        if withsize :
            buf.append('''
    width: %spx;
    height: %spx;''' % (x[1][0], x[1][1]))
        buf.append('\n}\n\n')
    return open(filename, 'w').write(''.join(buf))

def gsp_addimg(gsp, *filenames):
    '''
    Add images from files into gsp.img.
    '''
    img = gsp.img
    for x in filenames :
        im = Image.open(x)
        gsp.width = max(gsp.width, im.size[0])
        gsp.height = max(gsp.height, im.size[1])
        gsp.img.append(['_'.join(x.split('.')[:-1]),
                        [im.size[0], im.size[1]],
                        [0, 0], im])

def parse_argv(argv) :
    kwargs = {}
    key = '_'
    value = True
    for x in argv :
        if x[0] == '-' :
            if key is not None :
                kwargs[key] = value
                value = True
            key = x[1:]
        elif value is True :
            value = x
        elif type(value) == str :
            value = [value, x]
        else :
            value.append(x)
    if key is not None :
        kwargs[key] = value
    return kwargs

def sprites(**kwargs) :
    '''
    Do with sprites.

    -i a.psd b.psd ... : import psd layer from psd files (need psd_tools)
    -a x.png y.png ... : add png files
    -m filter  : only handle layer or image name startswith filter
    -p padding : add padding for each sprite
    -r         : reposition sprites
    -cp string : use string as css class prefix
    -b         : gen sprite width and height for css
    -c out.css : output css to file
    -o out.png : output merged png to file

    Example usage for command line:
    
    # import layer whose name starts with "icon-" from page1.psd,
    # reposition them, output the css with width and height
    # for each sprite to "page1.css", and output the merged png to
    # "page1.png"
    $ pysprites -i page1.psd -m icon- -b -r -c page1.css -o page1.png

    $ pysprites -i page*.psd -a icons/*.png -m icon- -b -r -c icon.css -o icon.png

    '''
    if 'h' in kwargs :
        print sprites.__doc__
        return
    prefix = kwargs.get('m', '')
    padding = int(kwargs.get('p', 1))
    gsp = GSP(0, 0, kwargs, prefix, padding)

    if 'i' in kwargs :
        ifs = kwargs['i']
        if type(ifs) != list :
            ifs = [ifs]
        gsp_import_psd(gsp, *ifs)

    if 'a' in kwargs:
        aifs = kwargs['a']
        if type(aifs) != list :
            aifs = [aifs]
        gsp_addimg(gsp, *aifs)

    if 'r' in kwargs :
        gsp_reposition(gsp)

    if 'o' in kwargs :
        ofs = kwargs['o']
        gsp_save(gsp, ofs)
    
    if 'c' in kwargs :
        ocss = kwargs['c']
        gsp_gencss(gsp, ocss)

if __name__ == "__main__" :
    import sys
    sprites(**parse_argv(sys.argv))
