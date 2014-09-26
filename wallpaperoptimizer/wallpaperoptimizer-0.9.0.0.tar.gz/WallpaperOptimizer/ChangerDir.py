# -*- coding: utf-8 -*-

import os.path
import re
import random


class ChangerDir(object):
    class FileCountZeroError(Exception):
        def __init__(self, value):
            self.value = value

        def __str__(self):
            return repr(self.value)

    def getImgfileSeq(self):
        if (self.maxlen <= self.fIdx):
            self.fIdx = 0
        fullpathimgfile = self.fullpathimgfiles[self.fIdx]
        self.fIdx += 1
        return fullpathimgfile

    def getImgfileRnd(self):
        return self.fullpathimgfiles[int(random.randint(0, self.maxlen - 1))]

    def __init__(self, srcdir='.'):
        self.fIdx = 0
        Ext = re.compile(r"\.(gif|jpg|jpeg|bmp|png)$", re.IGNORECASE)
        srcdir = os.path.abspath(os.path.expanduser(srcdir))
        imgfiles = os.listdir(srcdir)
        self.fullpathimgfiles = []
        for imgfile in imgfiles:
            x = os.path.join(srcdir, imgfile)
            if (os.path.isfile(x) and Ext.search(imgfile)):
                self.fullpathimgfiles.append(os.path.abspath(x))
        self.maxlen = len(self.fullpathimgfiles)

        if (self.maxlen == 0):
            raise ChangerDir.FileCountZeroError(
                'Directory does not have Imgfile [%s]' % srcdir)
