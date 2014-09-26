# -*- coding: utf-8 -*-

import sys

try:
    from PIL import Image  # @UnresolvedImport
except:
    print 'not installed Python Imaging Library (PIL)'
    print 'ex) sudo apt-get install python-imaging'
    print 'ex) sudo yum install python-imaging'
    sys.exit(2)

from WallpaperOptimizer.Imaging.Rectangle import Rectangle


class ImgFile(Rectangle, Image.Image):
    class ImgFileIOError(IOError):
        def __init__(self, value):
            self.value = value

        def __str__(self):
            return repr(self.value)

    def show(self):
        self._img.show()

    def reSize(self, w, h):
        size = (w, h)
        self._img = self._img.resize(size, Image.ANTIALIAS)
        self.setSize(self._img.size[0], self._img.size[1])

    def paste(self, image, box):
        self._img.paste(image._img, box)

    def save(self, path):
        try:
            self._img.save(path)
        except IOError:
            raise ImgFile.ImgFileIOError('Cannot save Imgfile [%s]' % path)

    def __init__(self, path='', color='black', w=5, h=5):
        Rectangle.__init__(self)
        if path == '':
            mode = 'RGB'
            size = (w, h)
            self._img = Image.new(mode, size, color)
        else:
            try:
                self._img = Image.open(path)
            except:
                raise ImgFile.ImgFileIOError('Cannot load Imgfile [%s]' % path)
        #Rectangle Method
        self.setSize(self._img.size[0], self._img.size[1])
