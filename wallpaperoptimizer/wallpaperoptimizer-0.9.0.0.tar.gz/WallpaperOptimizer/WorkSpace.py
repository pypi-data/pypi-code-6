# -*- coding: utf-8 -*-

import os.path
import subprocess
import re

from WallpaperOptimizer.Imaging.Rectangle import Rectangle


class WorkSpace(Rectangle):
    class WorkSpaceRuntimeError(Exception):
        def __init__(self, msg):
            self.value = msg

        def __str__(self):
            return repr(self.value)

    def getScreenSize(self):
        return (
            (self.lScreen.Size.w, self.lScreen.Size.h),
            (self.rScreen.Size.w, self.rScreen.Size.h)
        )

    def getDepth(self):
        return self.lScreen.depth

    def isSeparate(self):
        return self.separate

    #!	Twinview時に、各スクリーンサイズがxdyinfoでは取れないのでやはり必要
    def setScreenSize(self, lDisplay, rDisplay):
        self.lScreen.setSize(lDisplay[0], lDisplay[1])
        self.rScreen.setSize(rDisplay[0], rDisplay[1])

    def compareToScreen(self):
        if self.Size.w < (self.lScreen.Size.w + self.rScreen.Size.w):
            return False
        if self.Size.h > self.lScreen.Size.h:
            setattr(self.lScreen.Size, 'islessThanWorkSpaceHeight', True)
        elif self.Size.h > self.rScreen.Size.h:
            setattr(self.rScreen.Size, 'islessThanWorkSpaceHeight', True)
        else:
            pass
        return True

    def setAttrScreenBool(self, lBool, rBool):
        setattr(self.lScreen, 'bSetting', lBool)
        setattr(self.rScreen, 'bSetting', rBool)

    def setAttrScreenType(self):
        if self.lScreen.isSquare():
            setattr(self.lScreen, 'displayType', 'square')
        if self.lScreen.isWide():
            setattr(self.lScreen, 'displayType', 'wide')
        if self.rScreen.isSquare():
            setattr(self.rScreen, 'displayType', 'square')
        if self.rScreen.isWide():
            setattr(self.rScreen, 'displayType', 'wide')
        if (
                (
                    not self.separate and
                    not self.lScreen.bSetting and
                    not self.rScreen.bSetting
                ) or (self.separate and not self.lScreen.bSetting)
        ):
            raise WorkSpace.WorkSpaceRuntimeError(
                'Screen definition is not valid.')

    def __init__(self):
        Rectangle.__init__(self)
        self.lScreen = Rectangle()
        self.rScreen = Rectangle()
        self.lScreen.setSize(0, 0)  # Rectangle Method
        self.rScreen.setSize(0, 0)  # Rectangle Method
        setattr(self.lScreen, 'depth', 24)
        setattr(self.rScreen, 'depth', 24)

        xdpyinfo = '/usr/bin/xdpyinfo'
        if not os.path.exists(xdpyinfo):
            raise WorkSpace.WorkSpaceRuntimeError(
                'xdpyinfo not installed [%s]' % xdpyinfo)
        dimensions = (subprocess.Popen(
            ["grep", "dimensions"],
            stdin=subprocess.Popen([xdpyinfo], stdout=subprocess.PIPE).stdout,
            stdout=subprocess.PIPE).communicate()[0].rstrip()).splitlines()
        depths = (subprocess.Popen(
            ["grep", "depth of root window"],
            stdin=subprocess.Popen([xdpyinfo], stdout=subprocess.PIPE).stdout,
            stdout=subprocess.PIPE).communicate()[0].rstrip()).splitlines()

        #"  dimensions:    3200x1080 pixels (856x292 millimeters)"
        for i, dimension in enumerate(dimensions):
            ptn = re.compile('[\s]+|x')
            subStr = ptn.split(dimension)
            if i == 0:
                self.lScreen.setSize(int(subStr[2]), int(subStr[3]))
            else:
                self.rScreen.setSize(int(subStr[2]), int(subStr[3]))

        for i, depth in enumerate(depths):
            ptn = re.compile('[\s]')
            subStr = ptn.split(depth)
            if i == 0:
                self.lScreen.depth = int(subStr[9])
            else:
                self.rScreen.depth = int(subStr[9])

        if len(dimensions) > 1:
            setattr(self, 'separate', True)
            # とりあえず左画面サイズをWorkSpaceのサイズに
            self.setSize(
                self.lScreen.Size.w,
                self.lScreen.Size.h)  # Rectangle Method
        else:
            setattr(self, 'separate', False)
            if self.lScreen.Size.h > self.rScreen.Size.h:
                h = self.lScreen.Size.h
            else:
                h = self.rScreen.Size.h
            self.setSize(
                self.lScreen.Size.w + self.rScreen.Size.w,
                h)  # Rectangle Method
