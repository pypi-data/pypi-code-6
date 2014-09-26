# -*- coding: utf-8 -*-

from math import floor

from WallpaperOptimizer.Imaging.Bounds import Bounds


class Rectangle(Bounds):
    class Size(object):
        w = 0
        h = 0

    def getSize(self):
        return self.Size

    def setSize(self, w, h):
        self.Size.w = w
        self.Size.h = h
        self.setWidth(w)
        self.setHeight(h)

    def isSquare(self):
        if (self.Size.w == 0 and self.Size.h == 0):
            return False
        widthAs = 4
        heightAs = 3
        if not self.checkAspectRatio(widthAs, heightAs):
            widthAs = 5
            heightAs = 4
            return self.checkAspectRatio(widthAs, heightAs)
        else:
            return True

    def isWide(self):
        if (self.Size.w == 0 and self.Size.h == 0):
            return False
        widthAs = 16
        heightAs = 9
        if not self.checkAspectRatio(widthAs, heightAs):
            widthAs = 16
            heightAs = 10
            return self.checkAspectRatio(widthAs, heightAs)
        else:
            return True

    def isDual(self):
        if (self.Size.w == 0 and self.Size.h == 0):
            return False
        widthAs = 8
        heightAs = 2.7
        return self.checkAspectRatio(widthAs, heightAs)

    def checkAspectRatio(self, widthAs, heightAs):
        quotient_w = floor(self.Size.w / widthAs)
        quotient_h = floor(self.Size.h / heightAs)
        if (quotient_w == quotient_h):
            return True
        else:
            return False

    def contains(self, other):
        if (self.Size.w >= other.Size.w and self.Size.h >= other.Size.h):
            return True
        else:
            return False

    def containsPlusMergin(self, other, mergin=(0, 0, 0, 0)):
        # mergin(left/right/top/bottom)
        if (
            self.Size.w >= (other.Size.w + mergin[0] + mergin[1]) and
            self.Size.h >= (other.Size.h + mergin[2] + mergin[3])
        ):
            return True
        else:
            return False

    def __init__(self):
        self.Size = Rectangle.Size()
        Bounds.__init__(self)
