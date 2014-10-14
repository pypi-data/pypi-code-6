#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Duplicate class is responsible for search and duplicate files
    it is desired to remove a function of their extension.

"""

__title__ = 'job'
__version__ = '0.4'
__author__ = 'julien@hautefeuille.eu'

import os
import shutil
import hashlib


class Duplicate(object):
    """
        Duplicate check duplicates and remove choosen extensions.

    """
    def __init__(self, source, destination, extension, typehash, parent=None):
        """
            Init paths, hash type and extension string.

        """
        super(Duplicate, self).__init__()
        self.spath = source
        self.dpath = destination
        self.exten = extension
        self.thash = typehash

    @staticmethod
    def hashf(filename, typehash):
        """
            Hashing file.

        """
        blocksize = 65536
        if typehash == "sha1":
            h = hashlib.sha1()
        elif typehash == "md5":
            h = hashlib.md5()
        else:
            h = hashlib.sha1()
        with open(filename, 'rb') as afile:
            buf = afile.read(blocksize)
            while len(buf) > 0:
                h.update(buf)
                buf = afile.read(blocksize)
        return h.hexdigest().upper()

    def run(self):
        """
            Run main process, it's a generator.

        """
        fname = ""
        hfile = ""
        fcoun = 0
        hdict = {}

        for root, dirs, files in os.walk(self.spath):
            for f in files:
                fcoun += 1
                # Filename
                fname = os.path.join(root, f)
                # Hash file
                hfile = self.hashf(fname, self.thash)
                # File extension
                fextn = os.path.splitext(fname)[1][1:].strip().lower()
                # Standard message
                messg = {"file": fname,
                         "hash": hfile,
                         "coun": fcoun}

                # Conditions
                h = self.spath and not self.dpath and not self.exten
                d = self.spath and self.dpath and not self.exten
                r = self.spath and not self.dpath and self.exten
                a = self.spath and self.dpath and self.exten
                n = not self.spath and not self.dpath and not self.exten

                # Process
                if h:
                    hdict[fname] = hfile
                    yield messg
                elif d:
                    if hfile in hdict.itervalues():
                        shutil.move(fname, self.dpath)
                        messg["dupl"] = True
                        yield messg
                    else:
                        hdict[fname] = hfile
                        yield messg
                elif r:
                    if fextn in self.exten:
                        os.remove(fname)
                        messg["kill"] = True
                        yield messg
                    else:
                        hdict[fname] = hfile
                        yield messg
                elif a:
                    if fextn in self.exten:
                        os.remove(fname)
                        messg["kill"] = True
                        yield messg
                    elif hfile in hdict.itervalues():
                        shutil.move(fname, self.dpath)
                        messg["dupl"] = True
                        yield messg
                    else:
                        hdict[fname] = hfile
                        yield messg
                elif n:
                    break
                else:
                    break

if __name__ == '__main__':
    d = Duplicate(
        source="Z:\\dev\\pydouble\\test\\dump\\",
        destination="Z:\\dev\\pydouble\\test\\duplicates\\",
        extension="txt db jpg", typehash="md5")

    for elem in d.run():  # it's a generator
        print elem
