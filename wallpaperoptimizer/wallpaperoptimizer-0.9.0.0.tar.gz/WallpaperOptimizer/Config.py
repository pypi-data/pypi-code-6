# -*- coding: utf-8 -*-

# ~.wallpaperoptimizer/walloptrc
#1920x1080,left,srcdir
#1280x1024,right,srcdir

# console版では、.walloptrcは上書きしない


class Config(object):
    class FormatError(Exception):
        def __init__(self, value):
            self.value = value

        def __str__(self):
            return repr(self.value)

    class Display(object):

        def toIntAsSizestring(self, val):
            wh = val.split('x')
            self.width = int(wh[0])
            self.height = int(wh[1])

        def setWidth(self, val):
            self.width = val

        def setHeight(self, val):
            self.height = val

        def setPosit(self, val):
            self.posit = val

        def setSrcdir(self, val):
            self.srcdir = val

        def _setConfig(self, w, h, p, s):
            self.width = w
            self.height = h
            self.posit = p
            self.srcdir = s

        def checkBool(self):
            if (self.width != 0 and self.height != 0 and self.srcdir != ''):
                self.bSetting = True

        def getBool(self):
            return self.bSetting

        def __init__(self):
            self.width = 0
            self.height = 0
            self.posit = None
            self.srcdir = ''
            self.bSetting = False

    def _setConfig(self, size, p, s):
        if p == 'left':
            display = self.lDisplay
        elif p == 'right':
            display = self.rDisplay
        else:
            raise Config.FormatError("position setting is left or right")
        subStr = size.split('x')
        display._setConfig(int(subStr[0]), int(subStr[1]), p, s)

    def __init__(self,
                 configfile=None,
                 lsize=None,
                 rsize=None,
                 srcdir=['', '']):
        self.lDisplay = Config.Display()
        self.rDisplay = Config.Display()
        self.bSetting = False

        if (configfile is not None):
            # config set from configfile
            cf = open(configfile, 'r')
            try:
                i = 0
                for i, cfline in enumerate(cf):
                    subStr = cfline.rstrip().split(',')
                    self._setConfig(subStr[0], subStr[1], subStr[2])
            except ValueError:
                cf.close()
                raise Config.FormatError(
                    "configfile written not expected Value")

            cf.close()
            if i < 1:
                raise Config.FormatError("Config require 2 records")

        else:
            self.lDisplay.setPosit('left')
            self.rDisplay.setPosit('right')

        self.lDisplay.checkBool()
        self.rDisplay.checkBool()
