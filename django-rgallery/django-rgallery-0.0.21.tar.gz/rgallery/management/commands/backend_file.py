# -*- coding: utf-8 -*-
import os
import re
import sys
import time
import datetime
import gzip
import glob

from django.conf import settings as conf


class File(object):
    path = ""

    # The class "constructor" - It's actually an initializer
    def __init__(self, path):
        self.path = path


def get_contents(srcdir, debug):
    types = (srcdir + '/*.jpg',
             srcdir + '/*.JPG')
    bucket = []
    for files in types:
        bucket.extend(glob.glob(files))

    if debug:
        for file in bucket:
            print file

    file2 = []
    for file in bucket:
        file2.append(File(file))

    # Returns False for compatibility reasons
    return False, file2


def get_images(cont):
    pass

def download(client, file, nombre_imagen, srcdir, destdir, debug):
    # Keeps client and destdir arguments for compatibility reasons
    # but they're  not used
    f = open(file.path, 'r')
    img = srcdir + '/' + nombre_imagen
    out = open(img, 'wb')
    out.write(f.read())
    out.close()
    if debug:
        print "      Descargada"
    return img
